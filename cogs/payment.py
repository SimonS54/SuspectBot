import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS  # Import allowed role IDs from config

# Define a Payment cog to handle payment instruction commands
class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in commands

    # Command to provide payment instructions for "Dat" as a middleman
    @app_commands.command(name="dat", description="Payment instructions for Dat as your Middleman")
    async def dat(self, interaction: discord.Interaction, amount: str):
        # Extract user's role IDs for permission checking
        user_roles = [role.id for role in interaction.user.roles]
        # Check if user has any allowed role
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            # Create an embed with payment details for Dat
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
            # Send access denied message if user lacks proper roles
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide payment instructions for "Paradox" as a middleman
    @app_commands.command(name="paradox", description="Payment instructions for Paradox as your Middleman")
    async def paradox(self, interaction: discord.Interaction, amount: str):
        # Extract user's role IDs for permission checking
        user_roles = [role.id for role in interaction.user.roles]
        # Check if user has any allowed role
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            # Create an embed with payment details for Paradox
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
            # Send access denied message if user lacks proper roles
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Payment Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

# Setup function to register the Payment cog with the bot
async def setup(bot):
    await bot.add_cog(Payment(bot))  # Add the Payment cog to the bot instance