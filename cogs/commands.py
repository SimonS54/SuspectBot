import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bothelp", description="List of all available bot commands")
    async def bothelp(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="📋 SuspectBot Command List",
                description="Here’s everything you can do with SuspectBot—find the command you need below!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📘 Documentation — (use + error for error codes)",
                value="*/apexlite* - Apex Lite guide\n"
                      "*/apexkernaim* - Apex Kernaim guide\n"
                      "*/codkernaim* - COD Kernaim guide\n"
                      "*/codrutunlock* - COD RUT Unlock guide\n"
                      "*/codrutuav* - COD RUT UAV guide\n"
                      "*/eftexoarena* - EFT Exo Arena guide\n"
                      "*/eftexo* - EFT Exo guide\n"
                      "*/eftnextfull* - EFT NextCheat Full guide\n"
                      "*/eftnextlite* - EFT NextCheat Lite guide\n"
                      "*/fivemhx* - FiveM HX guide\n"
                      "*/fivemtzext* - FiveM TZ External guide\n"
                      "*/fivemtzint* - FiveM TZ Internal guide\n"
                      "*/fndcext* - FN Disconnect External guide\n"
                      "*/hwidexception* - Exception Spoofer guide\n"
                      "*/marvelklar* - Marvel Rivals Klar guide\n"
                      "*/r6ring* - R6 Ring1 guide\n"
                      "*/rustfluent* - Rust Fluent guide\n"
                      "*/rustmatrix* - Rust Matrix guide\n"
                      "*/rustdcext* - Rust Disconnect External guide\n"
                      "*/rustrecoil* - Rust Recoil Script guide",
                inline=False
            )
            embed.add_field(
                name="🛠️ Support",
                value="*/supporttool* - Get the support tool\n"
                      "*/anydesk* - Get AnyDesk tool\n"
                      "*/virtualization* - Virtualization guide\n"
                      "*/tpm* - TPM guide\n"
                      "*/secureboot* - Secure Boot guide\n"
                      "*/coreisolation* - Core Isolation guide\n"
                      "*/vc64* - Visual C++ redistributables",
                inline=False
            )
            embed.add_field(
                name="🌟 Elitepvpers",
                value="*/epvp* - Elitepvpers vouch list\n"
                      "*/epvptrade* - Trade review instructions",
                inline=False
            )
            embed.add_field(
                name="💰 Payment",
                value="*/dat* - Payment for Dat\n"
                      "*/paradox* - Payment for Paradox",
                inline=False
            )
            embed.add_field(
                name="🔧 Moderation",
                value="*/announce* - Send an announcement\n"
                      "*/update* - Send an update\n"
                      "*/productupdate* - Update product status",
                inline=False
            )
            embed.add_field(
                name="📊 General",
                value="*/review* - Leave a review\n"
                      "*/bothelp* - Show this list",
                inline=False
            )
            embed.add_field(
                name="📈 Stats",
                value="*/stats* - Support team ticket stats",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • General Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • General Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="review", description="Request to leave a review for SuspectServices")
    async def review(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🌟 Leave a Review",
                description="Loved our products and support? We’d appreciate your feedback—it helps us grow!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📝 How to Review",
                value="Take a moment to share your thoughts here: <#1297999173592940564>",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • General Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • General Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))