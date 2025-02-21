import discord
import openai
import os
from dotenv import load_dotenv
from discord.ext import commands
from firebase_config import db
from firebase_admin import firestore
from config import CATEGORY_IDS, AI_REVIEW_CHANNEL_ID
import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define Discord commands for the AI to reference
COMMAND_LIST = {
    # [Your existing COMMAND_LIST remains unchanged]
    "/apexlite": "Get Guide for Apex Lite",
    "/apexkernaim": "Get Guide for Apex Kernaim",
    "/codkernaim": "Get Guide for COD Kernaim",
    "/codrutunlock": "Get Guide for COD RUT Unlock",
    "/codrutuav": "Get Guide for COD RUT UAV",
    "/eftexoarena": "Get Guide for EFT Exo Arena",
    "/eftexo": "Get Guide for EFT Exo",
    "/eftnextfull": "Get Guide for EFT Nextcheat Full",
    "/eftnextlite": "Get Guide for EFT Nextcheat Lite",
    "/fivemhx": "Get Guide for FiveM HX",
    "/fivemtzext": "Get Guide for FiveM TZ External",
    "/fivemtzint": "Get Guide for FiveM TZ Internal",
    "/fndcext": "Get Guide for FN Disconnect External",
    "/hwidexception": "Get Guide for Exception Spoofer",
    "/marvelklar": "Get Guide for Marvel Rivals Klar",
    "/r6ring": "Get Guide for R6 Ring1",
    "/rustfluent": "Get Guide for Rust Fluent",
    "/rustmatrix": "Get Guide for Rust Matrix",
    "/rustdcext": "Get Guide for Rust Disconnect External",
    "/rustrecoil": "Get Guide for Rust Recoil Script",
    "/supporttool": "Get the support tool",
    "/anydesk": "Get the AnyDesk tool",
    "/virtualization": "Get the Virtualization Guide",
    "/tpm": "Get the TPM Guide",
    "/secureboot": "Get the Secure Boot Guide",
    "/coreisolation": "Get the Core Isolation Guide",
    "/vc64": "Get the Visual C++ redistributables",
    "/epvp": "Get Elitepvpers vouch list",
    "/epvptrade": "Get Instructions for a trade review",
    "/dat": "Payment instructions for Dat",
    "/paradox": "Payment instructions for Paradox",
    "/announce": "Send an announcement",
    "/update": "Send an update",
    "/productupdate": "Update a product status",
    "/review": "Leave a review",
    "/bothelp": "Shows this list",
    "/stats": "Retrieve ticket stats of the support team"
}

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tickets = {}  # In-memory cache of ticket IDs

    async def cog_load(self):
        """ Called when the cog is loaded; initialize existing tickets from Firestore. """
        print("Initializing AIAssistant with existing tickets...")
        tickets_ref = db.collection("tickets")
        tickets = tickets_ref.stream()
        for ticket in tickets:
            ticket_id = ticket.id
            self.active_tickets[ticket_id] = True
            print(f"Loaded ticket: {ticket_id}")
        print(f"Initialized with {len(self.active_tickets)} tickets.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # Ignore bot messages
            return

        if message.channel.category_id not in CATEGORY_IDS:  # Only process messages in ticket categories
            return

        ticket_id = str(message.channel.id)
        user_id = str(message.author.id)

        # Store conversation in Firestore
        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()

        if doc.exists:
            ticket_data = doc.to_dict()
            ticket_data["messages"].append({
                "user_id": user_id,
                "content": message.content,
                "timestamp": datetime.datetime.utcnow()
            })
            doc_ref.update({"messages": ticket_data["messages"]})
        else:
            # New ticket detected
            doc_ref.set({
                "ticket_id": ticket_id,
                "messages": [{
                    "user_id": user_id,
                    "content": message.content,
                    "timestamp": datetime.datetime.utcnow()
                }]
            })
            self.active_tickets[ticket_id] = True  # Add to in-memory cache
            print(f"New ticket created and cached: {ticket_id}")

        # Trigger AI suggestion immediately for this message
        await self.check_for_suggestions(message.channel, ticket_id)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Handles staff feedback on AI suggestions. """
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
            await reaction.message.channel.send(f"{user.mention} ✅ AI response approved and saved for future learning!", delete_after=5)

        elif reaction.emoji == "👎":
            print(f"❌ Rejecting AI response for ticket {ticket_id}")
            doc_list[0].reference.update({"rejected": True})
            await reaction.message.channel.send(f"{user.mention} ❌ AI response rejected. The bot will learn from this.", delete_after=5)

    async def check_for_suggestions(self, channel, ticket_id):
        """ Generate AI response based on stored conversation. """
        review_channel = self.bot.get_channel(AI_REVIEW_CHANNEL_ID)

        # Retrieve conversation history
        doc_ref = db.collection("tickets").document(ticket_id)
        doc = doc_ref.get()
        if not doc.exists:
            print(f"Ticket {ticket_id} not found in Firestore.")
            return

        messages = doc.to_dict().get("messages", [])
        if len(messages) < 1:  # Relaxed from 3 to 1 so it triggers on first message
            print(f"Ticket {ticket_id} has no messages yet.")
            return

        # Separate the last message and prior context
        last_message = messages[-1]["content"]
        prior_context = "\n".join([f"User {m['user_id']}: {m['content']}" for m in messages[:-1][-9:]])

        # Generate AI response
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
                description=f"Suggested response for `{channel.name}`:\n\n{ai_response}",
                color=discord.Color.blue()
            )
            msg = await review_channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            doc_ref.update({"message_id": str(msg.id)})

    async def generate_ai_response(self, prior_context, last_message):
        """ Calls OpenAI API to generate a response based on the last message with prior context. """
        try:
            client = openai.OpenAI()
            command_info = "The assistant can suggest the following commands when relevant:\n" + "\n".join(
                [f"{cmd}: {desc}" for cmd, desc in COMMAND_LIST.items()]
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful support assistant that provides information to customers on how to fix their issues with our products. "
                            "Your task is to respond ONLY to the most recent message provided below, using the prior conversation history as context to understand the situation. "
                            "Do not address or reference earlier messages in your response unless they are directly relevant to answering the latest message. "
                            "When the latest message relates to a specific product, tool, or process, suggest the appropriate Discord command from the list below if applicable. "
                            "Format your suggestion as: 'You can use the command `/command` to [description].' "
                            f"Available commands:\n{command_info}"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Prior conversation context:\n{prior_context}\n\nLatest message:\n{last_message}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))