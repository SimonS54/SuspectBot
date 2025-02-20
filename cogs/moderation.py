import discord
from discord.ext import commands
from config import ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='announce')
    async def announce(self, ctx, *, message: str):
        """Sends an announcement message to the designated channel."""
        if ctx.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            return

        target_channel = self.bot.get_channel(ANNOUNCE_TARGET_CHANNEL_ID)
        if target_channel is None:
            await ctx.send("The target channel for announcements could not be found.")
            return

        await target_channel.send(message)

    @commands.command(name='update')
    async def update(self, ctx, *, message: str):
        """Sends an update message to the designated channel."""
        if ctx.channel.id != UPDATE_COMMAND_CHANNEL_ID:
            return

        target_channel = self.bot.get_channel(UPDATE_TARGET_CHANNEL_ID)
        if target_channel is None:
            await ctx.send("The target channel for updates could not be found.")
            return

        await target_channel.send(message)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
