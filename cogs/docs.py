import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

class Documentation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to send the link to the Apex Lite documentation.
    @app_commands.command(name="apexlite", description="Sends the link to the Apex Lite documentation.")
    async def apexlite(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Apex Lite",
                description="Join this discord to activate your key: https://discord.gg/QPRuwFCXgP\n\n"
                            "Instructions will be sent with your custom loader link",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Apex Kernaim documentation.
    @app_commands.command(name="apexkernaim", description="Sends the link to the Apex Kernaim documentation.")
    async def apexkernaim(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Apex Kernaim",
                description="[Apex Kernaim Documentation](https://suspectservices.gitbook.io/kernaim-apex/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the COD Kernaim documentation.
    @app_commands.command(name="codkernaim", description="Sends the link to the COD Kernaim documentation.")
    async def codkernaim(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD Kernaim",
                description="[COD Kernaim Documentation](https://suspectservices.gitbook.io/kernaim-mw3/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the COD RUT Unlocker documentation.
    @app_commands.command(name="codrutunlock", description="Sends the link to the COD RUT Unlock documentation.")
    async def codrutunlock(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD RUT Unlock",
                description="[COD RUT Unlock Documentation](https://suspectservices.gitbook.io/rut-unlock-tool/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the COD RUT UAV documentation.
    @app_commands.command(name="codrutuav", description="Sends the link to the COD RUT UAV documentation.")
    async def codrutuav(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="COD RUT UAV",
                description="[COD RUT UAV Documentation](https://suspectservices.gitbook.io/rut-uav-tool/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the EFT Exo Arena documentation.
    @app_commands.command(name="eftexoarena", description="Sends the link to the EFT Exo Arena documentation.")
    async def eftexoarena(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT Exo Arena",
                description="[EFT Exo Arena Documentation](https://suspectservices.gitbook.io/exo-eft/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the EFT Exo documentation.
    @app_commands.command(name="eftexo", description="Sends the link to the EFT Exo documentation.")
    async def eftexo(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT Exo",
                description="[EFT Exo Documentation](https://suspectservices.gitbook.io/exo-eft/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the EFT NextCheat Full documentation.
    @app_commands.command(name="eftnextfull", description="Sends the link to the EFT NextCheat Full documentation.")
    async def eftnextfull(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT NextCheat Full",
                description="[EFT NextCheat Full Documentation](https://suspectservices.gitbook.io/nextcheat/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the EFT NextCheat Lite documentation.
    @app_commands.command(name="eftnextlite", description="Sends the link to the EFT NextCheat Lite documentation.")
    async def eftnextlite(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="EFT NextCheat Lite",
                description="[EFT NextCheat Lite Documentation](https://suspectservices.gitbook.io/nextcheat/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the FiveM HX documentation.
    @app_commands.command(name="fivemhx", description="Sends the link to the FiveM HX documentation.")
    async def fivemhx(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM HX",
                description="[FiveM HX Documentation](https://suspectservices.gitbook.io/hx-menu/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the FiveM TZ External documentation.
    @app_commands.command(name="fivemtzext", description="Sends the link to the FiveM TZ External documentation.")
    async def fivemtzext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM TZ External",
                description="[FiveM TZ External Documentation](https://suspectservices.gitbook.io/tz-project-fivem/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the FiveM TZ Internal documentation.
    @app_commands.command(name="fivemtzint", description="Sends the link to the FiveM TZ Internal documentation.")
    async def fivemtzint(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="FiveM TZ Internal",
                description="[FiveM TZ Internal Documentation](https://suspectservices.gitbook.io/tz-project-fivem/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Fortnite Disconnect External documentation.
    @app_commands.command(name="fndcext", description="Sends the link to the Fortnite Disconnect External documentation.")
    async def fndcext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Fortnite Disconnect External",
                description="[Fortnite Disconnect External Documentation](https://suspectservices.gitbook.io/disconnect-external-fn/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the HWID Spoofer Exception documentation.
    @app_commands.command(name="hwidexception", description="Sends the link to the HWID Spoofer Exception documentation.")
    async def hwidexception(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="HWID Spoofer Exception",
                description="[HWID Spoofer Exception Documentation](https://suspectservices.gitbook.io/exception-spoofer/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Marvel Rivals Klar documentation.
    @app_commands.command(name="marvelklar", description="Sends the link to the Marvel Rivals Klar documentation.")
    async def marvelklar(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Marvel Rivals Klar",
                description="[Marvel Rivals Klar Documentation](https://suspectservices.gitbook.io/klar-marvel-rivals/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the R6 Ring1 documentation.
    @app_commands.command(name="r6ring1", description="Sends the link to the R6 Ring1 documentation.")
    async def r6ring1(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="R6 Ring1",
                description="[R6 Ring1 Documentation](https://suspectservices.gitbook.io/ring-1-r6/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Rust Fluent documentation.
    @app_commands.command(name="rustfluent", description="Sends the link to the Rust Fluent documentation.")
    async def rustfluent(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Fluent",
                description="[Rust Fluent Documentation](https://suspectservices.gitbook.io/fluent-rust/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Rust Matrix documentation.
    @app_commands.command(name="rustmatrix", description="Sends the link to the Rust Matrix documentation.")
    async def rustmatrix(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Matrix",
                description="[Rust Matrix Documentation](https://suspectservices.gitbook.io/matrix-rust/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Rust Disconnect External documentation.
    @app_commands.command(name="rustdcext", description="Sends the link to the Rust Disconnect External documentation.")
    async def rustdcext(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Disconnect External",
                description="[Rust Disconnect External Documentation](https://suspectservices.gitbook.io/rust-external/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to send the link to the Rust Recoil Script documentation.
    @app_commands.command(name="rustrecoil", description="Sends the link to the Rust Recoil Script documentation.")
    async def rustrecoil(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="Rust Recoil Script",
                description="[Rust Recoil Script Documentation](https://suspectservices.gitbook.io/rust-recoil-script/)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Documentation(bot))
