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

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_TICKETS = 250

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tickets = {}
        self.assistant_id = "asst_kMPncHzly9M28mIQtCLe102e"  # Replace with your Assistant ID

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
        """ Ensure the tickets collection stays under MAX_TICKETS by removing the oldest ones based on created_at. """
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
            print(f"Ticket count reduced to {MAX_TICKETS}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.category_id not in CATEGORY_IDS:
            return

        ticket_id = str(message.channel.id)
        user_id = str(message.author.id)

        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()

        new_ticket = not doc.exists
        if doc.exists:
            ticket_data = doc.to_dict()
            ticket_data["messages"].append({
                "user_id": user_id,
                "content": message.content,
                "timestamp": datetime.datetime.utcnow()
            })
            doc_ref.update({"messages": ticket_data["messages"]})
        else:
            doc_ref.set({
                "ticket_id": ticket_id,
                "created_at": datetime.datetime.utcnow(),
                "messages": [{
                    "user_id": user_id,
                    "content": message.content,
                    "timestamp": datetime.datetime.utcnow()
                }]
            })
            self.active_tickets[ticket_id] = True
            print(f"New ticket created and cached: {ticket_id}")

        if new_ticket:
            await self.enforce_ticket_limit()

        await self.check_for_suggestions(message.channel, ticket_id)

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
                description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been approved and saved for future learning!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
            await reaction.message.channel.send(embed=embed, delete_after=5)
        elif reaction.emoji == "👎":
            print(f"❌ Rejecting AI response for ticket {ticket_id}")
            doc_list[0].reference.update({"rejected": True})
            embed = discord.Embed(
                title="❌ AI Response Rejected",
                description=f"{user.mention}, the AI suggestion for ticket `{ticket_id}` has been rejected. The bot will refine its approach.",
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

        last_message = messages[-1]["content"]
        prior_context = "\n".join([f"User {m['user_id']}: {m['content']}" for m in messages[:-1][-9:]])

        ai_response = await self.generate_ai_response(prior_context, last_message)
        if ai_response:
            doc_ref = db.collection("ai_suggestions").document()
            suggestion_data = {
                "ticket_id": ticket_id,
                "ai_response": ai_response,
                "timestamp": datetime.datetime.utcnow(),
                "rejected": False
            }
            doc_ref.set(suggestion_data)

            embed = discord.Embed(
                title="🤖 AI Suggestion",
                description=f"For ticket `{channel.name}`:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📝 Response",
                value=ai_response,
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • AI Section", icon_url=self.bot.user.avatar.url)
            msg = await review_channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            doc_ref.update({"message_id": str(msg.id)})
        else:
            print(f"Skipping irrelevant message for ticket {ticket_id}: '{last_message}'")

    async def generate_ai_response(self, prior_context, last_message):
        """ Calls OpenAI Assistants API with minimal prompt, relying on trained Assistant. """
        try:
            client = openai.OpenAI()
            thread = client.beta.threads.create()
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=(
                    f"Prior conversation context (for understanding only, do not reference unless explicitly asked):\n{prior_context}\n\n"
                    f"Latest message (respond to this):\n{last_message}"
                )
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant_id
            )
            while run.status not in ["completed", "failed"]:
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                await asyncio.sleep(0.1)
            if run.status == "failed":
                print(f"Assistant run failed: {run.last_error}")
                return None
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    response = message.content[0].text.value
                    return response if response.strip() else None
            return None
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))