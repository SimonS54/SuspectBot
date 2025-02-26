import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS, VERIFIED_CUSTOMER_ROLE_ID

# Define a Support cog to handle support-related commands for the bot
class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in commands

    # Command to provide a support tool for troubleshooting
    @app_commands.command(name="supporttool", description="Get our Support Tool to troubleshoot issues quickly")
    async def support_tool(self, interaction: discord.Interaction):
        # Extract user's role IDs for permission checking
        user_roles = [role.id for role in interaction.user.roles]
        # Check if user has any allowed role or verified customer role
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            # Create an embed with support tool instructions
            embed = discord.Embed(
                title="🔧 Support Tool Assistant",
                description="Save time and solve issues faster with our automated Support Tool! Follow these quick steps:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📋 Instructions",
                value="- Download the tool below\n- Run it and check for any **red** flags\n- Ensure all options show **green**\n- Retry your product\n- Still stuck? Our staff is here to help!",
                inline=False
            )
            embed.add_field(
                name="⬇️ Download",
                value="[Support Tool](https://mega.nz/file/ioJQ3TAK#khDxBBZ0_LiX__6zEnfr2N6PG1_HDuv271J5rFus7yQ)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            # Send access denied message if user lacks proper roles
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to guide users on setting up AnyDesk for remote support
    @app_commands.command(name="anydesk", description="Set up AnyDesk for remote support assistance")
    async def anydesk(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        # Restrict this command to users with ALLOWED_ROLE_IDS only
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="🖥️ Remote Support with AnyDesk",
                description="Let our team fix your issue directly through remote access - perfect for quick resolutions!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="🚀 How It Works",
                value="- Download AnyDesk below\n- Install it on your PC\n- Share your **access code** with staff\n- Sit back while we assist you",
                inline=False
            )
            embed.add_field(
                name="⬇️ Get AnyDesk",
                value="[Download AnyDesk](https://anydesk.com/en-gb)",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to assist users in enabling/disabling virtualization
    @app_commands.command(name="virtualization", description="Guide to enable/disable Virtualization")
    async def virtualization(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        # Check permissions for both allowed roles and verified customers
        if not any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            return await interaction.response.send_message(embed=embed)

        # Initial embed for CPU selection
        embed = discord.Embed(
            title="🖥️ Virtualization Setup Guide",
            description="Need to toggle Virtualization? Select your CPU type below to get started!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)

        # View class for CPU selection buttons (AMD/Intel)
        class CPUSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)  # Set timeout to 60 seconds

            @discord.ui.button(label="AMD", style=discord.ButtonStyle.red, emoji="🔴")
            async def amd_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **AMD**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=AMDView())

            @discord.ui.button(label="Intel", style=discord.ButtonStyle.red, emoji="🔵")
            async def intel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **Intel**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=IntelView())

        # View class for AMD motherboard selection
        class AMDView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (AMD)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=cnSgkEK8CWw)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (AMD)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=vyjWTXQW9x8)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (AMD)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=dpKGbtWl9Mo)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        # View class for Intel motherboard selection
        class IntelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (Intel)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=bQDVvhtBeO4)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (Intel)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=9xj-pO2822w)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (Intel)** Virtualization Guide: [Watch Tutorial](https://www.youtube.com/watch?v=cLouTP0kM2I)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        await interaction.response.send_message(embed=embed, view=CPUSelectView())

    # Command to guide users on enabling/disabling TPM
    @app_commands.command(name="tpm", description="Guide to enable/disable TPM")
    async def tpm(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if not any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(
            title="🔒 TPM Configuration Guide",
            description="Adjust your TPM settings easily - select your CPU type to begin!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)

        class CPUSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="AMD", style=discord.ButtonStyle.red, emoji="🔴")
            async def amd_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **AMD**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=AMDView())

            @discord.ui.button(label="Intel", style=discord.ButtonStyle.red, emoji="🔵")
            async def intel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **Intel**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=IntelView())

        class AMDView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (AMD)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=3qbU8T7MSxM)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (AMD)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=iTDuya1HYz4)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (AMD)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=DEnB9g4mCOQ)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        class IntelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (Intel)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=0rFrgPT1O9s)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (Intel)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=8cc0QVDqcmc)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (Intel)** TPM Guide: [Watch Tutorial](https://www.youtube.com/watch?v=_FQvLX9GPQw)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        await interaction.response.send_message(embed=embed, view=CPUSelectView())

    # Command to guide users on enabling/disabling Secure Boot
    @app_commands.command(name="secureboot", description="Guide to enable/disable Secure Boot")
    async def secureboot(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if not any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            return await interaction.response.send_message(embed=embed)

        embed = discord.Embed(
            title="🔐 Secure Boot Configuration",
            description="Toggle Secure Boot with ease - choose your CPU type to proceed!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)

        class CPUSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="AMD", style=discord.ButtonStyle.red, emoji="🔴")
            async def amd_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **AMD**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=AMDView())

            @discord.ui.button(label="Intel", style=discord.ButtonStyle.red, emoji="🔵")
            async def intel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You chose **Intel**! Pick your motherboard brand below:"
                await interaction.response.edit_message(embed=embed, view=IntelView())

        class AMDView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (AMD)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=RSBbfLGRWN0&t=78s)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (AMD)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=PPm4NbnAMLQ)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (AMD)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=lswRu0U1X9w)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        class IntelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.red)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **ASUS (Intel)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=CbgX_Ek76XA)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.red)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **MSI (Intel)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=XaJ-qNqzDIM)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.red)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "🔧 **Gigabyte (Intel)** Secure Boot Guide: [Watch Tutorial](https://www.youtube.com/watch?v=63t2TYHmBgc)\n\n*Note: BIOS layouts may differ - ask for help if needed!*"
                await interaction.response.edit_message(embed=embed, view=None)

        await interaction.response.send_message(embed=embed, view=CPUSelectView())

    # Command to help users disable Core Isolation
    @app_commands.command(name="coreisolation", description="Disable Core Isolation for compatibility")
    async def coreisolation(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="🛡️ Core Isolation Fix",
                description="Core Isolation can interfere with some products. Disable it quickly with this guide!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="📖 Tutorial",
                value="[Disable Core Isolation](https://www.youtube.com/watch?v=AEjt7daC60g)",
                inline=False
            )
            embed.add_field(
                name="ℹ️ Why?",
                value="This security feature might block certain product functions - turn it off if prompted!",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Command to provide Visual C++ and DirectX installation links
    @app_commands.command(name="vc64", description="Install Visual C++ and DirectX dependencies")
    async def vc64(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS + VERIFIED_CUSTOMER_ROLE_ID for role_id in user_roles):
            embed = discord.Embed(
                title="📦 Dependency Installer",
                description="Ensure product compatibility by installing these essential components!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="⬇️ Downloads",
                value="- [Visual C++ Redistributables](https://aka.ms/vs/17/release/vc_redist.x64.exe)\n- [DirectX Runtime](https://www.microsoft.com/en-us/download/details.aspx?id=35)",
                inline=False
            )
            embed.add_field(
                name="ℹ️ Important",
                value="These are often pre-installed by games, but install them here if asked for!",
                inline=False
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Support Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)

# Setup function to add the Support cog to the bot
async def setup(bot):
    await bot.add_cog(Support(bot))  # Register the Support cog with the bot instance