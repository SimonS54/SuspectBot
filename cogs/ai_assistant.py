import discord
import openai
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from firebase_config import db  # Firestore database instance
from firebase_admin import firestore
from config import CATEGORY_IDS, AI_REVIEW_CHANNEL_ID  # Configuration constants
import datetime
import asyncio
from Levenshtein import distance as levenshtein_distance  # For string similarity comparison
import re
import time
import logging
import uuid  # For generating unique message IDs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables and set OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants for ticket management and staff roles
MAX_TICKETS = 50  # Maximum number of tickets to retain
STAFF_ROLE_IDS = {1297999380745420822, 1297999355860615209, 1297999091187581020}  # Staff role IDs
NOTIFY_USER_ID = 368435292916416512  # User to notify about ticket closures
EMBED_FIELD_LIMIT = 1000  # Maximum characters per embed field

# Define an AIAssistant cog to handle AI-driven ticket support
class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance
        self.active_tickets = {}  # Cache of active ticket IDs
        self.assistant_id = "asst_kMPncHzly9M28mIQtCLe102e"  # OpenAI Assistant ID
        self.client = openai.OpenAI()  # OpenAI client instance
        self.pending_clarifications = {}  # Track tickets awaiting clarification
        self.check_closed_tickets.start()  # Start the background task for checking closed tickets

    # Load existing tickets from Firestore when the cog is initialized
    async def cog_load(self):
        tickets_ref = db.collection("tickets")
        tickets = tickets_ref.stream()
        for ticket in tickets:
            ticket_data = ticket.to_dict()
            ticket_id = ticket_data.get("ticket_id")
            if ticket_id and ticket_id.isdigit():
                self.active_tickets[ticket_id] = True
            else:
                logger.info(f"Skipping invalid ticket ID: {ticket_id} from document {ticket.id}")
        logger.info(f"Initialized with {len(self.active_tickets)} tickets.")

    # Enforce the maximum ticket limit by removing oldest tickets
    async def enforce_ticket_limit(self):
        tickets_ref = db.collection("tickets")
        tickets = list(tickets_ref.order_by("created_at").stream())
        if len(tickets) > MAX_TICKETS:
            tickets_to_remove = tickets[:len(tickets) - MAX_TICKETS]
            for ticket in tickets_to_remove:
                ticket_id = ticket.to_dict().get("ticket_id", ticket.id)
                ticket.reference.delete()
                if ticket_id in self.active_tickets:
                    del self.active_tickets[ticket_id]
                logger.info(f"Removed old ticket: {ticket_id}")
            logger.info(f"Ticket count reduced to {MAX_TICKETS}")

    # Background task to periodically check for closed tickets
    @tasks.loop(minutes=5)
    async def check_closed_tickets(self):
        tickets_to_remove = []
        for ticket_id in list(self.active_tickets.keys()):
            channel = self.bot.get_channel(int(ticket_id))
            # Mark ticket as closed if the channel no longer exists or isn’t in a valid category
            if not channel or channel.category_id not in CATEGORY_IDS:
                doc_ref = db.collection("tickets").document(ticket_id)
                doc = doc_ref.get()
                if doc.exists:
                    ticket_data = doc.to_dict()
                    if not ticket_data.get("closed", False):
                        doc_ref.update({"closed": True})
                        logger.info(f"Ticket {ticket_id} marked as closed (channel not found).")
                        user = self.bot.get_user(NOTIFY_USER_ID)
                        if user:
                            ticket_count = len(list(db.collection("tickets").where(filter=firestore.FieldFilter("closed", "==", True)).stream()))
                            await user.send(f"Ticket {ticket_id} is closed. {ticket_count}/{MAX_TICKETS} tickets collected for fine-tuning.")
                            if ticket_count >= MAX_TICKETS:
                                await user.send("🎉 50 tickets collected! Ready for fine-tuning!")
                tickets_to_remove.append(ticket_id)

        for ticket_id in tickets_to_remove:
            del self.active_tickets[ticket_id]
        logger.info(f"Finished checking tickets. Active tickets remaining: {len(self.active_tickets)}")

    # Ensure the bot is ready before starting the ticket check loop
    @check_closed_tickets.before_loop
    async def before_check_closed_tickets(self):
        await self.bot.wait_until_ready()

    # Listener to process messages in ticket channels
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages to prevent self-triggering

        if message.channel.category_id not in CATEGORY_IDS:
            return  # Only process messages in designated ticket categories

        ticket_id = str(message.channel.id)
        user_id = str(message.author.id)
        is_staff = any(role.id in STAFF_ROLE_IDS for role in message.author.roles) if isinstance(message.author, discord.Member) else False
        role = "staff" if is_staff else "customer"

        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()

        # Generate a unique message ID
        message_id = str(uuid.uuid4())

        new_ticket = not doc.exists
        if doc.exists:
            # Update existing ticket with the new message
            ticket_data = doc.to_dict()
            ticket_data["messages"].append({
                "message_id": message_id,
                "user_id": user_id,
                "content": message.content,
                "timestamp": datetime.datetime.utcnow(),
                "role": role
            })
            doc_ref.update({"messages": ticket_data["messages"]})
        else:
            # Create a new ticket document with an empty suggestions array
            doc_ref.set({
                "ticket_id": ticket_id,
                "created_at": datetime.datetime.utcnow(),
                "messages": [{
                    "message_id": message_id,
                    "user_id": user_id,
                    "content": message.content,
                    "timestamp": datetime.datetime.utcnow(),
                    "role": role
                }],
                "suggestions": [],  # Initialize suggestions array
                "closed": False
            })
            self.active_tickets[ticket_id] = True
            logger.info(f"New ticket created and cached: {ticket_id}")

        if new_ticket:
            await self.enforce_ticket_limit()  # Enforce ticket limit for new tickets

        await self.check_for_suggestions(message.channel, ticket_id, message_id)  # Pass the message_id

    # Listener to handle ticket closure when a message is deleted
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        ticket_id = str(payload.channel_id)
        if ticket_id in self.active_tickets:
            doc_ref = db.collection("tickets").document(ticket_id)
            doc = doc_ref.get()
            if doc.exists:
                ticket_data = doc.to_dict()
                if not ticket_data.get("closed", False):
                    doc_ref.update({"closed": True})
                    logger.info(f"Ticket {ticket_id} marked as closed (message deleted).")
                    user = self.bot.get_user(NOTIFY_USER_ID)
                    if user:
                        ticket_count = len(list(db.collection("tickets").where(filter=firestore.FieldFilter("closed", "==", True)).stream()))
                        await user.send(f"Ticket {ticket_id} is closed. {ticket_count}/{MAX_TICKETS} tickets collected for fine-tuning.")
                        if ticket_count >= MAX_TICKETS:
                            await user.send("🎉 50 tickets collected! Ready for fine-tuning!")
            del self.active_tickets[ticket_id]

    # Listener to handle reactions on AI suggestion messages
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return  # Ignore bot reactions

        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)
        if reaction.message.channel.id != review_channel.id:
            return  # Only process reactions in the AI review channel

        logger.info(f"Searching for suggestion with message_id {reaction.message.id}")

        # Fetch the latest ticket state
        ticket_ref = None
        ticket = None
        suggestion_index = None
        tickets = db.collection("tickets").stream()
        for t in tickets:
            ticket_data = t.to_dict()
            suggestions = ticket_data.get("suggestions", [])
            for i, s in enumerate(suggestions):
                if isinstance(s, dict) and s.get("message_id") == str(reaction.message.id):
                    ticket = t
                    ticket_ref = db.collection("tickets").document(ticket_data["ticket_id"])
                    suggestion_index = i
                    break
            if ticket:
                break

        if not ticket or suggestion_index is None:
            logger.warning(f"No ticket found with suggestion message_id {reaction.message.id}")
            return  # No matching suggestion found

        ticket_id = ticket.to_dict()["ticket_id"]
        suggestion = ticket.to_dict()["suggestions"][suggestion_index]
        ai_response = suggestion["ai_response"]
        message_ref_id = suggestion["message_ref_id"]
        # Find the original message by message_ref_id
        original_message = next((m["content"] for m in ticket.to_dict()["messages"] if m["message_id"] == message_ref_id), None)

        if reaction.emoji == "👍":
            logger.info(f"✅ Approving AI response for ticket {ticket_id}")
            approved_ref = db.collection("approved_responses").document(ticket_id)
            try:
                # Save the approved response along with the original message to Firestore
                approved_entry = {
                    "response": ai_response,
                    "original_message": original_message
                }
                approved_ref.set({"responses": firestore.ArrayUnion([approved_entry])}, merge=True)
                embed = discord.Embed(
                    title="✅ AI Response Approved",
                    description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been approved and saved!",
                    color=discord.Color.red()
                )
                embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
                await reaction.message.channel.send(embed=embed, delete_after=5)
            except Exception as e:
                logger.error(f"Error approving response for ticket {ticket_id}: {str(e)}")

        elif reaction.emoji == "👎":
            logger.info(f"❌ Rejecting AI response for ticket {ticket_id}")
            try:
                # Fetch the latest document state
                current_doc = ticket_ref.get()
                current_suggestions = current_doc.to_dict().get("suggestions", [])
                if suggestion_index >= len(current_suggestions):
                    logger.error(f"Invalid suggestion_index {suggestion_index} for ticket {ticket_id}, array length: {len(current_suggestions)}")
                    return

                # Log the suggestion state before rejection
                logger.info(f"Before rejection, suggestion state: {suggestion}")

                # Update the suggestion by rewriting it
                updated_suggestion = current_suggestions[suggestion_index].copy()
                updated_suggestion["rejected"] = True
                current_suggestions[suggestion_index] = updated_suggestion

                logger.info(f"Applying update: setting suggestions[{suggestion_index}] to {updated_suggestion}")
                ticket_ref.update({"suggestions": current_suggestions})

                # Fetch and log the updated document state
                updated_doc = ticket_ref.get()
                updated_suggestions = updated_doc.to_dict().get("suggestions", [])
                if suggestion_index < len(updated_suggestions):
                    updated_suggestion = updated_suggestions[suggestion_index]
                    logger.info(f"After rejection, suggestion state: {updated_suggestion}")
                else:
                    logger.error(f"Suggestion index {suggestion_index} out of bounds after update for ticket {ticket_id}")

                embed = discord.Embed(
                    title="❌ AI Response Rejected",
                    description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been rejected. You can reply with a better response within 5 minutes to improve it for future use.",
                    color=discord.Color.red()
                )
                embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
                await reaction.message.channel.send(embed=embed, delete_after=5)

                # Check for staff correction within 5 minutes
                async def check_correction():
                    def check(m):
                        return m.channel.id == reaction.message.channel.id and isinstance(m.author, discord.Member) and any(role.id in STAFF_ROLE_IDS for role in m.author.roles)

                    try:
                        correction = await self.bot.wait_for('message', check=check, timeout=300)  # 5-minute window
                        try:
                            correction_doc = ticket_ref.get()
                            correction_suggestions = correction_doc.to_dict().get("suggestions", [])
                            if suggestion_index < len(correction_suggestions):
                                correction_suggestion = correction_suggestions[suggestion_index].copy()
                                correction_suggestion["staff_correction"] = correction.content
                                correction_suggestions[suggestion_index] = correction_suggestion
                                ticket_ref.update({"suggestions": correction_suggestions})
                                logger.info(f"Staff correction added for ticket {ticket_id}: {correction.content}")
                                success_embed = discord.Embed(
                                    title="✅ Correction Saved",
                                    description=f"{correction.author.mention}, your correction for ticket `{ticket_id}` has been successfully saved for future improvement.",
                                    color=discord.Color.green()
                                )
                                success_embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
                                await reaction.message.channel.send(embed=success_embed, delete_after=5)
                            else:
                                logger.error(f"Suggestion index {suggestion_index} out of bounds during correction for ticket {ticket_id}")
                        except Exception as e:
                            logger.error(f"Error updating staff_correction for ticket {ticket_id}: {str(e)}")
                    except asyncio.TimeoutError:
                        logger.info(f"No staff correction received within 5 minutes for ticket {ticket_id}")

                await check_correction()
            except Exception as e:
                logger.error(f"Error processing downvote for ticket {ticket_id}: {str(e)}")
                logger.error(f"Full exception details: {repr(e)}")

    # Score the quality of an AI response based on length and keyword overlap
    def score_response(self, response, question):
        if not response or len(response) < 20:
            return False
        question_words = set(question.lower().split())
        response_words = set(response.lower().split())
        overlap = len(question_words.intersection(response_words)) / len(question_words)
        return overlap > 0.2  # Require at least 20% keyword overlap

    # Request clarification from staff in the review channel instead of the ticket channel
    async def _request_clarification(self, channel, ticket_id, question):
        """Request clarification from staff in the review channel instead of the ticket channel."""
        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)  # Get the AI review channel
        embed = discord.Embed(
            title="🤖 Need More Info",
            description=f"For ticket `{channel.name}` (ID: {ticket_id}):\n"
                        f"Question: '{question}'\n"
                        f"Can staff specify what additional details are needed? (e.g., product, specific issue)",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
        await review_channel.send(embed=embed)  # Send to review channel instead of ticket channel
        self.pending_clarifications[ticket_id] = question  # Track pending clarification
        logger.info(f"Requested clarification for ticket {ticket_id} in review channel: {question}")

    # Check for and generate AI suggestions for customer messages
    async def check_for_suggestions(self, channel, ticket_id, message_id):
        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)
        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()
        if not doc.exists:
            logger.info(f"Ticket {ticket_id} not found in Firestore.")
            return

        messages = doc.to_dict().get("messages", [])
        if len(messages) < 1:
            logger.info(f"Ticket {ticket_id} has no messages yet.")
            return

        last_message = messages[-1]
        if last_message["role"] != "customer":
            logger.info(f"Skipping staff message in ticket {ticket_id}: '{last_message['content']}'")
            return

        message_content = last_message["content"].lower().strip()
        question_indicators = {'how', 'why', 'what', 'where', 'when', 'can', 'does', 'is', 'are',
                               'setup', 'install', 'fix', 'error', 'crash', 'problem', 'issue', 'help',
                               'cheat', 'chair', 'cheeto', 'spoofer', 'woofer', 'poofer'}
        casual_indicators = {'hi', 'hello', 'hey', 'thanks', 'thank you', 'ok', 'okay', 'cool'}

        # Skip casual messages or those not indicating a question
        if (not message_content or
                len(message_content) < 5 or
                any(message_content.startswith(word) for word in casual_indicators) or
                (not any(word in message_content.split() for word in question_indicators) and
                 not message_content.endswith('?'))):
            logger.info(f"Skipping casual/non-question message in ticket {ticket_id}: '{message_content}'")
            return

        # Check for approved responses from previous tickets
        last_msg_text = last_message["content"].lower()
        approved_docs = db.collection("approved_responses").stream()
        for doc in approved_docs:
            approved_data = doc.to_dict()
            for resp in approved_data.get("responses", []):
                resp_lower = resp["response"].lower() if isinstance(resp, dict) else resp.lower()
                similarity = levenshtein_distance(last_msg_text, resp_lower)
                if similarity <= min(len(last_msg_text), len(resp_lower)) * 0.2:
                    logger.info(f"Using approved response from ticket {doc.id} for ticket {ticket_id} (similarity: {similarity})")
                    return resp["response"] if isinstance(resp, dict) else resp  # Return only the response string

        # Prepare context and message for AI processing
        prior_context = "\n".join([f"{m['role'].capitalize()} {m['user_id']}: {m['content']}" for m in messages[:-1][-9:]])
        last_message_content = f"Customer {last_message['user_id']}: {last_message['content']}"

        question = last_message_content.split(': ', 1)[1].lower()
        product_names = {'apex lite', 'cheeto', 'chair', 'cheat', 'spoofer', 'woofer', 'poofer'}
        if any(term in question for term in {'it', 'this', 'that'}) and not any(name in question for name in product_names):
            last_product = next((m['content'].lower() for m in messages[:-1][::-1] if any(name in m['content'].lower() for name in product_names)), None)
            if last_product:
                resolved_product = next((name for name in product_names if name in last_product), "product")
                question = f"{resolved_product} {question.replace('it', '').replace('this', '').replace('that', '').strip()}"
                last_message_content = f"Customer {last_message['user_id']}: {question}"
                logger.info(f"Resolved vague reference to {resolved_product}: {question}")

        if ticket_id in self.pending_clarifications:
            prior_question = self.pending_clarifications.pop(ticket_id)
            question = f"{prior_question} - {question}"
            last_message_content = f"Customer {last_message['user_id']}: {question}"
            logger.info(f"Received clarification for ticket {ticket_id}: {question}")

        # Send initial embed to review channel with "Processing..."
        embed = discord.Embed(
            title="🤖 AI Suggestion",
            description=f"For ticket `{channel.name}`:",
            color=discord.Color.red()
        )
        embed.add_field(
            name="📝 Response",
            value="Processing...",
            inline=False
        )
        embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
        msg = await review_channel.send(embed=embed)

        # Get AI response first
        ai_response = await self._poll_ai_response(prior_context, last_message_content, ticket_id)
        resolution_source = None

        if ai_response:
            ai_response = re.sub(r"【.*†source】", "", ai_response).strip()
            if "NO_ANSWER" in ai_response:
                error_terms = {'error', 'crash', 'fix', 'bug', 'fail', 'broken'}
                product_terms = {'setup', 'install', 'update', 'load', 'run'}
                time_specific_terms = {'yesterday', 'today', 'now', 'just', 'recently', 'this morning', 'tonight', 'last night'}
                context_specific_terms = {'my setup', 'my account', 'my pc', 'my system', 'mine'}
                vague_terms = {'issues', 'why', 'sometimes', 'maybe', 'it', 'this', 'that'}
                product_names = {'apex lite', 'cheeto', 'chair', 'cheat', 'spoofer', 'woofer', 'poofer'}

                question_words = question.split()
                has_error = any(term in question_words for term in error_terms)
                has_product = any(term in question_words for term in product_terms)
                has_time = any(term in question_words for term in time_specific_terms)
                has_context = any(term in question for term in context_specific_terms)
                has_vague = any(term in question_words for term in vague_terms if term in {'it', 'this', 'that'} or term in question_words[:-1])
                has_product_name = any(name in question for name in product_names)

                if question.startswith('how'):
                    intent = 'setup' if has_product else 'vague'
                elif question.startswith(('why', 'what')):
                    intent = 'troubleshooting' if has_error else 'vague'
                else:
                    intent = 'troubleshooting' if has_error else 'setup' if has_product else 'vague'

                if ((intent == 'troubleshooting' or intent == 'setup') and
                        has_product_name and
                        not has_time and
                        not has_context and
                        not (has_vague and not (has_error or has_product))):
                    ai_response = await self._fallback_to_gpt(last_message_content, ticket_id)
                    if (not ai_response or
                            any(phrase in ai_response.lower() for phrase in ["i don't have", "i can't", "could be", "might be", "not sure"]) or
                            not self.score_response(ai_response, question)):
                        ai_response = "I am sorry to inform you that I cannot help you with this issue, please try forming your question differently or wait to receive help from the staff team."
                        resolution_source = "staff"
                    else:
                        resolution_source = "gpt"
                else:
                    reason = ("time-specific" if has_time else
                              "context-specific" if has_context else
                              "vague" if intent == 'vague' else
                              "no clear product/error")
                    if intent == 'vague' or has_context:
                        await self._request_clarification(channel, ticket_id, question)
                        return
                    logger.info(f"Skipping web search due to {reason} question: {question}")
                    ai_response = "I am sorry to inform you that I cannot help you with this issue, please try forming your question differently or wait to receive help from the staff team."
                    resolution_source = "staff"
            else:
                resolution_source = "vector"
        else:
            # Handle case where no initial AI response is received
            error_terms = {'error', 'crash', 'fix', 'bug', 'fail', 'broken'}
            product_terms = {'setup', 'install', 'update', 'load', 'run'}
            time_specific_terms = {'yesterday', 'today', 'now', 'just', 'recently', 'this morning', 'tonight', 'last night'}
            context_specific_terms = {'my setup', 'my account', 'my pc', 'my system', 'mine'}
            vague_terms = {'issues', 'why', 'sometimes', 'maybe', 'it', 'this', 'that'}
            product_names = {'apex lite', 'cheeto', 'chair', 'cheat', 'spoofer', 'woofer', 'poofer'}

            question_words = question.split()
            has_error = any(term in question_words for term in error_terms)
            has_product = any(term in question_words for term in product_terms)
            has_time = any(term in question_words for term in time_specific_terms)
            has_context = any(term in question for term in context_specific_terms)
            has_vague = any(term in question_words for term in vague_terms if term in {'it', 'this', 'that'} or term in question_words[:-1])
            has_product_name = any(name in question for name in product_names)

            if question.startswith('how'):
                intent = 'setup' if has_product else 'vague'
            elif question.startswith(('why', 'what')):
                intent = 'troubleshooting' if has_error else 'vague'
            else:
                intent = 'troubleshooting' if has_error else 'setup' if has_product else 'vague'

            if ((intent == 'troubleshooting' or intent == 'setup') and
                    has_product_name and
                    not has_time and
                    not has_context and
                    not (has_vague and not (has_error or has_product))):
                ai_response = await self._fallback_to_gpt(last_message_content, ticket_id)
                if (not ai_response or
                        any(phrase in ai_response.lower() for phrase in ["i don't have", "i can't", "could be", "might be", "not sure"]) or
                        not self.score_response(ai_response, question)):
                    ai_response = "I am sorry to inform you that I cannot help you with this issue, please try forming your question differently or wait to receive help from the staff team."
                    resolution_source = "staff"
                else:
                    resolution_source = "gpt"
            else:
                reason = ("time-specific" if has_time else
                          "context-specific" if has_context else
                          "vague" if intent == 'vague' else
                          "no clear product/error")
                if intent == 'vague' or has_context:
                    await self._request_clarification(channel, ticket_id, question)
                    return
                logger.info(f"Skipping web search due to {reason} question: {question}")
                ai_response = "I am sorry to inform you that I cannot help you with this issue, please try forming your question differently or wait to receive help from the staff team."
                resolution_source = "staff"

        # Save the suggestion with the final response linked to the message_id
        suggestion = {
            "ai_response": ai_response,
            "timestamp": datetime.datetime.utcnow(),
            "rejected": False,
            "message_id": str(msg.id),
            "resolution_source": resolution_source,
            "message_ref_id": message_id  # Reference to the specific customer message
        }
        try:
            doc_ref.update({
                "suggestions": firestore.ArrayUnion([suggestion])
            })
            logger.info(f"Suggestion saved for ticket {ticket_id} with message_id {msg.id}, linked to message_ref_id {message_id}, response: {ai_response}")
        except Exception as e:
            logger.error(f"Failed to save suggestion for ticket {ticket_id}: {e}")
            return

        # Update the embed with the AI response, splitting if necessary
        response_chunks = [ai_response[i:i + EMBED_FIELD_LIMIT] for i in range(0, len(ai_response), EMBED_FIELD_LIMIT)]
        embed.clear_fields()
        for i, chunk in enumerate(response_chunks):
            embed.add_field(
                name="📝 Response" if i == 0 else f"📝 Response (Part {i + 1})",
                value=chunk,
                inline=False
            )

        await msg.edit(embed=embed)
        await msg.add_reaction("👍")  # Add thumbs up for approval
        await msg.add_reaction("👎")  # Add thumbs down for rejection

    # Poll OpenAI Assistant for a response with a timeout
    async def _poll_ai_response(self, prior_context, last_message, ticket_id):
        try:
            thread = self.client.beta.threads.create()
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=(
                    f"Prior conversation context (for understanding only, do not reference unless explicitly asked):\n{prior_context}\n\n"
                    f"Latest message (respond to this):\n{last_message}\n\n"
                    f"Guidelines: Check your vector storage files (`suspectbot_commands.json`, `game_product_setup_guide.json`, and product-specific files like `apex_lite_setup_guide.json` and `apex_lite_errors.json`) first. "
                    f"For general setup requests (e.g., 'how do I set up Apex Lite'), return only the command (e.g., 'You can use the command `/apexlite` to get the guide.'). "
                    f"For specific questions (e.g., 'Why does Apex Lite crash?'), use the relevant guide or error file to form a concise, tailored response. "
                    f"If you cannot provide a helpful response based strictly on these files, return 'NO_ANSWER'. Do NOT include file names or full guide contents unless specifically asked."
                )
            )
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant_id
            )

            start_time = time.time()
            max_wait = 15  # 15-second timeout
            while time.time() - start_time < max_wait:
                run_status = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run_status.status in ["completed", "failed"]:
                    break
                await asyncio.sleep(0.5)

            if run_status.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                for message in messages.data:
                    if message.role == "assistant":
                        response = message.content[0].text.value
                        return response if response.strip() else None
            elif run_status.status == "failed":
                logger.error(f"Assistant run failed for ticket {ticket_id}: {run_status.last_error}")
            else:
                logger.info(f"AI response exceeded 15 seconds for ticket {ticket_id}")
            return None
        except Exception as e:
            logger.error(f"Error polling AI response for ticket {ticket_id}: {e}")
            return None

    # Fallback to GPT-4o-mini for error or product-related questions
    async def _fallback_to_gpt(self, last_message, ticket_id):
        try:
            question = last_message.split(': ', 1)[1]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful support assistant for gaming products. Provide a concise, accurate answer based on general knowledge for error or product-related questions. Do not invent information or speculate."},
                    {"role": "user", "content": f"Customer question: {question}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error in GPT-4o-mini fallback for ticket {ticket_id}: {e}")
            return None

# Setup function to register the AIAssistant cog with the bot
async def setup(bot):
    await bot.add_cog(AIAssistant(bot))  # Add the AIAssistant cog to the bot instance