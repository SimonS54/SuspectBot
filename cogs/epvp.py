import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class EPVP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Instructions for leaving a vouch on Elitepvpers.
    @app_commands.command(name="epvp", description="Instructions for leaving a EPVP vouch.")
    async def epvp(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Elitepvpers Vouch",
                description="**Please follow these steps:**\n\n"
                            "1. **Select a post for the product you have purchased from the list below:**\n\n"
                            
                            """[BO6 Lite](https://www.elitepvpers.com/forum/call-duty-trading/5281211-suspectservices-com-bo6-lite-esp-aimbot-controller-support-undetected.html)
                            [Ring-1 R6](https://www.elitepvpers.com/forum/rainbow-six-siege-trading/5226949-suspectservices-com-ring-1-r6-aimbot-silent-aim-esp-gadget-esp-recoil.html) 
                            [Rust Disconnect External](https://www.elitepvpers.com/forum/rust-trading/5198453-rust-external-best-streamproof-cheat-undetected-instant-delivery.html) 
                            [Exception Spoofer](https://www.elitepvpers.com/forum/rust-trading/5198665-suspectservices-com-exception-spoofer-best-spoofer-rust-undetected.html) 
                            [EFT NextCheat Full](https://www.elitepvpers.com/forum/escape-tarkov-trading/5271084-suspectservices-com-eft-full-magic-bullet-wallhack-loot-esp-god.html) 
                            [EFT NextCheat Lite](https://www.elitepvpers.com/forum/escape-tarkov-trading/5247476-suspectservices-com-eft-lite-built-spoofer-player-esp-quest-esp.html) 
                            [COD Unlock All](https://www.elitepvpers.com/forum/call-duty-trading/5198447-black-ops-6-wz-unlock-all-ud-4-years-works-bo6-wz-instant-delivery.html) 
                            [COD UAV Tool](https://www.elitepvpers.com/forum/call-duty-trading/5198448-black-ops-6-wz-uav-tool-undetected-constant-uav-instant-delivery.html) 
                            [Rust Recoil Script](https://www.elitepvpers.com/forum/rust-trading/5208992-rust-recoil-script-undetected-all-weapons-customizable-randomization-easy-use-i.html) 
                            [Apex Kernaim](https://www.elitepvpers.com/forum/apex-legends-trading/5193782-suspectservices-com-apex-lite-ud-15-months-aimbot-esp-instant-delivery.html) 
                            [Fortnite Disconnect External](https://www.elitepvpers.com/forum/fortnite-trading/5281213-suspectservices-com-disconnect-external-ud-streamproof-instant-delivery.html)\n\n"""
                            
                            "2. **Send a trade request, and then leave a positive comment on the trade once accepted & the post.**\n"
                            "3. **Press the 'thanks' button on the post.**\n"
                            "4. **Leave a positive comment on our visitor page: [SuspectServices](https://www.elitepvpers.com/forum/members/8665498-suspectservices.html)**\n\n"
                            "5. **Reply to this message with the link to your vouch including a @ for either Paradox or Liam.**",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
            await interaction.followup.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzc3d2Y1b2JzcWQ3czFhOXVxZnU0a2ZhN3VzNGE3a2Y3dm95a2t3ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8OOU4QnsKQOqVrfA3w/giphy.gif")
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Instructions for leaving a trade review on Elitepvpers.
    @app_commands.command(name="epvptrade", description="Explains how to leave a positive review for a trade.")
    async def epvptrade(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Thank you! Your Trade has now been accepted",
                description="## **Follow the below steps to claim your key:**\n\n"
                            "Please now leave a positive rating on the trade, heres how to do it:\n\n"

                            """Head over to **'The Black Market'**
                            Look over to the right hand side and select **'Trades'**
                            Then find the trade with **SuspectServices** and click the **trade ID**
                            Here you will then see a text box, **please write a nice comment in the box and put the rating to positive.**\n\n"""

                            "Please then provide us with your **Elitepvpers username** and select a **DAY KEY** from our store which you would like.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
            await interaction.followup.send("https://imgur.com/a/t6O6hQa")
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(EPVP(bot))