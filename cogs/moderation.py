import discord
from discord import app_commands
from discord.ext import commands
import logging
from config import ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID, ALLOWED_ROLE_IDS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to initiate an announcement message
    @app_commands.command(name="announce", description="Initiates an announcement message.")
    async def announce(self, interaction: discord.Interaction):
        await self.initiate_message(interaction, ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID)

    # Command to initiate an update message
    @app_commands.command(name="update", description="Initiates an update message.")
    async def update(self, interaction: discord.Interaction):
        await self.initiate_message(interaction, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID)

    # Helper method to initiate a message process
    async def initiate_message(self, interaction: discord.Interaction, command_channel_id: int, target_channel_id: int):
        if interaction.channel.id != command_channel_id:
            await interaction.response.send_message("❌ You cannot use this command in this channel.")
            return

        embed = discord.Embed(
            title="Announcement/Update initiated",
            description="Please type your message. Once you send it, it will be processed.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            message = await self.bot.wait_for('message', check=check, timeout=300)
            await message.delete()
            embed.description = message.content
            view = MessageControlView(target_channel_id, message.content)
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            logger.error(f"Error in message initiation: {e}")
            await interaction.followup.send("An error occurred while processing the message.")

class MessageControlView(discord.ui.View):
    def __init__(self, target_channel_id: int, message_content: str):
        super().__init__(timeout=300)
        self.target_channel_id = target_channel_id
        self.message_content = message_content

    # Button to confirm and send the message
    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        target_channel = interaction.client.get_channel(self.target_channel_id)
        if target_channel:
            await target_channel.send(self.message_content)
            await interaction.response.send_message("Message sent successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Target channel not found.", ephemeral=True)
        await interaction.message.delete()

    # Button to cancel the message sending process
    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Message sending canceled.", ephemeral=True)
        await interaction.message.delete()

    # Button to edit the message content
    @discord.ui.button(label="✏️", style=discord.ButtonStyle.blurple)
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Please type the new message content.", ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            new_message = await interaction.client.wait_for('message', check=check, timeout=300)
            await new_message.delete()
            self.message_content = new_message.content
            embed = interaction.message.embeds[0]
            embed.description = self.message_content
            await interaction.message.edit(embed=embed)
            await interaction.followup.send("Message content updated.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in message editing: {e}")
            await interaction.followup.send("An error occurred while editing the message.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))