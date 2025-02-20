import discord
from discord import app_commands
from discord.ext import commands

staff_stats = {}  # This will be loaded from a file

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Displays the current staff stats.")
    async def stats(self, interaction: discord.Interaction):
        """Displays statistics of staff members."""
        if not staff_stats:
            await interaction.response.send_message("No stats available.")
            return

        sorted_stats = sorted(staff_stats.items(), key=lambda x: x[1]['tickets_handled'], reverse=True)
        embed = discord.Embed(title="Staff Stats Leaderboard", color=discord.Color.red())

        for rank, (staff_id, stats) in enumerate(sorted_stats, start=1):
            staff_member = interaction.guild.get_member(int(staff_id))
            if staff_member:
                embed.add_field(
                    name=f"{rank}. {staff_member.display_name}",
                    value=f"Tickets Handled: {stats['tickets_handled']}",
                    inline=False
                )

        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
