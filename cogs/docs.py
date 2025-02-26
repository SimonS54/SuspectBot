import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID  # Import role IDs from config

# Define a Documentation cog to provide setup guides for various products
class Documentation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in commands

    # Command to provide the setup guide for Apex Lite
    @app_commands.command(name="apexlite", description="Guide for Apex Lite")
    async def apexlite(self, interaction: discord.Interaction):
        # Extract user's role IDs for permission checking
        user_roles = [role.id for role in interaction.user.roles]
        # Check if user has any allowed role or verified customer role
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            # Create an embed with instructions for Apex Lite
            embed = discord.Embed(
                title="📘 Apex Lite Guide",
                description="Get started with Apex Lite—here’s how:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Instructions",
                value="Join this Discord to activate your key: [Apex Lite Discord](https://discord.gg/QPRuwFCXgP)\n"
                      "Your custom loader link will include full instructions.",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            # Send access denied message if user lacks proper roles
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Apex Kernaim
    @app_commands.command(name="apexkernaim", description="Guide for Apex Kernaim")
    async def apexkernaim(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Apex Kernaim Guide",
                description="Everything you need to use Apex Kernaim:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Apex Kernaim Guide](https://suspectservices.gitbook.io/kernaim-apex/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for COD Kernaim
    @app_commands.command(name="codkernaim", description="Guide for COD Kernaim")
    async def codkernaim(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 COD Kernaim Guide",
                description="Everything you need to use COD Kernaim:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[COD Kernaim Guide](https://suspectservices.gitbook.io/kernaim-mw3/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for COD RUT Unlock
    @app_commands.command(name="codrutunlock", description="Guide for COD RUT Unlock")
    async def codrutunlock(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 COD RUT Unlock Guide",
                description="Everything you need to use COD RUT Unlock:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[COD RUT Unlock Guide](https://suspectservices.gitbook.io/rut-unlock-tool/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for COD RUT UAV
    @app_commands.command(name="codrutuav", description="Guide for COD RUT UAV")
    async def codrutuav(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 COD RUT UAV Guide",
                description="Everything you need to use COD RUT UAV:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[COD RUT UAV Guide](https://suspectservices.gitbook.io/rut-uav-tool/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for EFT Exo Arena
    @app_commands.command(name="eftexoarena", description="Guide for EFT Exo Arena")
    async def eftexoarena(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 EFT Exo Arena Guide",
                description="Everything you need to use EFT Exo Arena:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[EFT Exo Arena Guide](https://suspectservices.gitbook.io/exo-eft/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for EFT Exo
    @app_commands.command(name="eftexo", description="Guide for EFT Exo")
    async def eftexo(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 EFT Exo Guide",
                description="Everything you need to use EFT Exo:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[EFT Exo Guide](https://suspectservices.gitbook.io/exo-eft/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for EFT NextCheat Full
    @app_commands.command(name="eftnextfull", description="Guide for EFT NextCheat Full")
    async def eftnextfull(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 EFT NextCheat Full Guide",
                description="Everything you need to use EFT NextCheat Full:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[EFT NextCheat Full Guide](https://suspectservices.gitbook.io/nextcheat/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for EFT NextCheat Lite
    @app_commands.command(name="eftnextlite", description="Guide for EFT NextCheat Lite")
    async def eftnextlite(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 EFT NextCheat Lite Guide",
                description="Everything you need to use EFT NextCheat Lite:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[EFT NextCheat Lite Guide](https://suspectservices.gitbook.io/nextcheat/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for FiveM HX
    @app_commands.command(name="fivemhx", description="Guide for FiveM HX")
    async def fivemhx(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 FiveM HX Guide",
                description="Everything you need to use FiveM HX:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[FiveM HX Guide](https://suspectservices.gitbook.io/hx-menu/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for FiveM TZ External
    @app_commands.command(name="fivemtzext", description="Guide for FiveM TZ External")
    async def fivemtzext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 FiveM TZ External Guide",
                description="Everything you need to use FiveM TZ External:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[FiveM TZ External Guide](https://suspectservices.gitbook.io/tz-project-fivem/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for FiveM TZ Internal
    @app_commands.command(name="fivemtzint", description="Guide for FiveM TZ Internal")
    async def fivemtzint(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 FiveM TZ Internal Guide",
                description="Everything you need to use FiveM TZ Internal:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[FiveM TZ Internal Guide](https://suspectservices.gitbook.io/tz-project-fivem/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Fortnite Disconnect External
    @app_commands.command(name="fndcext", description="Guide for Fortnite Disconnect External")
    async def fndcext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Fortnite Disconnect External Guide",
                description="Everything you need to use Fortnite Disconnect External:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Fortnite Disconnect External Guide](https://suspectservices.gitbook.io/disconnect-external-fn/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for HWID Spoofer Exception
    @app_commands.command(name="hwidexception", description="Guide for HWID Spoofer Exception")
    async def hwidexception(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 HWID Spoofer Exception Guide",
                description="Everything you need to use HWID Spoofer Exception:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[HWID Spoofer Exception Guide](https://suspectservices.gitbook.io/exception-spoofer/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Marvel Rivals Klar
    @app_commands.command(name="marvelklar", description="Guide for Marvel Rivals Klar")
    async def marvelklar(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Marvel Rivals Klar Guide",
                description="Everything you need to use Marvel Rivals Klar:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Marvel Rivals Klar Guide](https://suspectservices.gitbook.io/klar-marvel-rivals/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for R6 Ring1
    @app_commands.command(name="r6ring1", description="Guide for R6 Ring1")
    async def r6ring1(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 R6 Ring1 Guide",
                description="Everything you need to use R6 Ring1:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[R6 Ring1 Guide](https://suspectservices.gitbook.io/ring-1-r6/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Rust Fluent
    @app_commands.command(name="rustfluent", description="Guide for Rust Fluent")
    async def rustfluent(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Rust Fluent Guide",
                description="Everything you need to use Rust Fluent:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Rust Fluent Guide](https://suspectservices.gitbook.io/fluent-rust/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Rust Matrix
    @app_commands.command(name="rustmatrix", description="Guide for Rust Matrix")
    async def rustmatrix(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Rust Matrix Guide",
                description="Everything you need to use Rust Matrix:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Rust Matrix Guide](https://suspectservices.gitbook.io/matrix-rust/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Rust Disconnect External
    @app_commands.command(name="rustdcext", description="Guide for Rust Disconnect External")
    async def rustdcext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Rust Disconnect External Guide",
                description="Everything you need to use Rust Disconnect External:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Rust Disconnect External Guide](https://suspectservices.gitbook.io/rust-external/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide the setup guide for Rust Recoil Script
    @app_commands.command(name="rustrecoil", description="Guide for Rust Recoil Script")
    async def rustrecoil(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📘 Rust Recoil Script Guide",
                description="Everything you need to use Rust Recoil Script:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Documentation",
                value="[Rust Recoil Script Guide](https://suspectservices.gitbook.io/rust-recoil-script/)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Documentation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

# Setup function to register the Documentation cog with the bot
async def setup(bot):
    await bot.add_cog(Documentation(bot))  # Add the Documentation cog to the bot instance