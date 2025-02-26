import discord
from discord import app_commands
from discord.ext import commands
import logging
import asyncio
import firebase_admin
from firebase_config import db  # Firestore database instance
from firebase_admin import credentials, firestore
from config import ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID, STATUS_CHANNEL_ID, ALLOWED_ROLE_IDS

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Autocomplete function for product names in the productstatus command
async def product_autocomplete(interaction: discord.Interaction, current: str):
    products_ref = db.collection("product_status")  # Reference to product_status collection
    products = products_ref.get()  # Fetch all product documents
    product_names = [product.id for product in products]  # Extract product IDs (names)
    # Return filtered choices based on user input
    return [
        app_commands.Choice(name=product, value=product)
        for product in product_names if current.lower() in product.lower()
    ]

# Define a Moderation cog for announcement, update, and product status commands
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance for use in commands

    # Helper method to check if the user has an allowed role
    def has_allowed_role(self, interaction: discord.Interaction):
        return any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)

    # Command to send an announcement to the target channel
    @app_commands.command(name="announce", description="Send an announcement to the target channel")
    async def announce(self, interaction: discord.Interaction):
        if not self.has_allowed_role(interaction):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Ensure command is used in the correct channel
        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated announcement channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Initiate the message creation process
        await self.initiate_message(interaction, ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID)

    # Command to send an update to the target channel
    @app_commands.command(name="update", description="Send an update to the target channel")
    async def update(self, interaction: discord.Interaction):
        if not self.has_allowed_role(interaction):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Ensure command is used in the correct channel
        if interaction.channel.id != UPDATE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated update channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Initiate the message creation process
        await self.initiate_message(interaction, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID)

    # Helper method to handle message input and confirmation
    async def initiate_message(self, interaction: discord.Interaction, command_channel_id: int, target_channel_id: int):
        embed = discord.Embed(
            title="📢 Message Creation",
            description="Type your message below—it’ll be processed once sent!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        # Check to ensure message is from the same user in the same channel
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            # Wait for user’s message with a 5-minute timeout
            message = await self.bot.wait_for('message', check=check, timeout=300)
            await message.delete()  # Clean up the input message
            embed.description = f"**Preview:**\n{message.content}"
            view = MessageControlView(target_channel_id, message.content)  # Create buttons for control
            await interaction.edit_original_response(embed=embed, view=view)
        except Exception as e:
            logger.error(f"Error in message initiation: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="Something went wrong while processing your message.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.followup.send(embed=embed)

    # Command to update a product’s status with interactive buttons
    @app_commands.command(name="productstatus", description="Update a product’s status with buttons")
    @app_commands.autocomplete(product=product_autocomplete)
    async def product_status(self, interaction: discord.Interaction, product: str):
        if not self.has_allowed_role(interaction):
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don’t have permission to use this command.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Ensure command is used in the correct channel
        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated announcement channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        doc_ref = db.collection("product_status").document(product)  # Reference to product document
        doc = doc_ref.get()  # Fetch the document

        if doc.exists:
            data = doc.to_dict()
            embed = discord.Embed(
                title=f"🔧 Update Status: {data['name']}",
                description="Select a component to update its status:",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            # Special handling for Rust Fluent with separate Fluent and Spoofer statuses
            if product.lower() == "rustfluent":
                view = FluentStatusView(product, interaction.client)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                view = StatusUpdateView(product, interaction.client)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ Product Not Found",
                description="Couldn’t find that product—check the name and try again.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

# View class for controlling message sending (Send, Cancel, Edit)
class MessageControlView(discord.ui.View):
    def __init__(self, target_channel_id: int, message_content: str):
        super().__init__(timeout=300)  # 5-minute timeout
        self.target_channel_id = target_channel_id
        self.message_content = message_content

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        target_channel = interaction.client.get_channel(self.target_channel_id)
        if target_channel:
            await target_channel.send(self.message_content)  # Send the message to the target channel
            embed = discord.Embed(
                title="✅ Success",
                description="Message sent successfully!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="Target channel not found.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.message.delete()  # Remove the original interaction message

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="❌ Canceled",
            description="Message sending has been canceled.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.message.delete()  # Remove the original interaction message

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="✏️ Edit Message",
            description="Type the new message content below.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Check to ensure message is from the same user in the same channel
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            # Wait for user’s new message with a 5-minute timeout
            new_message = await interaction.client.wait_for('message', check=check, timeout=300)
            await new_message.delete()  # Clean up the input message
            self.message_content = new_message.content  # Update the stored content
            embed = interaction.message.embeds[0]
            embed.description = f"**Preview:**\n{self.message_content}"
            await interaction.message.edit(embed=embed)  # Update the preview
            embed = discord.Embed(
                title="✅ Updated",
                description="Message content has been updated.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error in message editing: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An error occurred while editing the message.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)

# View class for updating standard product statuses
class StatusUpdateView(discord.ui.View):
    def __init__(self, product, client):
        super().__init__(timeout=60)  # 1-minute timeout
        self.product = product
        self.client = client

    # Helper method to update product status in Firestore and refresh the embed
    async def update_status(self, interaction: discord.Interaction, status: str, emoji: str):
        doc_ref = db.collection("product_status").document(self.product)
        doc_ref.update({"status": status})  # Update the status in Firestore
        embed = discord.Embed(
            title="✅ Status Updated",
            description=f"Set to {emoji} **{status}**",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await update_status_embed(self.client)  # Refresh the status overview

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

# View class for updating Rust Fluent product statuses (Fluent and Spoofer separately)
class FluentStatusView(discord.ui.View):
    def __init__(self, product, client):
        super().__init__(timeout=60)  # 1-minute timeout
        self.product = product
        self.client = client
        self.fluent_status = None  # Store Fluent status
        self.spoofer_status = None  # Store Spoofer status

    @discord.ui.button(label="Set Fluent Status", style=discord.ButtonStyle.red)
    async def set_fluent_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔧 Update Fluent Status",
            description="Select the status for Rust Fluent:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=FluentStatusButtons(self))

    @discord.ui.button(label="Set Built-In Spoofer Status", style=discord.ButtonStyle.red)
    async def set_spoofer_status(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔧 Update Built-In Spoofer Status",
            description="Select the status for the Built-In Spoofer:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=SpooferStatusButtons(self))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="✅")
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fluent_status is None and self.spoofer_status is None:
            embed = discord.Embed(
                title="❌ Nothing to Save",
                description="Please set at least one status before saving.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            return

        # Update Firestore with the selected statuses
        doc_ref = db.collection("product_status").document(self.product)
        update_data = {}
        if self.fluent_status:
            update_data["status"] = self.fluent_status
        if self.spoofer_status:
            update_data["spoofer_status"] = self.spoofer_status
        doc_ref.update(update_data)

        embed = discord.Embed(
            title="✅ Status Updated",
            description=f"Updated Rust Fluent:\n- Fluent: `{self.fluent_status or 'Unchanged'}`\n- Built-In Spoofer: `{self.spoofer_status or 'Unchanged'}`",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        confirmation_message = await interaction.original_response()
        await update_status_embed(self.client)  # Refresh the status overview
        await asyncio.sleep(3)  # Brief delay before cleanup
        await confirmation_message.delete()
        await interaction.message.delete()

# View class for setting Fluent status options
class FluentStatusButtons(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)  # 1-minute timeout
        self.parent_view = parent_view

    # Helper method to set Fluent status and return to parent view
    async def update_status(self, interaction: discord.Interaction, status: str, emoji: str):
        self.parent_view.fluent_status = status
        embed = discord.Embed(
            title="🔧 Update Status: Rust Fluent",
            description=f"Fluent status set to {emoji} **{status}**\nSelect a component to update its status:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.parent_view.client.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=self.parent_view)

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

# View class for setting Spoofer status options
class SpooferStatusButtons(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)  # 1-minute timeout
        self.parent_view = parent_view

    # Helper method to set Spoofer status and return to parent view
    async def update_status(self, interaction: discord.Interaction, status: str, emoji: str):
        self.parent_view.spoofer_status = status
        embed = discord.Embed(
            title="🔧 Update Built-In Spoofer Status",
            description=f"Built-In Spoofer status set to {emoji}\nSelect a component to update its status:",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.parent_view.client.user.avatar.url)
        await interaction.response.edit_message(embed=embed, view=self.parent_view)

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

# Function to update the product status embed in the status channel
async def update_status_embed(client):
    channel = client.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        logger.error("Status channel not found!")
        return

    embed = discord.Embed(
        title="📢 Product Status Overview",
        description="Current status of products, grouped by game:",
        color=discord.Color.red()
    )
    products = db.collection("product_status").stream()  # Stream all product documents

    # Define status emojis for consistent display
    status_emojis = {
        "Undetected": "🟢",
        "Use at Own Risk": "🟡",
        "Detected": "🔴",
        "Updating": "🔵"
    }

    games = {}
    for doc in products:
        data = doc.to_dict()
        game = data.get("game", "Uncategorized")
        status = data.get("status", "Unchanged")
        emoji = status_emojis.get(status, status) if status in status_emojis else status
        product_info = f"- {data.get('name', 'Unknown')} {emoji} (<t:{int(doc.update_time.timestamp())}:f>)"

        # Handle built-in spoofer status if present
        if "spoofer_status" in data:
            spoofer_status = data.get("spoofer_status", "Unchanged")
            if spoofer_status in status_emojis:
                spoofer_emoji = status_emojis.get(spoofer_status, "")
                spoofer_line = f"{spoofer_emoji}"
            else:
                spoofer_line = "Unchanged"
            product_info += f"\n  - Built-In Spoofer: {spoofer_line} (<t:{int(doc.update_time.timestamp())}:f>)"

        if game in games:
            games[game].append(product_info)
        else:
            games[game] = [product_info]

    # Add fields for each game with its products
    for game, products_list in games.items():
        embed.add_field(
            name=f"🎮 {game}",
            value="\n".join(products_list),
            inline=False
        )

    if not games:
        embed.add_field(
            name="ℹ️ No Products",
            value="No product statuses available yet.",
            inline=False
        )

    # Add a status key for clarity
    embed.add_field(
        name="🔑 Status Key",
        value="🟢 Undetected: Fully safe to use\n🟡 Use at Own Risk: Caution advised\n🔴 Detected: Not safe to use\n🔵 Updating: Currently in maintenance",
        inline=False
    )

    # Delay to suppress sticky bot embeds, then purge and send the new embed
    await asyncio.sleep(2)
    await channel.purge(limit=10)
    await channel.send(embed=embed)

# Cog to suppress sticky bot embeds in the status channel
class StickyBotEmbedRemover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance

    @commands.Cog.listener()
    async def on_message(self, message):
        # Suppress embeds from the sticky bot (ID: 628400349979344919) in the status channel
        if message.channel.id == STATUS_CHANNEL_ID and message.author.id == 628400349979344919:
            if message.embeds:
                await asyncio.sleep(2)  # Brief delay to ensure timing
                await message.edit(suppress=True)

# Setup function to register both cogs with the bot
async def setup(bot):
    await bot.add_cog(Moderation(bot))  # Add Moderation cog
    await bot.add_cog(StickyBotEmbedRemover(bot))  # Add StickyBotEmbedRemover cog

# Explicitly register the autocomplete function for productstatus command
Moderation.product_status.autocomplete("product")(product_autocomplete)