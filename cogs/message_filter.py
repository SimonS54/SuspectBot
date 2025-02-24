import discord
import asyncio
from discord.ext import commands
from config import LOG_CHANNEL_ID, FILTERED_CHANNEL_ID, ALLOWED_WORDS, ALLOWED_ROLE_IDS

class MessageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            return

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if message.channel.id == FILTERED_CHANNEL_ID:
            allowed = any(word.lower() in message.content.lower() for word in ALLOWED_WORDS)
            if not allowed and message.author.id != self.bot.user.id:
                # Log the deleted message
                deleted_message_embed = discord.Embed(
                    title="🗑️ Deleted Message",
                    description=f"**User:** {message.author.mention}\n**Content:** {message.content}",
                    color=discord.Color.red()
                )
                deleted_message_embed.set_footer(text="Powered by SuspectServices • Filter Section", icon_url=self.bot.user.avatar.url)
                await log_channel.send(embed=deleted_message_embed)

                # Notify the user with a temporary, dismissible message
                notification_embed = discord.Embed(
                    title="❌ Message Removed",
                    description=f"{message.author.mention}, your message was deleted—it it contained not allowed words.",
                    color=discord.Color.red()
                )
                notification_embed.set_footer(text="Powered by SuspectServices • Filter Section", icon_url=self.bot.user.avatar.url)
                notification_message = await message.channel.send(embed=notification_embed)
                await message.delete()
                await asyncio.sleep(5)  # Show for 5 seconds, then delete
                await notification_message.delete()

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(MessageFilter(bot))