import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to display a list of available bot commands.
    @app_commands.command(name="bothelp", description="Shows a commands list.")
    async def bothelp(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Commands List",
                description="List of available commands offered by SuspectBot:\n\n"
                            
                            """**Documentation Section:**
                            /apexlite - Get Guide for Apex Lite
                            /apexkernaim - Get Guide for Apex Kernaim
                            /codkernaim - Get Guide for COD Kernaim
                            /codrutunlock - Get Guide for COD RUT Unlock
                            /codrutuav - Get Guide for COD RUT UAV
                            /eftexoarena - Get Guide for EFT Exo Arena
                            /eftexo - Get Guide for EFT Exo
                            /eftnextfull - Get Guide for EFT Nextcheat Full
                            /eftnextlite - Get Guide for EFT Nextcheat Lite
                            /fivemhx - Get Guide for FiveM HX
                            /fivemtzext - Get Guide for FiveM TZ External
                            /fivemtzint - Get Guide for FiveM TZ Internal
                            /fndcext - Get Guide for FN Disconnect External
                            /hwidexception - Get Guide for Exception Spoofer
                            /marvelklar - Get Guide for Marvel Rivals Klar
                            /r6ring - Get Guide for R6 Ring1
                            /rustfluent - Get Guide for Rust Fluent
                            /rustmatrix - Get Guide for Rust Matrix
                            /rustdcext - Get Guide for Rust Disconnect External
                            /rustrecoil -  Get Guide for Rust Recoil Script
                            
                            **Support Section:**
                            /supporttool - Get the support tool
                            /anydesk - Get the AnyDesk tool
                            /virtualization - Get the Virtualization Guide
                            /tpm - Get the TPM Guide
                            /secureboot - Get the Secure Boot Guide
                            /coreisolation - Get the Core Isolation Guide
                            /vc64 - Get the Visual C++ redistributables
                
                            **Elitepvpers Section:**
                            /epvp - Get Elitepvpers vouch list
                            /epvptrade - Get Instructions for a trade review
                            
                            **Payment Section:**
                            /dat - Payment instructions for Dat
                            /paradox - Payment instructions for Paradox
                            
                            **Moderation Section:**
                            /announce - Send an announcement
                            /update - Send an update
                            */productupdate - Update a product status
                
                            **General Section:**
                            /review - Leave a review
                            /bothelp - Shows this list
                            
                            **Stats Section:**
                            /stats - Retrieve ticket stats of the support team""",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to ask the client to leave a review.
    @app_commands.command(name="review", description="Asks the client to leave a review.")
    async def review(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Review",
                description="If you are satisfied with both product and support team we would be pleased to receive a review from you, as this helps us improve our store daily.\n\n"
                            "Spare us a few minutes of your time and leave a review here: <#1297999173592940564>",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
