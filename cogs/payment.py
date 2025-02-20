import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="heaven", description="Payment instruction for MM.")
    async def heaven(self, interaction: discord.Interaction, amount: str):
        """Payment details for 9heaven."""
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            await interaction.response.send_message(
                f"Thank you for choosing <@1232181386090123297> as your MM. "
                f"Please send {amount} EUR to https://www.paypal.com/paypalme/chrivvs f&f."
            )
        else:
            await interaction.response.send_message("You don't have permission to use this command.")

    @app_commands.command(name="9k", description="Payment instruction for MM.")
    async def nine_k(self, interaction: discord.Interaction, amount: str):
        """Payment details for 9k."""
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            await interaction.response.send_message(
                f"Thank you for choosing <@397469006946238476> as your MM. "
                f"Please send {amount} EUR to https://paypal.me/9kuk f&f."
            )
        else:
            await interaction.response.send_message("You don't have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Payment(bot))
