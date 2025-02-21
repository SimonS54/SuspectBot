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

        # Exclude users with ALLOWED_ROLE_IDS from filtering
        if any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            return

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)

        # Filter messages in the FILTERED_CHANNEL_ID
        if message.channel.id == FILTERED_CHANNEL_ID:
            allowed = any(word.lower() in message.content.lower() for word in ALLOWED_WORDS)
            if not allowed:
                if message.author.id != self.bot.user.id:
                    deleted_message_embed = discord.Embed(
                        title="Deleted Message",
                        description=f"Message from {message.author.name} ({message.author.id}): {message.content}",
                        color=discord.Color.red()
                    )
                    deleted_message_embed.set_footer(text="Powered by SuspectServices")
                    await log_channel.send(embed=deleted_message_embed)

                    notification_embed = discord.Embed(
                        title="Message Deleted",
                        description=f"{message.author.mention}, your message was deleted because it didn't contain any of the allowed words.",
                        color=discord.Color.red()
                    )
                    notification_embed.set_footer(text="Powered by SuspectServices")
                    notification_message = await message.channel.send(embed=notification_embed)
                    await message.delete()
                    await asyncio.sleep(2)
                    await notification_message.delete(delay=3)

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(MessageFilter(bot))
