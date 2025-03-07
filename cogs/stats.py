import discord
from discord import app_commands
from discord.ext import commands
from firebase_config import db  # Firestore database instance
from firebase_admin import firestore
from config import CATEGORY_IDS, ALLOWED_ROLE_IDS  # Configuration constants
from datetime import datetime, timedelta, timezone  # Added timezone for UTC-aware datetimes
import asyncio

# Define a Stats cog to track and manage staff ticket-handling statistics
class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in the cog
        # Start the background task to clean up old tickets
        self.bot.loop.create_task(self.cleanup_old_tickets_task())

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
        now = datetime.now(timezone.utc)  # Current UTC timestamp, timezone-aware

        # Create a ticket entry with ticket ID and timestamp
        ticket_entry = {
            "ticket_id": ticket_id,
            "timestamp": now
        }

        if doc.exists:
            data = doc.to_dict()
            tickets = data.get("tickets", [])  # Get existing tickets or empty list
            ticket_ids = {t["ticket_id"] for t in tickets}  # Use set for efficient duplicate check

            # Skip if this ticket has already been counted for the user
            if ticket_id not in ticket_ids:
                tickets.append(ticket_entry)  # Add new ticket entry
                # Update Firestore with new ticket and increment total
                doc_ref.update({
                    "tickets": tickets,
                    "total_tickets": firestore.Increment(1),
                    "last_updated": now
                })
        else:
            # Create a new document for the user if none exists
            doc_ref.set({
                "user_id": user_id,
                "total_tickets": 1,
                "tickets": [ticket_entry],
                "last_updated": now
            })

    # Helper method to calculate rolling stats based on ticket timestamps
    def calculate_stats(self, tickets):
        """Calculate rolling stats based on ticket timestamps."""
        now = datetime.now(timezone.utc)  # Use UTC-aware datetime for consistency with Firestore
        stats = {
            "daily_tickets": 0,
            "weekly_tickets": 0,
            "monthly_tickets": 0
        }

        # Count tickets within each time window
        for ticket in tickets:
            ticket_time = ticket["timestamp"]  # Firestore returns UTC-aware timestamps
            age = now - ticket_time  # Both are now UTC-aware, subtraction works

            if age <= timedelta(hours=24):
                stats["daily_tickets"] += 1
            if age <= timedelta(days=7):
                stats["weekly_tickets"] += 1
            if age <= timedelta(days=30):
                stats["monthly_tickets"] += 1

        return stats

    # Background task to periodically clean up tickets older than 30 days
    async def cleanup_old_tickets_task(self):
        """Periodically remove tickets older than 30 days to manage Firestore storage."""
        while True:
            now = datetime.now(timezone.utc)  # UTC-aware timestamp for cleanup
            # Run cleanup every 24 hours
            await asyncio.sleep(24 * 60 * 60)  # Sleep for 24 hours

            docs = db.collection("user_stats").stream()  # Stream all user stats documents
            for doc in docs:
                doc_ref = db.collection("user_stats").document(doc.id)
                data = doc.to_dict()
                tickets = data.get("tickets", [])

                # Filter out tickets older than 30 days
                updated_tickets = [t for t in tickets if (now - t["timestamp"]) <= timedelta(days=30)]

                # Only update Firestore if tickets were removed
                if len(updated_tickets) < len(tickets):
                    doc_ref.update({
                        "tickets": updated_tickets,
                        "last_updated": now
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
            tickets = data.get("tickets", [])  # Get list of ticket entries
            total_tickets = data.get("total_tickets", 0)  # Get all-time total
            stats = self.calculate_stats(tickets)  # Calculate rolling stats

            # Create an embed to display the user’s stats
            embed = discord.Embed(
                title="📊 Staff Performance Stats",
                description=f"Ticket handling stats for {user.mention}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            embed.add_field(
                name="📅 Daily Tickets (Last 24h)",
                value=f"`{stats['daily_tickets']}` handled",
                inline=True
            )
            embed.add_field(
                name="📆 Weekly Tickets (Last 7d)",
                value=f"`{stats['weekly_tickets']}` handled",
                inline=True
            )
            embed.add_field(
                name="📅 Monthly Tickets (Last 30d)",
                value=f"`{stats['monthly_tickets']}` handled",
                inline=True
            )
            embed.add_field(
                name="🏆 All-Time Total",
                value=f"`{total_tickets}` handled",
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