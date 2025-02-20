import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class Documentation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nextcheat", description="Sends the link to the NextCheat documentation.")
    async def nextcheat(self, interaction: discord.Interaction):
        """Provides a link to NextCheat documentation."""
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="NextCheat",
                description=f"[NextCheat Documentation](https://suspectservices.gitbook.io/nextcheat/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You don't have permission to use this command.")

    @app_commands.command(name="rustexternal", description="Sends the link to the Rust External documentation.")
    async def rustexternal(self, interaction: discord.Interaction):
        """Provides a link to Rust External documentation."""
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Rust External",
                description=f"[Rust External Documentation](https://suspectservices.gitbook.io/rust-external/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You don't have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Documentation(bot))
