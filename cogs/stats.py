import discord
from discord import app_commands
from discord.ext import commands
from firebase_config import db
from firebase_admin import firestore
from config import CATEGORY_IDS, ALLOWED_ROLE_IDS
from datetime import datetime, timedelta

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Listen for messages in the ticket category.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            return

        # Check if the message is in a ticket channel.
        if message.channel.category_id in CATEGORY_IDS:
            user_id = str(message.author.id)
            ticket_id = str(message.channel.id)
            doc_ref = db.collection("user_stats").document(user_id)
            doc = doc_ref.get()
            now = datetime.utcnow()
            expiration_time = now - timedelta(days=3)

            if doc.exists:
                data = doc.to_dict()
                handled_tickets = [
                    t for t in data.get("handled_tickets", [])
                    if t["timestamp"].replace(tzinfo=None) > expiration_time
                ]

                if any(t["ticket_id"] == ticket_id for t in handled_tickets):
                    return

                # Update the user's stats.
                handled_tickets.append({"ticket_id": ticket_id, "timestamp": now})
                doc_ref.update({
                    "tickets_handled": firestore.Increment(1),
                    "daily": firestore.Increment(1),
                    "weekly": firestore.Increment(1),
                    "monthly": firestore.Increment(1),
                    "handled_tickets": handled_tickets,
                    "last_updated": now
                })
            else:
                doc_ref.set({
                    "user_id": user_id,
                    "tickets_handled": 1,
                    "daily": 1,
                    "weekly": 1,
                    "monthly": 1,
                    "handled_tickets": [{"ticket_id": ticket_id, "timestamp": now}],
                    "last_updated": now
                })

    # Command to view stats of a specific user.
    @app_commands.command(name="stats", description="View stats of a specific user.")
    async def stats(self, interaction: discord.Interaction, member: discord.Member = None):
        if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
            return

        user = member if member else interaction.user
        user_id = str(user.id)
        doc_ref = db.collection("user_stats").document(user_id)
        doc = doc_ref.get()

        # Check if the user has stats.
        if doc.exists:
            data = doc.to_dict()
            embed = discord.Embed(
                title=f"📊 User Statistics",
                description=f"Statistics for {user.mention}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.add_field(name="📅 **Daily**", value=f"`{data.get('daily', 0)}` tickets handled", inline=True)
            embed.add_field(name="📆 **Weekly**", value=f"`{data.get('weekly', 0)}` tickets handled", inline=True)
            embed.add_field(name="📅 **Monthly**", value=f"`{data.get('monthly', 0)}` tickets handled", inline=True)
            embed.add_field(name="🏆 **All-Time**", value=f"`{data.get('tickets_handled', 0)}` tickets handled", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("❌ No stats found for this user.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Stats(bot))
