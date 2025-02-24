import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="apexliteerror", description="Fixes for common Apex Lite error codes")
    async def apexliteerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Apex Lite Error Fixes",
                description="No specific error fixes available yet—contact support if you’re stuck!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="apexkernaimerror", description="Fixes for common Apex Kernaim error codes")
    async def apexkernaimerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Apex Kernaim Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 0xR / 0xD / 0xI or Infinite Loading",
                value="Boot the loader while connected to a VPN.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0xC1843",
                value="Ensure no anticheat (VGK, Faceit, EAC, BE) or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="codkernaimerror", description="Fixes for common COD Kernaim error codes")
    async def codkernaimerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 COD Kernaim Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 0xR / 0xD / 0xI or Infinite Loading",
                value="Boot the loader while connected to a VPN.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0xC1843",
                value="Ensure no anticheat (VGK, Faceit, EAC, BE) or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="codrutunlockerror", description="Fixes for common COD RUT Unlocker error codes")
    async def codrutunlockerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 COD RUT Unlocker Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 0",
                value="Redownload the launcher and launch it while connected to a VPN.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 3",
                value="Ensure no anticheat (VGK, Faceit, EAC, BE) or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="codrutuaverror", description="Fixes for common COD RUT UAV error codes")
    async def codrutuaverror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 COD RUT UAV Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 0",
                value="Redownload the launcher and launch it while connected to a VPN.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 3",
                value="Ensure no anticheat (VGK, Faceit, EAC, BE) or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eftexoarenaerror", description="Fixes for common EFT Exo Arena error codes")
    async def eftexoarenaerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 EFT Exo Arena Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 92",
                value="Disable Secure Boot in your BIOS settings.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 94",
                value="Set your BIOS to UEFI mode.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 95",
                value="Enable Virtualization in your BIOS.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eftexoerror", description="Fixes for common EFT Exo error codes")
    async def eftexoerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 EFT Exo Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 92",
                value="Disable Secure Boot in your BIOS settings.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 94",
                value="Set your BIOS to UEFI mode.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 95",
                value="Enable Virtualization in your BIOS.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eftnextfullerror", description="Fixes for common EFT NextCheat Full error codes")
    async def eftnextfullerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 EFT NextCheat Full Error Fixes",
                description="Still facing issues after the setup guide? Try this solution:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error: Cannot Start Driver",
                value="Disable Secure Boot in your BIOS settings and ensure no anticheat or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="eftnextliteerror", description="Fixes for common EFT NextCheat Lite error codes")
    async def eftnextliteerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 EFT NextCheat Lite Error Fixes",
                description="Still facing issues after the setup guide? Try this solution:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error: Cannot Start Driver",
                value="Disable Secure Boot in your BIOS settings and ensure no anticheat or antivirus is running.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fivemhxerror", description="Fixes for common FiveM HX error codes")
    async def fivemhxerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 FiveM HX Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error: steam.exe Popup",
                value="Caused by GeForce Now or Shadow PC—restart your PC and redo injection if not applicable.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error: User Couldn't Be Found",
                value="Verify registration on the HX panel; contact support if issue persists.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error: No User Found with HWID",
                value="Provide your key and user in a ticket and await support.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error: Limit Reached",
                value="Max HWID resets used—wait for support assistance.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error: ntdll.dll",
                value="1. Open FiveM without HX.\n2. Set screentype to Fullscreen.\n3. Delete data, crashes, and logs folders in FiveM Application Data.\n4. Reinject—or contact support if unresolved.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error: Instaban",
                value="1. Change menu key to something discreet.\n2. Disable 'Block Game Input' in config.\n3. Avoid rage/exploit features.\n4. Reinject—or contact support if unresolved.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fivemtzexterror", description="Fixes for common FiveM TZ External error codes")
    async def fivemtzexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 FiveM TZ External Error Fixes",
                description="No specific error fixes available yet—contact support if you’re stuck!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fivemtzinterror", description="Fixes for common FiveM TZ Internal error codes")
    async def fivemtzinterror(self, interaction: discord.Interaction):  # Fixed function name typo
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 FiveM TZ Internal Error Fixes",
                description="No specific error fixes available yet—contact support if you’re stuck!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fndcexterror", description="Fixes for common Fortnite Disconnect External error codes")
    async def fndcexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Fortnite Disconnect External Error Fixes",
                description="Still facing issues after the setup guide? Check this resource:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Error List",
                value="[Common Errors](https://disconnectcheats.com/forums/forum/19-common-errors/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hwidexceptionerror", description="Fixes for common HWID Spoofer Exception error codes")
    async def hwidexceptionerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 HWID Spoofer Exception Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error #10000004",
                value="Ensure no AV/EDR is running and your system isn’t infected by a rootkit.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error #37070000",
                value="Ensure Faceit/ESEA/Vanguard drivers aren’t running.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error #3B000000",
                value="Disable Core Isolation and Memory Integrity in Windows Defender. Run `bcdedit /set hypervisorlaunchtype off` in admin CMD, restart PC, or disable Intel VT-X/AMD SVM in BIOS. Ensure Vanguard/Faceit/ESEA are uninstalled.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error #37100022",
                value="Hold SHIFT and restart your PC.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error #3C000101",
                value="Windows build number too low—minimum supported is 19041.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error #3C000110",
                value="Multiple launcher instances detected—close all but one.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="marvelklarerror", description="Fixes for common Marvel Rivals Klar error codes")
    async def marvelklarerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Marvel Rivals Klar Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error VGC.SYS",
                value="Uninstall Vanguard.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error BHDRVS.SYS",
                value="Uninstall Norton antivirus.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error BEDAISY.SYS",
                value="Launch Klar before opening the game, not while it’s running.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error L2",
                value="Uninstall Faceit and Vanguard, disable antivirus, and turn off Core Isolation.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error L2 -(1073741637)",
                value="1. Go to Settings > Security > Device Security.\n2. Turn off Memory Integrity.\n3. Restart PC and verify it’s off.\n4. Start the loader.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error L2 -(1073741670)",
                value="Uninstall FACEIT AC from your PC.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error VCRUNTIME/MSVCP140.DLL",
                value="Install vc_redist.x64.exe: [Download](https://aka.ms/vs/17/release/vc_redist.x64.exe)",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error M1 | DEBUG ERROR 2",
                value="Temporary fix: Restart PC per injection. Permanent fix: Reinstall Windows to PRO version.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error Loader Closing at 100%",
                value="Go to Windows Settings > Date and Time > 'Sync Now', then reinject Klar.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error Loader Shows Banned",
                value="Restart PC and retry after 2 hours.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error BSOD",
                value="Run as admin in CMD: `sfc /scannow`, then `DISM.exe /Online /Cleanup-image /Restorehealth`. Restart PC and reinject.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0xc0000142",
                value="Caused by Windows Insider—reinstall to normal Windows version.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error Connection Error 3",
                value="Server downtime—wait for product update.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="r6ring1error", description="Fixes for common R6 Ring1 error codes")
    async def r6ring1error(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 R6 Ring1 Error Fixes",
                description="No common errors reported—follow the setup guide or contact support if issues persist.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rustfluenterror", description="Fixes for common Rust Fluent error codes")
    async def rustfluenterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Rust Fluent Error Fixes",
                description="Still facing issues after the setup guide? Try these solutions:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error 0x718",
                value="Uninstall Faceit/Vanguard, disable antivirus, and restart.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0x717",
                value="Uninstall Faceit/Vanguard, disable antivirus, and restart.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0x712",
                value="1. Verify Rust files via Steam.\n2. Restart PC.\n3. Launch Rust to main menu without Fluent.\n4. Close Rust and reinject—or contact support.",
                inline=False
            )
            embed.add_field(
                name="⚠️ Error 0x757",
                value="1. Disable Fast Boot in BIOS.\n2. Set UAC to lowest level.\n3. Check if 'luafv' is running (`fltmc` in admin CMD); if not, run `sc config luafv start=boot` and `sc start luafv`.\n4. Disable antivirus and uninstall Faceit/Vanguard.\n5. Restart and reinject—or contact support.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rustmatrixerror", description="Fixes for common Rust Matrix error codes")
    async def rustmatrixerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Rust Matrix Error Fixes",
                description="No common errors reported—follow the setup guide or contact support if issues persist.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rustdcexterror", description="Fixes for common Rust Disconnect External error codes")
    async def rustdcexterror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Rust Disconnect External Error Fixes",
                description="Still facing issues after the setup guide? Check this resource:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Error List",
                value="[Common Errors](https://disconnectcheats.com/forums/forum/19-common-errors/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rustrecoilerror", description="Fixes for common Rust Recoil Script error codes")
    async def rustrecoilerror(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🔧 Rust Recoil Script Error Fixes",
                description="Still facing issues after the setup guide? Try this solution:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⚠️ Error: Cannot Sync",
                value="Go to Windows Settings > 'Change date and time' > 'Sync now', then retry.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Error Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Error(bot))