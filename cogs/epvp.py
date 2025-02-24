import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class EPVP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="epvp", description="How to leave a vouch on Elitepvpers")
    async def epvp(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="⭐ Elitepvpers Vouch Guide",
                description="**1️⃣ Choose Your Product**\nSelect the post for your purchased product from the categories below, then follow the remaining steps:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="🎮 Call of Duty",
                value="[BO6 Lite](https://www.elitepvpers.com/forum/call-duty-trading/5281211-suspectservices-com-bo6-lite-esp-aimbot-controller-support-undetected.html)\n"
                      "[COD Unlock All](https://www.elitepvpers.com/forum/call-duty-trading/5198447-black-ops-6-wz-unlock-all-ud-4-years-works-bo6-wz-instant-delivery.html)\n"
                      "[COD UAV Tool](https://www.elitepvpers.com/forum/call-duty-trading/5198448-black-ops-6-wz-uav-tool-undetected-constant-uav-instant-delivery.html)",
                inline=False
            )
            embed.add_field(
                name="🏃 Escape from Tarkov",
                value="[EFT NextCheat Full](https://www.elitepvpers.com/forum/escape-tarkov-trading/5271084-suspectservices-com-eft-full-magic-bullet-wallhack-loot-esp-god.html)\n"
                      "[EFT NextCheat Lite](https://www.elitepvpers.com/forum/escape-tarkov-trading/5247476-suspectservices-com-eft-lite-built-spoofer-player-esp-quest-esp.html)",
                inline=False
            )
            embed.add_field(
                name="🛠️ Rust",
                value="[Rust Disconnect External](https://www.elitepvpers.com/forum/rust-trading/5198453-rust-external-best-streamproof-cheat-undetected-instant-delivery.html)\n"
                      "[Exception Spoofer](https://www.elitepvpers.com/forum/rust-trading/5198665-suspectservices-com-exception-spoofer-best-spoofer-rust-undetected.html)\n"
                      "[Rust Recoil Script](https://www.elitepvpers.com/forum/rust-trading/5208992-rust-recoil-script-undetected-all-weapons-customizable-randomization-easy-use-i.html)",
                inline=False
            )
            embed.add_field(
                name="🎯 Other Games",
                value="[Ring-1 R6](https://www.elitepvpers.com/forum/rainbow-six-siege-trading/5226949-suspectservices-com-ring-1-r6-aimbot-silent-aim-esp-gadget-esp-recoil.html)\n"
                      "[Apex Kernaim](https://www.elitepvpers.com/forum/apex-legends-trading/5193782-suspectservices-com-apex-lite-ud-15-months-aimbot-esp-instant-delivery.html)\n"
                      "[Fortnite Disconnect External](https://www.elitepvpers.com/forum/fortnite-trading/5281213-suspectservices-com-disconnect-external-ud-streamproof-instant-delivery.html)",
                inline=False
            )
            embed.add_field(
                name="2️⃣ Send Trade Request",
                value="Request a trade on the post, then leave a positive comment once accepted.",
                inline=False
            )
            embed.add_field(
                name="3️⃣ Thank the Post",
                value="Press the 'Thanks' button on the product post.",
                inline=False
            )
            embed.add_field(
                name="4️⃣ Visitor Page Comment",
                value="Leave a positive comment on our page: [SuspectServices](https://www.elitepvpers.com/forum/members/8665498-suspectservices.html)",
                inline=False
            )
            embed.add_field(
                name="5️⃣ Reply Here",
                value="Reply to this message with your vouch link and mention @Paradox or @Liam.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • EPVP Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            await interaction.followup.send("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzc3d2Y1b2JzcWQ3czFhOXVxZnU0a2ZhN3VzNGE3a2Y3dm95a2t3ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8OOU4QnsKQOqVrfA3w/giphy.gif")
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • EPVP Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="epvptrade", description="How to leave a positive trade review on Elitepvpers")
    async def epvptrade(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="✅ Trade Accepted - Next Steps",
                description="Thanks for your trade! Follow these steps to claim your key:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📝 Leave a Positive Review",
                value="1. Go to **'The Black Market'**.\n"
                      "2. On the right, click **'Trades'**.\n"
                      "3. Find your trade with **SuspectServices** and click the **trade ID**.\n"
                      "4. In the text box, write a nice comment and set the rating to **positive**.",
                inline=False
            )
            embed.add_field(
                name="🔑 Claim Your Key",
                value="Provide your **Elitepvpers username** and choose a **DAY KEY** from our store.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • EPVP Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            await interaction.followup.send("https://imgur.com/a/t6O6hQa")
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • EPVP Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EPVP(bot))