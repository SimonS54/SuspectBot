import discord
import openai
import os
from dotenv import load_dotenv
from discord.ext import commands
from firebase_config import db
from firebase_admin import firestore
from config import CATEGORY_IDS, AI_REVIEW_CHANNEL_ID
import datetime
import asyncio
from Levenshtein import distance as levenshtein_distance
import re
import time
from googlesearch import search  # Requires `pip install google`

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_TICKETS = 50
STAFF_ROLE_IDS = {1297999380745420822, 1297999355860615209, 1297999091187581020}
NOTIFY_USER_ID = 368435292916416512
EMBED_FIELD_LIMIT = 1000  # Discord embed field character limit

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tickets = {}
        self.assistant_id = "asst_kMPncHzly9M28mIQtCLe102e"
        self.client = openai.OpenAI()

    async def cog_load(self):
        print("Initializing AIAssistant with existing tickets...")
        tickets_ref = db.collection("tickets")
        tickets = tickets_ref.stream()
        for ticket in tickets:
            ticket_id = ticket.id
            self.active_tickets[ticket_id] = True
            print(f"Loaded ticket: {ticket_id}")
        print(f"Initialized with {len(self.active_tickets)} tickets.")

    async def enforce_ticket_limit(self):
        """ Ensure the tickets collection stays under MAX_TICKETS by removing the oldest ones. """
        tickets_ref = db.collection("tickets")
        tickets = list(tickets_ref.order_by("created_at").stream())
        if len(tickets) > MAX_TICKETS:
            tickets_to_remove = tickets[:len(tickets) - MAX_TICKETS]
            for ticket in tickets_to_remove:
                ticket_id = ticket.id
                ticket.reference.delete()
                if ticket_id in self.active_tickets:
                    del self.active_tickets[ticket_id]
                print(f"Removed old ticket: {ticket_id}")
            print(f"Ticket count reduced to {MAX_TICKETS}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.category_id not in CATEGORY_IDS:
            return

        ticket_id = str(message.channel.id)
        user_id = str(message.author.id)
        is_staff = any(role.id in STAFF_ROLE_IDS for role in message.author.roles) if isinstance(message.author, discord.Member) else False
        role = "staff" if is_staff else "customer"

        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()

        new_ticket = not doc.exists
        if doc.exists:
            ticket_data = doc.to_dict()
            ticket_data["messages"].append({
                "user_id": user_id,
                "content": message.content,
                "timestamp": datetime.datetime.utcnow(),
                "role": role
            })
            doc_ref.update({"messages": ticket_data["messages"]})
        else:
            doc_ref.set({
                "ticket_id": ticket_id,
                "created_at": datetime.datetime.utcnow(),
                "messages": [{
                    "user_id": user_id,
                    "content": message.content,
                    "timestamp": datetime.datetime.utcnow(),
                    "role": role
                }],
                "closed": False
            })
            self.active_tickets[ticket_id] = True
            print(f"New ticket created and cached: {ticket_id}")

        if new_ticket:
            await self.enforce_ticket_limit()

        await self.check_for_suggestions(message.channel, ticket_id)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        ticket_id = str(payload.channel_id)
        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()
        if doc.exists and payload.channel_id in [int(t) for t in self.active_tickets.keys()]:
            ticket_data = doc.to_dict()
            if not ticket_data.get("closed", False):
                ticket_data["closed"] = True
                doc_ref.update({"closed": True})
                print(f"Ticket {ticket_id} marked as closed.")
                user = self.bot.get_user(NOTIFY_USER_ID)
                if user:
                    ticket_count = len(list(db.collection("tickets").where("closed", "==", True).stream()))
                    await user.send(f"Ticket {ticket_id} is closed. {ticket_count}/50 tickets collected for fine-tuning.")
                    if ticket_count >= 50:
                        await user.send("🎉 50 tickets collected! Ready for fine-tuning.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        print(f"✅ Reaction detected: {reaction.emoji} from {user.name}")
        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)
        if reaction.message.channel.id != review_channel.id:
            print("❌ Reaction not in AI review channel")
            return

        doc_ref = db.collection("ai_suggestions").where(filter=firestore.FieldFilter("message_id", "==", str(reaction.message.id))).limit(1)
        docs = doc_ref.stream()
        doc_list = list(docs)

        if not doc_list:
            print("❌ No Firestore document found for this message.")
            return

        suggestion_data = doc_list[0].to_dict()
        ticket_id = suggestion_data["ticket_id"]
        ai_response = suggestion_data["ai_response"]

        if reaction.emoji == "👍":
            print(f"✅ Approving AI response for ticket {ticket_id}")
            approved_ref = db.collection("approved_responses").document(ticket_id)
            approved_ref.set({"responses": firestore.ArrayUnion([ai_response])}, merge=True)
            embed = discord.Embed(
                title="✅ AI Response Approved",
                description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been approved and saved!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
            await reaction.message.channel.send(embed=embed, delete_after=5)
        elif reaction.emoji == "👎":
            print(f"❌ Rejecting AI response for ticket {ticket_id}")
            doc_list[0].reference.update({"rejected": True})
            embed = discord.Embed(
                title="❌ AI Response Rejected",
                description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been rejected.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
            await reaction.message.channel.send(embed=embed, delete_after=5)

    async def check_for_suggestions(self, channel, ticket_id):
        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)
        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()
        if not doc.exists:
            print(f"Ticket {ticket_id} not found in Firestore.")
            return

        messages = doc.to_dict().get("messages", [])
        if len(messages) < 1:
            print(f"Ticket {ticket_id} has no messages yet.")
            return

        last_message = messages[-1]
        if last_message["role"] != "customer":
            print(f"Skipping staff message in ticket {ticket_id}: '{last_message['content']}'")
            return

        approved_ref = db.collection("approved_responses").document(ticket_id)
        approved_doc = approved_ref.get()
        if approved_doc.exists:
            approved_responses = approved_doc.to_dict().get("responses", [])
            last_msg_text = last_message["content"].lower()
            for resp in approved_responses:
                resp_lower = resp.lower()
                similarity = levenshtein_distance(last_msg_text, resp_lower)
                if similarity <= min(len(last_msg_text), len(resp_lower)) * 0.2:
                    print(f"Using approved response for ticket {ticket_id} (similarity: {similarity})")
                    return resp

        prior_context = "\n".join([f"{m['role'].capitalize()} {m['user_id']}: {m['content']}" for m in messages[:-1][-9:]])
        last_message_content = f"Customer {last_message['user_id']}: {last_message['content']}"

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
        suggestion_doc_ref = db.collection("ai_suggestions").document()
        suggestion_doc_ref.set({
            "ticket_id": ticket_id,
            "ai_response": "Processing...",
            "timestamp": datetime.datetime.utcnow(),
            "rejected": False,
            "message_id": str(msg.id)
        })

        ai_response = await self._poll_ai_response(prior_context, last_message_content, ticket_id)
        if ai_response:
            ai_response = re.sub(r"【.*†source】", "", ai_response).strip()
            if "NO_ANSWER" in ai_response:
                # Try web search as fallback
                ai_response = await self._search_web(last_message_content, ticket_id)
                if not ai_response:
                    ai_response = "Please wait for assistance from the staff team."
        else:
            ai_response = await self._search_web(last_message_content, ticket_id)
            if not ai_response:
                ai_response = "Please wait for assistance from the staff team."

        # Split response into chunks if over 1024 chars
        response_chunks = [ai_response[i:i + EMBED_FIELD_LIMIT] for i in range(0, len(ai_response), EMBED_FIELD_LIMIT)]
        embed.clear_fields()
        for i, chunk in enumerate(response_chunks):
            embed.add_field(
                name="📝 Response" if i == 0 else f"📝 Response (Part {i + 1})",
                value=chunk,
                inline=False
            )

        suggestion_doc_ref.update({"ai_response": ai_response})
        await msg.edit(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    async def _poll_ai_response(self, prior_context, last_message, ticket_id):
        """ Asynchronously poll the Assistants API for a response. """
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
            max_wait = 15
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
                print(f"Assistant run failed for ticket {ticket_id}: {run_status.last_error}")
            else:
                print(f"AI response exceeded 15 seconds for ticket {ticket_id}")
            return None
        except Exception as e:
            print(f"Error polling AI response for ticket {ticket_id}: {e}")
            return None

    async def _search_web(self, query, ticket_id):
        """ Search the web for a solution if vector storage fails. """
        try:
            search_query = f"{query} Windows troubleshooting steps recent results"
            results = []
            for result in search(search_query, num_results=3, stop=3):
                results.append(result)
            if results:
                response = (
                    "I couldn’t find a specific solution in my trained data, but based on a web search, here’s a general troubleshooting tip: "
                    "Check for recent Windows troubleshooting guides online. For example, try updating your system or running 'sfc /scannow' in Command Prompt as an administrator. "
                    "If this doesn’t help, please wait for staff assistance."
                )
                return response[:EMBED_FIELD_LIMIT]  # Cap at 1024 for safety
            return None
        except Exception as e:
            print(f"Error searching web for ticket {ticket_id}: {e}")
            return None

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))