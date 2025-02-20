import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bothelp", description="Shows a commands list.")
    async def bothelp(self, interaction: discord.Interaction):
        """Displays a list of available bot commands."""
        embed = discord.Embed(
            title="Commands List",
            description="""Here are the available commands:
            **Support:**
            /supporttool - Get the support tool
            /anydesk - Instructions for remote support
            /virt - Enable/Disable virtualization
            /tpm - Enable/Disable TPM
            /coreisolation - Disable core isolation
            /secureboot - Enable/Disable Secure Boot
            /vc64 - Install Visual C++ dependencies

            **Elitepvpers:**
            /epvp - Elitepvpers vouch list
            /epvptrade - Instructions for a trade review

            **General:**
            /review - Leave a review
            /checkrole [role_name] - Check if you have a role
            """,
            color=discord.Color.blue()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="checkrole", description="Checks if the user has a specific role.")
    async def check_role(self, interaction: discord.Interaction, role_name: str):
        """Checks whether the user has a given role."""
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role in interaction.user.roles:
            embed = discord.Embed(
                title="Role Check",
                description=f"You have the `{role.name}` role.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Role Check",
                description=f"You don't have the `{role_name}` role.",
                color=discord.Color.red()
            )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
