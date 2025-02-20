import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Payment instructions for using Dat as your MM.
    @app_commands.command(name="dat", description="Payment instruction for MM.")
    async def dat(self, interaction: discord.Interaction, amount: str):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Dat MM Payment",
                description="Thank you for choosing <@383435302527696896> as your MM.\n\n"
                            f"Please send {amount}USD to [Dat](https://paypal.me/ChrisColindres01), make sure that your sending as **Friends&Family** and that you are sending the correct currency -> **USD**.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Payment instructions for using Paradox as your MM.
    @app_commands.command(name="paradox", description="Payment instruction for MM.")
    async def paradox(self, interaction: discord.Interaction, amount: str):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Paradox MM Payment",
                description="Thank you for choosing <@368435292916416512> as your MM.\n\n"
                            f"Please send {amount}CHF to [Paradox](https://paypal.me/zeemonzh), make sure that your sending as **Friends&Family** and that you are sending the correct currency -> **CHF**.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Payment(bot))
