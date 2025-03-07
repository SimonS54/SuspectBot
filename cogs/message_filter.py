import discord
import asyncio
from discord.ext import commands
from discord.ui import Button, View
from config import LOG_CHANNEL_ID, FILTERED_CHANNEL_ID, ALLOWED_WORDS, ALLOWED_ROLE_IDS  # Import configuration constants

# Define a MessageFilter cog to monitor and filter messages in a specific channel
class MessageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in the cog

    # Custom view class for the "Restore" button
    class RestoreView(View):
        def __init__(self, original_message_content, original_author, original_channel):
            super().__init__(timeout=None)  # No timeout, so the button persists
            self.original_message_content = original_message_content
            self.original_author = original_author
            self.original_channel = original_channel

        @discord.ui.button(label="Restore Message", style=discord.ButtonStyle.green)
        async def restore_button(self, interaction: discord.Interaction, button: Button):
            # Check if the user has an allowed role
            if not any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
                await interaction.response.send_message("You don’t have permission to restore messages!", ephemeral=True)
                return

            # Repost the original message in the original channel
            await self.original_channel.send(f"{self.original_author.mention}: {self.original_message_content}")
            await interaction.response.send_message("Message restored successfully!", ephemeral=True)

            # Optionally, disable the button after use
            button.disabled = True
            await interaction.message.edit(view=self)

    # Listener to process every message sent in the server
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots to prevent self-triggering or processing other bot messages
        if message.author.bot:
            return

        # Skip filtering for users with allowed roles (e.g., staff or moderators)
        if any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            return

        # Get the log channel for recording deleted messages
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        filtered_channel = self.bot.get_channel(FILTERED_CHANNEL_ID)

        # Only filter messages in the designated filtered channel
        if message.channel.id == FILTERED_CHANNEL_ID:
            # Check if the message contains any allowed words (case-insensitive)
            allowed = any(word.lower() in message.content.lower() for word in ALLOWED_WORDS)
            # If no allowed words are found and the message isn’t from the bot itself
            if not allowed and message.author.id != self.bot.user.id:
                # Create an embed to log the deleted message in the log channel
                deleted_message_embed = discord.Embed(
                    title="🗑️ Deleted Message",
                    description=f"**User:** {message.author.mention}\n**Content:** {message.content}",
                    color=discord.Color.red()
                )
                deleted_message_embed.set_footer(text="Powered by SuspectServices • Filter Section", icon_url=self.bot.user.avatar.url)

                # Add the "Restore" button to the embed
                view = self.RestoreView(message.content, message.author, filtered_channel)
                await log_channel.send(embed=deleted_message_embed, view=view)

                # Create a temporary notification embed to inform the user
                notification_embed = discord.Embed(
                    title="❌ Message Removed",
                    description=f"{message.author.mention}, your message was deleted—it contained unallowed words.",
                    color=discord.Color.red()
                )
                notification_embed.set_footer(text="Powered by SuspectServices • Filter Section", icon_url=self.bot.user.avatar.url)
                notification_message = await message.channel.send(embed=notification_embed)
                await message.delete()  # Delete the original message
                await asyncio.sleep(5)  # Display the notification for 5 seconds
                await notification_message.delete()  # Clean up the notification

        # Ensure command processing continues after filtering
        await self.bot.process_commands(message)

# Setup function to register the MessageFilter cog with the bot
async def setup(bot):
    await bot.add_cog(MessageFilter(bot))  # Add the MessageFilter cog to the bot instance
