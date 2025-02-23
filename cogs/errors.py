import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class Documentation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to display error fixes for Apex Lite.
    @app_commands.command(name="apexliteerror", description="Sends the fixes to common error codes for Apex Lite.")
    async def apexliteerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Apex Lite Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Apex Kernaim.
    @app_commands.command(name="apexkernaimerror", description="Sends the fixes to common error codes for Apex Kernaim.")
    async def apexkernaimerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Apex Kernaim Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for COD Kernaim.
    @app_commands.command(name="codkernaimerror", description="Sends the fixes to common error codes for COD Kernaim.")
    async def codkernaimerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD Kernaim Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for COD RUT Unlocker.
    @app_commands.command(name="codrutunlockerror", description="Sends the fixes to common error codes for COD RUT Unlocker.")
    async def codrutunlockerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD RUT Unlocker Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for COD RUT UAV.
    @app_commands.command(name="codrutuaverror", description="Sends the fixes to common error codes for COD RUT UAV.")
    async def codrutuaverror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD RUT UAV Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for EFT Exo Arena.
    @app_commands.command(name="eftexoarenaerror", description="Sends the fixes to common error codes for EFT Exo Arena.")
    async def eftexoarenaerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT Exo Arena Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error 92:** Please Disable Secure Boot in your BIOS settings.\n\n"
                            "**Error 94:** Please set your Bios to UEFI mode.\n\n"
                            "**Error 95:** Please enable Virtualization in your Bios.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for EFT Exo.
    @app_commands.command(name="eftexoerror", description="Sends the fixes to common error codes for EFT Exo.")
    async def eftexoerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT Exo Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error 92:** Please Disable Secure Boot in your BIOS settings.\n\n"
                            "**Error 94:** Please set your Bios to UEFI mode.\n\n"
                            "**Error 95:** Please enable Virtualization in your Bios.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for EFT NextCheat Full.
    @app_commands.command(name="eftnextfullerror", description="Sends the fixes to common error codes for EFT NextCheat Full.")
    async def eftnextfullerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT NextCheat Full Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error cannot start driver due...:** Please Disable Secure Boot in your BIOS settings. Additionally make sure theres no active Anticheat/Antivirus running.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for EFT NextCheat Lite.
    @app_commands.command(name="eftnextliteerror", description="Sends the fixes to common error codes for EFT NextCheat Lite.")
    async def eftnextliteerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT NextCheat Lite Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error cannot start driver due...:** Please Disable Secure Boot in your BIOS settings. Additionally make sure theres no active Anticheat/Antivirus running.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for FiveM HX.
    @app_commands.command(name="fivemhxerror", description="Sends the fixes to common error codes for FiveM HX.")
    async def fivemhxerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM HX Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error steam.exe popup with a bunch of random letters:** Error is mostly caused by the product being used on geforce now or a shadow pc. If thats not the case restart your pc and redo the injection progress.\n\n"
                            "**Error user couldn't be found:** Make sure you are registered as a user on the hx panel, if that's the case and you still get this issue please ask support for further instructions.\n\n"
                            "**Error no user was found with current HWID:** Please provide your key + user in the ticket and wait for support.\n\n"
                            "**Error limit reached:** You have used the maximum amount of HWID resets. Please wait for support.\n\n"
                            "**Error ntdll.dll:** To solve this 1.) Open FiveM without HX. 2.) Change screentype to Fullscreen. 3.) Go to your FiveM Application Data. 4.) Delete the data, crashes and logs folder. 5.) Try to reinject if this doesnt work wait for support.\n\n"
                            "**Error instaban:** To solve this 1.) Change menu key to something not suspicious. 2.) Disable Block Game Input option in the config tab. 3.) Dont use rage/exploit features. 5.) Try to reinject if this doesnt work wait for support.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for FiveM TZ External.
    @app_commands.command(name="fivemtzexterror", description="Sends the fixes to common error codes for FiveM TZ External.")
    async def fivemtzexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM TZ External Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for FiveM TZ Internal.
    @app_commands.command(name="fivemtzinterror", description="Sends the fixes to common error codes for FiveM TZ Internal.")
    async def fivemtzexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM TZ Internal Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Fortnite Disconnect External.
    @app_commands.command(name="fndcexterror", description="Sends the fixes to common error codes for Fortnite Disconnect External.")
    async def fndcexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Fortnite Disconnect External Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "[Common Error List](https://disconnectcheats.com/forums/forum/19-common-errors/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for HWID Spoofer Exception.
    @app_commands.command(name="hwidexceptionerror", description="Sends the fixes to common error codes for HWID Spoofer Exception.")
    async def hwidexceptionerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="HWID Spoofer Exception Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error #10000004: Make sure AV/EDR is not running and you are not infected by a rootkit.\n\n"
                            "**Error #37070000: Make sure Faceit/ESEA/Vanguard driver is not running.\n\n"
                            "**Error #3B000000: Make sure Core Isolation and Memory Integrity options are disabled in Windows Defender settings, then open cmd.exe as admin, type the following: bcdedit /set hypervisorlaunchtype off, hit Enter and restart PC. Alternatively, disable Intel VT-X / AMD SVM in your BIOS settings. Also make sure that Vanguard/Faceit/ESEA are deleted.\n\n"
                            "**Error #37100022: Hold SHIFT and restart your PC.\n\n"
                            "**Error #3C000101: Windows build number requirement is not met, the minimum supported build number is 19041.\n\n"
                            "**Error #3C000110: Multiple running instances of the launcher are not allowed.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Marvel Rivals Klar.
    @app_commands.command(name="marvelklarerror", description="Sends the fixes to common error codes for Marvel Rivals Klar.")
    async def marvelklarerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Marvel Rivals Klar Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error VGC.SYS: Uninstall Vanguard.\n\n"
                            "**Error BHDRVS.SYS: Uninstall Norton antivirus.\n\n"
                            "**Error BEDAISY.SYS: Launch Klar before you open the game not while its open.\n\n"
                            "**Error L2: Deinstall Faceit and Vanguard additionally check that your antivirus is turned off and that core isolation is turned off.\n\n"
                            "**Error l2 -(1073741637): 1.) Go to Settings and open Security > Device Security 2.) Turn off Memory Integrity.) 3. Restart your PC. 4.) Verify that Memory Integrity is still turned off. 5.) Start the loader and see if this resolves the issue.\n\n"
                            "**Error l2 -(1073741670): FACEIT AC is installed on your PC, please uninstall it.\n\n"
                            "**Error VCRUNTIME/MSVCP140.DLL: Please install vc_redist.x64.exe: https://aka.ms/vs/17/release/vc_redist.x64.exe.\n\n"
                            "**Error M1 | DEBUG ERROR 2: A temporary fix for that issue is to restart the PC every injection. If you want to fix it permanently, reinstall Windows to the PRO version.\n\n"
                            "**Error loader closing at 100%: Go to Windows settings -> date and time -> Press “SYNC NOW”. Afterwards, reinject klar.\n\n"
                            "**Error loader shows that Im banned: Please restart your computer and attempt to log in again. (Have to wait 2 hours usually).\n\n"
                            "**Error BSOD: Please run the following commands in the command prompt as Administrator and do: sfc /Scannow Once completed, Run: DISM.exe /Online /Cleanup-image /Restorehealth After that is done, restart your PC and then try to inject.\n\n"
                            "**Error 0xc0000142: The error is caused by Windows Insider being installed, which is not supported. To fix it, please reinstall Windows to the normal version..\n\n"
                            "**Error connection error 3: This is caused by a server downtime please wait for the product to be updated.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for R6 Ring1.
    @app_commands.command(name="r6ring1error", description="Sends the fixes to common error codes for R6 Ring1.")
    async def r6ring1error(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="R6 Ring1 Errors",
                description="n/a",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Rust Fluent.
    @app_commands.command(name="rustfluent", description="Sends the fixes to common error codes for Rust Fluent.")
    async def rustfluent(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Fluent Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error 0x718: Uninstall conflicting software such as Faceit / Vanguard and disable antivirus and restart.\n\n"
                            "**Error 0x717: Uninstall conflicting software such as Faceit / Vanguard and disable antivirus and restart.\n\n"
                            "**Error 0x712: 1.) Verify Rust Game Files via Steam. 2.) Restart PC. 3.) Launch Rust without Fluent till in the main menu. 4.) Close Rust and try with Fluent injected again, if that doesnt work wait for support.\n\n"
                            "**Error 0x757: 1.) Make sure fast boot is disabled in bios. 2.) make sure UAC is set to the lowest level. 3.) Check if luafv is running by typing fltmc in an admin cmd, if thats not the case run the following commands: **sc config luafv start=boot** and **sc start luafv**. 4.) Disable any kind of antivirus and make sure Faceit and Vanguard are deinstalled 5.) Restart PC and reinject, if theres still issues wait for support.\n\n",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Rust Matrix.
    @app_commands.command(name="rustmatrixerror", description="Sends the fixes to common error codes for Rust Matrix.")
    async def rustmatrixerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Matrix Errors",
                description="There are no common errors for Rust Matrix. So we recommend you to follow the setup guide step by step and if you still have issues/errors please contact support.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Rust Disconnect External.
    @app_commands.command(name="rustdcexterror", description="Sends the fixes to common error codes for Rust Disconnect External.")
    async def rustdcexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Disconnect External Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "[Common Error List](https://disconnectcheats.com/forums/forum/19-common-errors/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to display error fixes for Rust Recoil Script.
    @app_commands.command(name="rustrecoilerror", description="Sends the fixes to common error codes for Rust Recoil Script.")
    async def rustrecoilerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Recoil Script Errors",
                description="Followed the setup guide step by step and still having Issues/Errors? Please refer to the following common solutions:\n\n"
                            "**Error cannot sync:** Go to 'Change the date and time' in Windows settings and click 'Sync now', then retry.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Documentation(bot))