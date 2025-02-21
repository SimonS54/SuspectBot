import discord
from discord import app_commands
from discord.ext import commands
import logging
import firebase_admin
from firebase_config import db
from firebase_admin import credentials, firestore
from config import ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID, STATUS_CHANNEL_ID, ALLOWED_ROLE_IDS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Autocomplete function for product names
async def product_autocomplete(interaction: discord.Interaction, current: str):
    products_ref = db.collection("product_status")
    products = products_ref.get()
    product_names = [product.id for product in products]
    return [
        app_commands.Choice(name=product, value=product)
        for product in product_names if current.lower() in product.lower()
    ]

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check if the user has the required role
    def has_allowed_role(self, interaction: discord.Interaction):
        return any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)

    # Command to initiate an announcement message
    @app_commands.command(name="announce", description="Initiates an announcement message.")
    async def announce(self, interaction: discord.Interaction):
        if not self.has_allowed_role(interaction):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
            return

        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            await interaction.response.send_message("❌ You cannot use this command in this channel.", ephemeral=True)
            return

        await self.initiate_message(interaction, ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID)

    # Command to initiate an update message
    @app_commands.command(name="update", description="Initiates an update message.")
    async def update(self, interaction: discord.Interaction):
        if not self.has_allowed_role(interaction):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
            return

        if interaction.channel.id != UPDATE_COMMAND_CHANNEL_ID:
            await interaction.response.send_message("❌ You cannot use this command in this channel.", ephemeral=True)
            return

        await self.initiate_message(interaction, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID)

    # Helper method to initiate a message process
    async def initiate_message(self, interaction: discord.Interaction, command_channel_id: int, target_channel_id: int):
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

    # Command to update product status via buttons with autocomplete
    @app_commands.command(name="productstatus", description="Change the status of a product.")
    @app_commands.autocomplete(product=product_autocomplete)
    async def product_status(self, interaction: discord.Interaction, product: str):
        if not self.has_allowed_role(interaction):
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
            return

        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            await interaction.response.send_message("❌ You cannot use this command in this channel.", ephemeral=True)
            return

        doc_ref = db.collection("product_status").document(product)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            embed = discord.Embed(
                title=f"Change Status for {data['name']}",
                description="Select a button below to update the product status:",
                color=discord.Color.red()
            )
            view = StatusUpdateView(product, interaction.client)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Product not found. Please check the name.", ephemeral=True)

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

class StatusUpdateView(discord.ui.View):
    def __init__(self, product, client):
        super().__init__(timeout=60)
        self.product = product
        self.client = client

    # Helper method to update the status of a product
    async def update_status(self, interaction: discord.Interaction, status: str, emoji: str):
        doc_ref = db.collection("product_status").document(self.product)
        doc_ref.update({"status": status})
        await interaction.response.send_message(f"✅ Status updated to {emoji} {status}", ephemeral=True)
        await update_status_embed(self.client)

    @discord.ui.button(label="Undetected", style=discord.ButtonStyle.green, emoji="🟢")
    async def undetected_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_status(interaction, "Undetected", "🟢")

    @discord.ui.button(label="Use at Own Risk", style=discord.ButtonStyle.blurple, emoji="🟡")
    async def risk_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_status(interaction, "Use at Own Risk", "🟡")

    @discord.ui.button(label="Detected", style=discord.ButtonStyle.red, emoji="🔴")
    async def detected_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_status(interaction, "Detected", "🔴")

    @discord.ui.button(label="Updating", style=discord.ButtonStyle.gray, emoji="🔵")
    async def updating_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.update_status(interaction, "Updating", "🔵")

# Helper method to update the status embed
async def update_status_embed(client):
    channel = client.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        logger.error("Status channel not found!")
        return

    embed = discord.Embed(title="📢 Product Status", color=discord.Color.red())
    products = db.collection("product_status").stream()

    status_emojis = {
        "Undetected": "🟢",
        "Use at Own Risk": "🟡",
        "Detected": "🔴",
        "Updating": "🔵"
    }

    # Add a field for each product
    for doc in products:
        data = doc.to_dict()
        status = data["status"]
        emoji = status_emojis.get(status, "")
        embed.add_field(
            name=f"{data['name']} {emoji}",
            value=f"**Status:** {status}\n**Last Updated:** <t:{int(doc.update_time.timestamp())}:f>",
            inline=False
        )

    await channel.purge(limit=10)
    await channel.send(embed=embed)

class StickyBotEmbedRemover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Remove sticky bot embeds from the status channel
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == STATUS_CHANNEL_ID and message.author.id == 628400349979344919:
            if message.embeds:
                await message.edit(suppress=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(StickyBotEmbedRemover(bot))

# Bind the autocomplete function to the productstatus command
Moderation.product_status.autocomplete("product")(product_autocomplete)