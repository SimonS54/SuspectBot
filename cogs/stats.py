import discord
from discord import app_commands
from discord.ext import commands
from firebase_config import db  # Firestore database instance
from firebase_admin import firestore
from config import CATEGORY_IDS, ALLOWED_ROLE_IDS  # Configuration constants
from datetime import datetime, timedelta
import asyncio

# Define a Stats cog to track and manage staff ticket-handling statistics
class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in the cog
        # Start the background task to reset counters when the cog is loaded
        self.bot.loop.create_task(self.reset_counters_task())

    # Listener to track messages in specified ticket categories
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots to prevent self-triggering
        if message.author.bot:
            return

        # Restrict tracking to users with allowed roles
        if not any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            return

        # Only track messages in designated ticket categories
        if message.channel.category_id not in CATEGORY_IDS:
            return

        user_id = str(message.author.id)  # Convert user ID to string for Firestore
        ticket_id = str(message.channel.id)  # Convert channel ID to string
        doc_ref = db.collection("user_stats").document(user_id)  # Reference to user’s stats document
        doc = doc_ref.get()  # Fetch the document if it exists
        now = datetime.utcnow()  # Current UTC timestamp

        if doc.exists:
            data = doc.to_dict()
            # Use a set to avoid duplicate ticket IDs
            handled_tickets = set(data.get("handled_ticket_ids", []))

            # Skip if this ticket has already been counted for the user
            if ticket_id in handled_tickets:
                return

            handled_tickets.add(ticket_id)  # Add new ticket ID
            # Increment all counters and update the ticket list
            doc_ref.update({
                "total_tickets": firestore.Increment(1),
                "daily_tickets": firestore.Increment(1),
                "weekly_tickets": firestore.Increment(1),
                "monthly_tickets": firestore.Increment(1),
                "handled_ticket_ids": list(handled_tickets),
                "last_updated": now
            })
        else:
            # Create a new document for the user if none exists
            doc_ref.set({
                "user_id": user_id,
                "total_tickets": 1,
                "daily_tickets": 1,
                "weekly_tickets": 1,
                "monthly_tickets": 1,
                "handled_ticket_ids": [ticket_id],
                "last_updated": now
            })

    # Background task to periodically reset daily, weekly, and monthly counters
    async def reset_counters_task(self):
        """Background task to reset daily, weekly, and monthly counters."""
        while True:
            now = datetime.utcnow()
            # Calculate time until next daily reset (midnight UTC)
            next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            await asyncio.sleep((next_day - now).total_seconds())
            await self.reset_counters("daily_tickets")

            # Calculate time until next weekly reset (Monday midnight UTC)
            days_until_monday = (7 - now.weekday()) % 7 or 7
            next_week = (now + timedelta(days=days_until_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            await asyncio.sleep((next_week - now).total_seconds())
            await self.reset_counters("weekly_tickets")

            # Calculate time until next monthly reset (1st of next month at midnight UTC)
            next_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            await asyncio.sleep((next_month - now).total_seconds())
            await self.reset_counters("monthly_tickets")

    # Helper method to reset a specified counter field for all users
    async def reset_counters(self, field_to_reset):
        """Reset the specified counter field for all users."""
        docs = db.collection("user_stats").stream()  # Stream all user stats documents
        for doc in docs:
            doc_ref = db.collection("user_stats").document(doc.id)
            # Reset the specified field to 0 and update the timestamp
            doc_ref.update({
                field_to_reset: 0,
                "last_updated": datetime.utcnow()
            })

    # Command to display ticket-handling stats for a user
    @app_commands.command(name="stats", description="View your ticket handling stats or someone else’s")
    async def stats(self, interaction: discord.Interaction, member: discord.Member = None):
        # Restrict command to users with allowed roles
        if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Stats Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Default to the command user if no member is specified
        user = member if member else interaction.user
        user_id = str(user.id)
        doc_ref = db.collection("user_stats").document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            # Create an embed to display the user’s stats
            embed = discord.Embed(
                title="📊 Staff Performance Stats",
                description=f"Ticket handling stats for {user.mention}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.add_field(
                name="📅 Daily Tickets",
                value=f"`{data.get('daily_tickets', 0)}` handled",
                inline=True
            )
            embed.add_field(
                name="📆 Weekly Tickets",
                value=f"`{data.get('weekly_tickets', 0)}` handled",
                inline=True
            )
            embed.add_field(
                name="📅 Monthly Tickets",
                value=f"`{data.get('monthly_tickets', 0)}` handled",
                inline=True
            )
            embed.add_field(
                name="🏆 All-Time Total",
                value=f"`{data.get('total_tickets', 0)}` handled",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Stats Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # Display a message if no stats are found for the user
            embed = discord.Embed(
                title="📉 No Stats Available",
                description=f"No ticket handling stats found for {user.mention}.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Stats Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

# Setup function to register the Stats cog with the bot
async def setup(bot):
    await bot.add_cog(Stats(bot))  # Add the Stats cog to the bot instance