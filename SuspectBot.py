import discord
from discord.ext import commands
import asyncio
import json
import os

staff_stats = {}
handled_channels = {}

STAFF_ROLE_ID = 1297999355860615209

CATEGORY_IDS = [1314011243173908503, 1310348839827406990, 1317240722377932952, 1298000300774260817, 1298000331036164218, 1298000367384268880, 1298000435579326556, 1298000476058685490, 1305201380180627466, 1333811568756129856]

# Intents 9heaven
intents = discord.Intents.default()
intents.typing = False  # Deaktiviert das Tippen-Event
intents.presences = False  # Deaktiviert das Präsenz-Event
intents.message_content = True  # Aktiviert den Zugriff auf Nachrichteninhalte
intents.members = True  # Aktiviert den Zugriff auf Mitglieder

# Erstelle den Bot mit den definierten Intents
bot = commands.Bot(command_prefix=["/", "!"], intents=intents)

STATS_FILE = 'stats.json'

def save_stats():
    with open(STATS_FILE, 'w') as f:
        json.dump({
            'staff_stats': staff_stats,
            'handled_channels': {k: list(v) for k, v in handled_channels.items()}
        }, f)
    print(f"Saved stats: {staff_stats}")
    print(f"Saved handled channels: {handled_channels}")

def load_stats():
    global staff_stats, handled_channels
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            data = json.load(f)
            staff_stats = data.get('staff_stats', {})
            handled_channels = {k: set(v) for k, v in data.get('handled_channels', {}).items()}
        print(f"Loaded stats: {staff_stats}")
        print(f"Loaded handled channels: {handled_channels}")

ALLOWED_ROLE_IDS = [1276174525113040938,1297999380745420822, 1297999355860615209]
FILTERED_CHANNEL_ID = 1297999173592940564
ALLOWED_WORDS = ['insane', 'problems', 'problem', 'bad', 'issues', 'great', 'love', 'good', 'awesome',
                 'fantastic', 'insane', 'perfect', 'best', 'nice', '10/10', '/', '+', '-', 'support',
                 'staff', 'team', 'amazing', 'fantastic', 'incredible', 'outstanding', 'superb',
                 'exceptional', 'wonderful', 'fabulous', 'phenomenal', 'spectacular', 'brilliant',
                 'remarkable', 'stellar', 'terrific', 'marvelous', 'top-notch', 'impressive',
                 'magnificent', 'high-quality', 'well-made', 'durable', 'reliable', 'affordable',
                 'user-friendly', 'unique', 'creative', 'stylish', 'modern', 'beautiful', 'elegant',
                 'comfortable', 'convenient', 'effective', 'efficient', 'love it', 'highly recommend',
                 'worth every penny', 'exceeded expectations', 'better than expected', 'would buy again',
                 'must-have', 'go-to choice', 'works perfectly', 'game-changer', 'life-saver',
                 'excellent service', 'fast delivery', 'helpful staff', 'friendly', 'responsive',
                 'polite', 'knowledgeable', 'fast', 'powerful', 'quiet', 'smooth', 'accurate', 'safe',
                 'versatile', 'affordable', 'cost-effective', 'reasonable', 'good deal', 'great value',
                 'worth it', 'kudos', '5-star', 'unbeatable', 'fantastic buy', 'thank you', '100%']
LOG_CHANNEL_ID = 1298015864087511080

ANNOUNCE_COMMAND_CHANNEL_ID = 1297999872829689999  # Replace with the channel ID where the !announce command will be used
ANNOUNCE_TARGET_CHANNEL_ID = 1297999047935791145  # Replace with the channel ID where the announcement will be posted

UPDATE_COMMAND_CHANNEL_ID = 1297999872829689999  # Replace with the channel ID where the !update command will be used
UPDATE_TARGET_CHANNEL_ID = 1298001935948972043  # Replace with the channel ID where the update will be posted

allowed_channel_id = 1298016167184695376
allowed_user_id = [1039903232023081010, 397469006946238476, 806944542284709919, 1112883021406814248, 1138093567248695337, 756169131639701585, 368435292916416512, 368435292916416512, 1022589611496710164, 206166974269489154]
command_channel_id = 1297999872829689999
log_channel_id = 1238537184080822424  # Replace with the ID of the channel where you want to log updates

product_texts = {
    'Ring1 R6 :': 'Undetected & Safe to use :green_circle:',
    'Fluent Full :': 'Undetected & Safe to use :green_circle:',
    'Rust External :': 'Undetected & Safe to use :green_circle:',
    'Matrix :': 'Undetected & Safe to use :green_circle:',
    'Rust Recoil Script :': 'Undetected & Safe to use :green_circle:',
    'Kernaim Apex :': 'Undetected & Safe to use :green_circle:',
    'Apex Lite :': 'Undetected & Safe to use :green_circle:',
    'Kernaim BO6 :': 'Undetected & Safe to use :green_circle:',
    'RUT Unlock Tool BO6 :': 'Undetected & Safe to use :green_circle:',
    'RUT UAV Tool BO6 :': 'Undetected & Safe to use :green_circle:',
    'Exo EFT :': 'Undetected & Safe to use :green_circle:',
    'EFT Lite :': 'Undetected & Safe to use :green_circle:',
    'EFT Full :': 'Undetected & Safe to use :green_circle:',
    'TZ Internal :': 'Undetected & Safe to use :green_circle:',
    'TZ External :': 'Undetected & Safe to use :green_circle:',
    'HX FiveM :': 'Undetected & Safe to use :green_circle:',
    'Disconnect External FN :' : 'Undetected & Safe to use :green_circle:',
    'Exception Spoofer :': 'Undetected & Safe to use :green_circle:',
}

last_embed = None

def has_allowed_role(ctx):
    return ctx.author.id == allowed_user_id or any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)

@bot.event
async def on_ready():
    load_stats()
    save_stats()  # Ensure the file is created if it doesn't exist
    try:
        await bot.tree.sync()
        print(f'Successfully synchronized commands')
    except Exception as e:
        print(f'Failed to synchronize commands: {e}')
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="supporttool", description="Shows the support tool.")
async def support_tool(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Support Tool",
            description="""We are thrilled to have you as a customer and are here to ensure you have the best experience with our products. Should you encounter any issues or have questions, we're here to help. Please follow the provided steps for optimal use of your purchase.

https://mega.nz/file/ioJQ3TAK#khDxBBZ0_LiX__6zEnfr2N6PG1_HDuv271J5rFus7yQ

Please download the above file and make everything **Green**.
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="stats", description="Displays the current stats of staff members.")
async def stats(interaction: discord.Interaction):
    if not staff_stats:
        await interaction.response.send_message("No stats available.")
        return

    sorted_stats = sorted(staff_stats.items(), key=lambda x: x[1]['tickets_handled'], reverse=True)

    embed = discord.Embed(
        title="Staff Stats Leaderboard",
        color=discord.Color.red()
    )

    for rank, (staff_id, stats) in enumerate(sorted_stats, start=1):
        staff_member = interaction.guild.get_member(int(staff_id))
        if staff_member:
            embed.add_field(
                name=f"{rank}. {staff_member.display_name}",
                value=f"Tickets Handled: {stats['tickets_handled']}",
                inline=False
            )

    embed.set_footer(text="Powered by SuspectServices")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="epvp", description="Shows the Elitepvpers Instructions.")
async def epvp(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Elitepvpers Vouch",
            description="""**Please follow these steps:**

1. **Select a post for the product you have purchased from the list below:** \n
   [BO6 Lite](https://www.elitepvpers.com/forum/call-duty-trading/5281211-suspectservices-com-bo6-lite-esp-aimbot-controller-support-undetected.html)
   [Ring 1 R6](https://www.elitepvpers.com/forum/rainbow-six-siege-trading/5226949-suspectservices-com-ring-1-r6-aimbot-silent-aim-esp-gadget-esp-recoil.html) 
   [Rust External](https://www.elitepvpers.com/forum/rust-trading/5198453-rust-external-best-streamproof-cheat-undetected-instant-delivery.html) 
   [Exception Spoofer](https://www.elitepvpers.com/forum/rust-trading/5198665-suspectservices-com-exception-spoofer-best-spoofer-rust-undetected.html) 
   [EFT Full](https://www.elitepvpers.com/forum/escape-tarkov-trading/5271084-suspectservices-com-eft-full-magic-bullet-wallhack-loot-esp-god.html) 
   [EFT Lite](https://www.elitepvpers.com/forum/escape-tarkov-trading/5247476-suspectservices-com-eft-lite-built-spoofer-player-esp-quest-esp.html) 
   [BO6 Unlock All](https://www.elitepvpers.com/forum/call-duty-trading/5198447-black-ops-6-wz-unlock-all-ud-4-years-works-bo6-wz-instant-delivery.html) 
   [BO6 UAV Tool](https://www.elitepvpers.com/forum/call-duty-trading/5198448-black-ops-6-wz-uav-tool-undetected-constant-uav-instant-delivery.html) 
   [Rust Recoil Script](https://www.elitepvpers.com/forum/rust-trading/5208992-rust-recoil-script-undetected-all-weapons-customizable-randomization-easy-use-i.html) 
   [BO6 Pro](https://www.elitepvpers.com/forum/call-duty-trading/5229905-suspectservices-com-bo6-pro-wonder-weapon-saver-esp-aimbot-undetected.html) 
   [Apex Lite](https://www.elitepvpers.com/forum/apex-legends-trading/5193782-suspectservices-com-apex-lite-ud-15-months-aimbot-esp-instant-delivery.html) 
   [Exo EFT](https://www.elitepvpers.com/forum/escape-tarkov-trading/5201348-exo-eft-arena-supported-rage-intel-amd-undetected-speed-instant-delivery.html) 
   [Disconnect External FN](https://www.elitepvpers.com/forum/fortnite-trading/5281213-suspectservices-com-disconnect-external-ud-streamproof-instant-delivery.html)

2. **Send a trade request, and then leave a positive comment on the trade once accepted & the post.**
3. **Press the 'thanks' button on the post.**
4. **Leave a positive comment on our visitor page: [SuspectServices](https://www.elitepvpers.com/forum/members/8665498-suspectservices.html)** 

**Once done, let me know!**
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)  # Nachricht für alle sichtbar
        await interaction.followup.send("""https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzc3d2Y1b2JzcWQ3czFhOXVxZnU0a2ZhN3VzNGE3a2Y3dm95a2t3ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8OOU4QnsKQOqVrfA3w/giphy.gif""")
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="epvptrade", description="Explains how to leave a positive review for a trade.")
async def epvptrade(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="**Thank you! Your Trade has now been accepted**",
            description="""# **Follow the below steps to claim your key:**
Please now leave a positive rating on the trade, heres how to do it:

Head over to **'The Black Market'**
Look over to the right hand side and select **'Trades'**
Then find the trade with **SuspectServices** and click the **trade ID**
Here you will then see a text box, **please write a nice comment in the box and put the rating to positive.**

Please then provide us with your **Elitepvpers username** and select a **DAY KEY** from our store which you would like.
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)  # Nachricht für alle sichtbar
        await interaction.followup.send("""https://imgur.com/a/t6O6hQa""")
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)


@bot.tree.command(name="coreisolation", description="Show instructions for deactivating core isolation.")
async def coreisolation(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            """How to disable core isolation: https://www.youtube.com/watch?v=AEjt7daC60g
            
**Or run this:** https://cdn.discordapp.com/attachments/1312962765593378958/1313101942867890227/Turn_Core_Isolation_Memory_Integrity_OFF.reg?ex=6756293b&is=6754d7bb&hm=261f0f064b398a663334a16665721c60a16aee3da3cbf8a338c4e8a218fc72fb&
            """
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="anydesk", description="Instructions for using Anydesk for further support.")
async def anydesk(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            " Please download Anydesk so we can assist you further: https://anydesk.com/en-gb \n "
            "\n"
            "Once downloaded, provide us with your access code so we can connect!"
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="virt", description="Instructions for activating or deactivating virtualization.")
async def virt(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            "How to disable/enable Virtualization: https://www.youtube.com/watch?v=NNNLuBGjxFw"
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="tpm", description="Instructions for activating or deactivating TPM.")
async def tpm(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            "How to disable/enable TPM: https://www.youtube.com/watch?v=sCKKjaZjqGM"
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="secureboot", description="Instructions for activating or deactivating Secure Boot.")
async def secureboot(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            "How to disable/enable Secure Boot: https://www.youtube.com/watch?v=z0YJi8RJHK4"
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="vc64", description="Instructions for installing the required Visual C++ redistributables.")
async def vc64(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            """Please install the following:
https://aka.ms/vs/17/release/vc_redist.x64.exe
https://www.microsoft.com/en-us/download/details.aspx?id=35"""
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="review", description="Link to review..")
async def review(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        message = (
            "<#1297999173592940564> Are always appreciated!"
        )
        await interaction.response.send_message(message)  # Nachricht für alle sichtbar
    else:
        message = (
            "Permission Denied\n"
            "You don't have permission to use this command.\n"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="bothelp", description="Shows a commands list.")
async def bothelp(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Commands",
            description="""Suspect Bot Commands **STAFF ONLY**:

            **Guide Links:**
            /apexcola
            /rustexternal
            /exception
            /monolith
            /rutunlock **(MW3/BO6)**
            /rutuav **(MW3/BO6)**
            /recoil 
            /terra
            /exoeft
            /kernaim **(Kernaim MW3/BO6)**
            /ring1r6
            /klarz **(Klar Dayz)**
            /tz
            /kernapex
            /fluent
            /kernaimxdefiant
            /apexexternal
            /goldcore
            /r6lite

            **Message Commands:**
            !update - Sends message to #updates
            !announce - Sends message to #announcements
            !staticupdate - Sends embed in #product-status
            !productupdate "Product Name :" Status + Corresponding emoji
            /bothelp - Sends list of available commands

            **Automated Replies:**
            /epvp - Sends Elitepvpers Vouch List
            /epvptrade - Sends instructions to leave EPVP Trade once accepted
            /supporttool - Sends Suspect Support Tool
            /virt - Guide to enable/disable Virtualization
            /anydesk - Sends anydesk link
            /review - Prompts the customer to leave a review
            /tpm - Guide to disable TPM
            /coreisolation - Guide to disable core isolation
            /secureboot - Guide to enable/disable secure boot

            **Paypal Commands:**
            /heaven *amount in EUR*

            For bot bugs please contact 9heaven.
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices and 9heaven")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="checkrole", description="Checks whether the user has a specific role.")
async def check_role(interaction: discord.Interaction, role_name: str):
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if role in interaction.user.roles:
        embed = discord.Embed(
            title="Role Check",
            description=f"You have the {role.name} role.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Role Check",
            description=f"You don't have the {role.name} role.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="heaven", description="Payment instruction for MM.")
async def nine_k(interaction: discord.Interaction, amount: str):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        await interaction.response.send_message(
            f"Thank you for choosing <@1232181386090123297> as your MM. Please send {amount} EUR to https://www.paypal.com/paypalme/chrivvs f&f."
        )
    else:
        await interaction.response.send_message("You don't have permission to use this command.")

@bot.tree.command(name="9k", description="Payment instruction for MM.")
async def nine_k(interaction: discord.Interaction, amount: str):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        await interaction.response.send_message(
            f"Thank you for choosing <@397469006946238476> as your MM. Please send {amount} EUR to https://paypal.me/9kuk f&f."
        )
    else:
        await interaction.response.send_message("You don't have permission to use this command.")

@bot.command(name='announce')
async def announce(ctx, *, message: str):
    if ctx.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
        return

    target_channel = bot.get_channel(ANNOUNCE_TARGET_CHANNEL_ID)
    if target_channel is None:
        await ctx.send("The target channel for announcements could not be found.")
        return

    await target_channel.send(message)

@bot.command(name='update')
async def update(ctx, *, message: str):
    if ctx.channel.id != UPDATE_COMMAND_CHANNEL_ID:
        return

    target_channel = bot.get_channel(UPDATE_TARGET_CHANNEL_ID)
    if target_channel is None:
        await ctx.send("The target channel for updates could not be found.")
        return

    await target_channel.send(message)

@bot.tree.command(name="nextcheat", description="Sends the link to the NextCheat documentary.")
async def nextcheat(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="NextCheat",
            description=f"https://suspectservices.gitbook.io/nextcheat/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rustexternal", description="Sends the link to the Rust External documentation.")
async def rustexternal(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Rust External",
            description=f"https://suspectservices.gitbook.io/rust-external/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="apexlite", description="Sends the link to activate your Apex Lite key.")
async def apexlite(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Apex Lite",
            description=f"""Join this discord to activate your key: https://discord.gg/QPRuwFCXgP

Instructions will be sent with your custom loader link""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exception", description="Sends the link to the Exception Spoofer documentation.")
async def exception(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Exception Spoofer",
            description=f"https://suspectservices.gitbook.io/exception-spoofer/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="monolith", description="Sends the link to the Monolith External documentation.")
async def monolith(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Monolith External",
            description=f"https://suspectservices.gitbook.io/monolith-external/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rutunlock", description="Sends the link to the RUT Unlock Tool documentation.")
async def rutunlock(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="RUT Unlock Tool",
            description=f"https://suspectservices.gitbook.io/rut-unlock-tool/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rutuav", description="Sends the link to the RUT UAV Tool documentation.")
async def rutuav(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="RUT UAV Tool",
            description=f"https://suspectservices.gitbook.io/rut-uav-tool/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="recoil", description="Sends the link to the Rust Recoil Script documentation.")
async def recoil(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Rust Recoil Script",
            description=f"https://suspectservices.gitbook.io/rust-recoil-script/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="terra", description="Sends the link to the RU TerraABS EFT documentation.")
async def terra(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="RU TerraABS EFT",
            description=f"https://suspectservices.gitbook.io/ru-terraabs-eft/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exoeft", description="Sends the link to the Exo EFT documentation.")
async def exoeft(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Exo EFT",
            description=f"https://suspectservices.gitbook.io/exo-eft/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kernaim", description="Sends the link to the KernAim MW3 documentation.")
async def kernaim(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="KernAim MW3",
            description=f"https://suspectservices.gitbook.io/kernaim-mw3/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ring1r6", description="Sends the link to the Ring 1 R6 documentation.")
async def ring1r6(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Ring 1 R6",
            description=f"https://suspectservices.gitbook.io/ring-1-r6/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="tz", description="Sends the link to the TZ Project documentation.")
async def tz(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="TZ Project",
            description=f"https://suspectservices.gitbook.io/tz-project-fivem/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kernaimapex", description="Sends the link to the Kernaim Apex documentation.")
async def kernaimapex(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Kernaim Apex",
            description=f"https://suspectservices.gitbook.io/kernaim-apex/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fluent", description="Sends the link to the Fluent documentation.")
async def fluent(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Fluent",
            description=f"https://suspectservices.gitbook.io/fluent-rust/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="r6lite", description="Sends the link to the R6 Lite documentation.")
async def r6lite(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="R6 Lite",
            description=f"https://suspectservices.gitbook.io/r6-lite",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="matrix", description="Sends the link to the Matrix Rust documentation.")
async def matrix(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Matrix Rust",
            description=f"https://suspectservices.gitbook.io/matrix-rust/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bo6pro", description="Sends the link to the BO6 Pro documentation.")
async def bo6pro(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="BO6 Pro",
            description=f"https://suspectservices.gitbook.io/bo6-pro/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hx", description="Sends the link to the HX documentation.")
async def hx(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="HX Menu",
            description=f"https://suspectservices.gitbook.io/hx-menu/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="disconnect_fn", description="Sends the link to the Disconnect FN documentation.")
async def disconnectfn(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Disconnect FN",
            description=f"https://suspectservices.com/product/fn-disconnect-external/",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.command(name='staticupdate',)
@commands.check(has_allowed_role)
async def post_static_update(ctx):
    global last_embed
    if ctx.channel.id != command_channel_id:
        return

    update_channel = bot.get_channel(allowed_channel_id)
    embed = discord.Embed(title='Product Status')
    for product, text in product_texts.items():
        embed.add_field(name=f"{product} {text}", value="\u200b", inline=False)
    embed.set_footer(text="*Powered by SuspectServices*")

    if last_embed:
        await last_embed.delete()

    last_embed = await update_channel.send(embed=embed)
    await ctx.message.add_reaction('?')

@bot.command(name='productupdate',)
@commands.check(has_allowed_role)
async def update_product(ctx, product, *, new_text):
    global last_embed
    if ctx.channel.id != command_channel_id:
        return

    if product not in product_texts:
        await ctx.send(f'Invalid product: {product}')
        return

    old_text = product_texts[product]
    product_texts[product] = new_text

    update_channel = bot.get_channel(allowed_channel_id)
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(title='Product Status')
    for prod, text in product_texts.items():
        embed.add_field(name=f"{prod} {text}", value="\u200b", inline=False)
    embed.set_footer(text="*Powered By SuspectServices*")

    if last_embed:
        await last_embed.delete()

    last_embed = await update_channel.send(embed=embed)
    await ctx.message.add_reaction('?')

    log_embed = discord.Embed(title=f'Update for {product}', color=discord.Color.red())
    log_embed.add_field(name='Old Text', value=old_text, inline=False)
    log_embed.add_field(name='New Text', value=new_text, inline=False)
    log_embed.set_footer(text=f'Updated by {ctx.author}', icon_url=ctx.author.avatar_url)
    await log_channel.send(embed=log_embed)

@bot.tree.command(name="disconnecterror", description="Sends the link to the Disconnect Errors List")
async def disconnecterror(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Disconnect Errors",
            description=(
                """**Format:**  
                (Error Message) : (Error Code) : (Error Reason) : (Suggested Solution)  

                **Misc. Reason Key:**  
                1. *Unknown Errors* = Likely due to Anti-Virus or Anti-Cheat interference.  
                2. *Removed Errors* = Details not disclosed. Refer to a developer.  

                **Info:**  
                This guide lists common errors. Some may not be included if self-explanatory.  

                **Error Key:**  
                `?` = Identifying Code (for developers).  
                `ERRORCODE` = Windows Error Code."""
            ),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Error Details",
            value=(
                """ 
                (Bootstrap Failure) : (Invalid Data 0x?) : (Failed to Contact Loader Server) : Check your ISP or server status.  
                (Bootstrap Failure) : (Failed to Open Client) : Contact a developer.  
                (Bootstrap Failure) : (Cleanup Error) : Likely caused by Anti-Virus interference.  
                (Bootstrap Failure) : (Query Error) : Insufficient permissions; check Anti-Virus settings."""
            ),
            inline=False
        )
        embed.add_field(
            name="Overlay Failures",
            value=(
                "(Overlay Failure) : (0x0) : (Couldn't Register DX Window Class) : "
                "(Missing DirectX Runtimes Likely / Runtimes Need to be Updated / DirectX Version Unsupported)\n"
                "(Overlay Failure) : (0x1) : (Couldn't Create or Update Window) : (Contact Dev, Shouldn't ever happen)\n"
                "(Overlay Failure) : (0x2) : (Couldn't Create DX Device) : "
                "(Missing DirectX Runtimes Likely / Runtimes Need to be Updated / DirectX Version Unsupported)\n"
                "(Overlay Failure) : (0x3) : (Window / Window Handle Invalid or Closed) : "
                "(Potentially Re-Install DirectX or Contact Dev)"
            ),
            inline=False
        )
        embed.add_field(
            name="Injection Failures",
            value=(
                """
                (Injection Failure) : (0x0) : Product Data Missing or Corrupted.  
                (Injection Failure) : (0x9 : 0x14) : Uninstall Anti-Virus and try again.  
                (Injection Failure) : (0x11 : 0x1) : Invalid Injection Data. Use a VPN or contact a dev.
                """
            ),
            inline=False
        )
        embed.add_field(
            name="Bypass Failures",
            value=(
                """
                (Bypass Failure) : (0x0 : 0x1) : Unknown issue. Contact a developer.  
                (Bypass Failure) : (0x1 : 0x0) : System corruption. Reinstall Windows or contact support.  
                (Bypass Failure) : (0x1 : 0x1) : System issue. Submit logs to the developer.
                """
            ),
            inline=False
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fluenterror", description="Sends the link to the Fluent Errors List")
async def fluenterror(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Fluent Errors",
            description=(
                "**Common Issues:**\n"
                "**Error 0xc01c0013**\n"
                "Make sure UAC (User Account Control) is enabled and file virtualization is enabled.\n"
                "[Download and run this registry file](https://fluent.gg/c01c0013.reg)\n"
                "Alternatively, [download and run this batch file as admin](https://fluent.gg/c01c0013.bat)\n"
                "Restart your computer.\n\n"
                "If the above does not help you (does not work on Windows Home):\n"
                "1. Press `Windows + R`, type `secpol.msc`, and open the Local Security Policy.\n"
                "2. Expand Local Policies > Security Options.\n"
                "3. Open `User Account Control: Virtualize file and registry write failures to per-user locations` and enable it.\n"
                "4. Restart your computer.\n"
                "Make sure you are not running unofficial Windows ISOs.\n\n"
                "**Error 0xc00000bb**\n"
                "Your Windows version is not supported. Ensure you are running official Windows and are not on Insider/Preview builds.\n"
                "You can download Windows installation media from the Microsoft website.\n\n"
                "**Error 0xc0000365 / 0xc0000906 / 0xc0000907 / 0xc000009a / 0xc0000022 / 0xc000004e**\n"
                "1. Uninstall FaceIT AC/Vanguard/ESEA anti-cheat or other anti-cheat software starting at boot.\n"
                "2. Restart your computer.\n"
                "3. Disable your antivirus.\n"
                "4. If none of the above work, reinstall Windows using the official Windows ISO.\n\n"
                "**Error 0xc0000428**\n"
                "Disable Secure Boot. [Disabling Secure Boot | Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/disabling-secure-boot)\n\n"
                "**Issues with 3rd Party HWID Spoofers**\n"
                "Some users might experience issues with 3rd party HWID spoofers:\n"
                "1. Log in to the loader.\n"
                "2. Before injecting, use your 3rd party HWID spoofer.\n"
                "3. Inject as normal. When the loader asks if you want to spoof, click 'No'.\n"
                "4. Launch the game as you normally would."
            ),
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exceptionerror", description="Sends the link to the Exception Errors List")
async def exceptionerror(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Exception Errors",
            description=(
                "**#10000004**\n"
                "Make sure AV/EDR is not running and you are not infected by a rootkit.\n\n"
                "**#37070000**\n"
                "Make sure Faceit/Vanguard driver is not running.\n\n"
                "**#3B000000**\n"
                "Open cmd.exe as admin, type the following:\n"
                "`bcdedit /set hypervisorlaunchtype off`\n"
                "Hit Enter and restart your PC.\n\n"
                "**#370F0022**\n"
                "Hold SHIFT and restart your PC.\n\n"
                "**#3C000101**\n"
                "Windows build number requirement is not met. The minimum supported build number is 19041.\n\n"
                "**#3C000110**\n"
                "Multiple running instances of the launcher are not allowed."
            ),
            color=discord.Color.orange()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="r6error", description="Sends the link to the R6 Errors List")
async def r6error(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="R6 Errors & Guide",
            description="For a comprehensive guide and troubleshooting tips for R6 errors, visit the following link:\n\n"
                        "[R6 Errors & Guide](https://cheatarmy.com/tutorial)",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="camo", description="Sends the link to the Camo Unlocks Form")
async def camo(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Camo Unlocks Form",
            description="""__**Please Answer this form using numbers 1, 2, and 3 to reference:**__

**1. Please provide your Activision ID:**  
**Activision ID:** (Enter your Activision ID)

**2. Do you care for Gold or Diamond out of any of the mastery camos?**  
**Answer:** (Yes/No)  
*(Note: If no, it speeds up the process.)*

**3. If no, please specify which camos you would like:**  
**Desired Camos:** (Enter the camos you'd like)
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="camobox", description="Sends the link to the Camo Unlocks Form for Xbox")
async def camobox(interaction: discord.Interaction):
    user_roles = [role.id for role in interaction.user.roles]
    if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
        embed = discord.Embed(
            title="Console Unlocks Form",
            description="""__**Please Answer this form using numbers 1, 2, and 3 to reference:**__

**1. Do you have Xbox Game Pass?**  
**Answer:** (Yes/No)  
If yes, please provide your Xbox login:

**Xbox Login:** (Enter your Xbox login)  
If no, please provide your Activision ID:  

**Activision ID:** (Enter your Activision ID)

**2. Do you care for Gold or Diamond out of any of the mastery camos?**  
**Answer:** (Yes/No)  
(Note: If no, it speeds up the process.)

**3. If no, please specify which camos you would like:**  
**Desired Camos:** (Enter the camos you'd like)
""",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission Denied",
            description="You don't have permission to use this command.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")
        await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if message.channel.id == FILTERED_CHANNEL_ID:
        allowed = any(word.lower() in message.content.lower() for word in ALLOWED_WORDS)
        if not allowed:
            if message.author.id != bot.user.id:
                deleted_message_embed = discord.Embed(
                    title="Deleted Message",
                    description=f"Message from {message.author.name} ({message.author.id}): {message.content}",
                    color=discord.Color.red()
                )
                deleted_message_embed.set_footer(text="Powered by SuspectServices")
                await log_channel.send(embed=deleted_message_embed)

                notification_embed = discord.Embed(
                    title="Message Deleted",
                    description=f"{message.author.mention}, your message was deleted because it didn't contain any of the allowed words.",
                    color=discord.Color.red()
                )
                notification_embed.set_footer(text="Powered by SuspectServices")
                notification_message = await message.channel.send(embed=notification_embed)
                await message.delete()
                await asyncio.sleep(2)
                await notification_message.delete(delay=3)

    if message.channel.category_id in CATEGORY_IDS:
        if any(role.id == STAFF_ROLE_ID for role in message.author.roles):
            staff_id = message.author.id
            channel_id = message.channel.id

            if staff_id not in handled_channels:
                handled_channels[staff_id] = set()

            if channel_id not in handled_channels[staff_id]:
                handled_channels[staff_id].add(channel_id)
                if staff_id not in staff_stats:
                    staff_stats[staff_id] = {'tickets_handled': 0}
                staff_stats[staff_id]['tickets_handled'] += 1
                save_stats()  # Save stats whenever they are updated

    await bot.process_commands(message)

@bot.event
async def on_disconnect():
    save_stats()

if __name__ == "__main__":
    bot.run('MTM0MTcxNDcyMzM4NDU5MDQ1Ng.GJ037c.qID2nWkaWsMw7UbK38-pEpbKSdWqnxQh-ctpJ4')
