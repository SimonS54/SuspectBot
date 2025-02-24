import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dat", description="Payment instructions for Dat as your Middleman")
    async def dat(self, interaction: discord.Interaction, amount: str):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="💸 Payment to Dat",
                description="Thanks for choosing <@383435302527696896> as your Middleman!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📤 Send Payment",
                value=f"Send **{amount} USD** to [Dat’s PayPal](https://paypal.me/ChrisColindres01)",
                inline=False
            )
            embed.add_field(
                name="⚠️ Important",
                value="- Use **Friends & Family**\n- Ensure currency is **USD**",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="paradox", description="Payment instructions for Paradox as your Middleman")
    async def paradox(self, interaction: discord.Interaction, amount: str):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="💸 Payment to Paradox",
                description="Thanks for choosing <@368435292916416512> as your Middleman!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📤 Send Payment",
                value=f"Send **{amount} CHF** to [Paradox’s PayPal](https://paypal.me/zeemonzh)",
                inline=False
            )
            embed.add_field(
                name="⚠️ Important",
                value="- Use **Friends & Family**\n- Ensure currency is **CHF**",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Payment(bot))