import discord
from discord import app_commands
from discord.ext import commands
from config import ALLOWED_ROLE_IDS

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to show the support tool.
    @app_commands.command(name="supporttool", description="Shows the support tool.")
    async def support_tool(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="Support Tool",
                description="To save our staff time and frustration, please take five minutes to download our SupportTool and make sure there are no red options. Then, try starting/injecting the product again. If it still doesn't work, please wait for a staff member to help.\n\n"
                            "Download and ensure all settings are **Green**: [Support Tool](https://mega.nz/file/ioJQ3TAK#khDxBBZ0_LiX__6zEnfr2N6PG1_HDuv271J5rFus7yQ)",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Command to show AnyDesk instructions.
    @app_commands.command(name="anydesk", description="Instructions for using AnyDesk for remote support.")
    async def anydesk(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            embed = discord.Embed(
                title="AnyDesk",
                description="It often takes less time to fix specific Issues if support can remotely connect to your Pc and install your Product for you. This can be especially useful for new Users.\n\n"
                            "Please download AnyDesk: [AnyDesk](https://anydesk.com/en-gb)\n"
                            "Once installed, provide your **access code**.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.")

    # Virtualization Command with Interactive Buttons
    @app_commands.command(name="virt", description="Instructions for enabling/disabling Virtualization.")
    async def virt(self, interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        if not any(role_id in ALLOWED_ROLE_IDS for role_id in user_roles):
            return await interaction.response.send_message("❌ You do not have permission to use this command.")

        embed = discord.Embed(
            title="Virtualization Guide",
            description="Your product or assisting staff member might tell you disable virtualization. Follow these steps below to enable or disable virtualization on your system. Choose your CPU type to continue.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices")

        # Initial CPU Selection View
        class CPUSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="AMD", style=discord.ButtonStyle.red)
            async def amd_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You selected **AMD**. Now, choose your motherboard brand. If your specifc brand is not listed, please ask for help."
                await interaction.response.edit_message(embed=embed, view=AMDView())

            @discord.ui.button(label="Intel", style=discord.ButtonStyle.blurple)
            async def intel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "You selected **Intel**. Now, choose your motherboard brand. If your specifc brand is not listed, please ask for help."
                await interaction.response.edit_message(embed=embed, view=IntelView())

        # AMD Motherboard Selection View
        class AMDView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.gray)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on ASUS (AMD): [Guide](https://www.youtube.com/watch?v=cnSgkEK8CWw)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.gray)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on MSI (AMD): [Guide](https://www.youtube.com/watch?v=vyjWTXQW9x8)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.gray)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on Gigabyte (AMD): [Guide](https://www.youtube.com/watch?v=dpKGbtWl9Mo)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

        # Intel Motherboard Selection View
        class IntelView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)

            @discord.ui.button(label="ASUS", style=discord.ButtonStyle.gray)
            async def asus_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on ASUS (Intel): [Guide](https://www.youtube.com/watch?v=bQDVvhtBeO4)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="MSI", style=discord.ButtonStyle.gray)
            async def msi_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on MSI (Intel): [Guide](https://www.youtube.com/watch?v=9xj-pO2822w)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

            @discord.ui.button(label="Gigabyte", style=discord.ButtonStyle.gray)
            async def gigabyte_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed.description = "Enable/Disable Virtualization on Gigabyte (Intel): [Guide](https://www.youtube.com/watch?v=cLouTP0kM2I)\n\n Please note that the BIOS layout may vary. In the case of you not being able to find the option, please ask for guidance."
                await interaction.response.edit_message(embed=embed, view=None)

        # Send initial CPU selection message
        await interaction.response.send_message(embed=embed, view=CPUSelectView())

    # Command to show instructions for enabling/disabling TPM.
    @app_commands.command(name="tpm", description="Instructions for enabling/disabling TPM.")
    async def tpm(self, interaction: discord.Interaction):
        message = "Enable/Disable TPM: [Guide](https://www.youtube.com/watch?v=sCKKjaZjqGM)"
        await interaction.response.send_message(message)

    # Command to show instructions for enabling/disabling Core Isolation.
    @app_commands.command(name="coreisolation", description="Shows instructions to disable Core Isolation.")
    async def coreisolation(self, interaction: discord.Interaction):
        """Explains how to disable Core Isolation."""
        message = "Disable Core Isolation: [Guide](https://www.youtube.com/watch?v=AEjt7daC60g)"
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Support(bot))
