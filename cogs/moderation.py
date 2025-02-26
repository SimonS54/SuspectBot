import discord
from discord import app_commands
from discord.ext import commands
import logging
import asyncio
import firebase_admin
from firebase_config import db
from firebase_admin import credentials, firestore
from config import ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID, STATUS_CHANNEL_ID, ALLOWED_ROLE_IDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    def has_allowed_role(self, interaction: discord.Interaction):
        return any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)

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

        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated announcement channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.initiate_message(interaction, ANNOUNCE_COMMAND_CHANNEL_ID, ANNOUNCE_TARGET_CHANNEL_ID)

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

        if interaction.channel.id != UPDATE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated update channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await self.initiate_message(interaction, UPDATE_COMMAND_CHANNEL_ID, UPDATE_TARGET_CHANNEL_ID)

    async def initiate_message(self, interaction: discord.Interaction, command_channel_id: int, target_channel_id: int):
        embed = discord.Embed(
            title="📢 Message Creation",
            description="Type your message below—it’ll be processed once sent!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            message = await self.bot.wait_for('message', check=check, timeout=300)
            await message.delete()
            embed.description = f"**Preview:**\n{message.content}"
            view = MessageControlView(target_channel_id, message.content)
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

        if interaction.channel.id != ANNOUNCE_COMMAND_CHANNEL_ID:
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Please use this command in the designated announcement channel.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        doc_ref = db.collection("product_status").document(product)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            embed = discord.Embed(
                title=f"🔧 Update Status: {data['name']}",
                description="Select a component to update its status:",
                color=discord.Color.red()
            )
            embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.bot.user.avatar.url)
            # For Rust Fluent, send a regular message so interactions can be edited and later deleted
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

class MessageControlView(discord.ui.View):
    def __init__(self, target_channel_id: int, message_content: str):
        super().__init__(timeout=300)
        self.target_channel_id = target_channel_id
        self.message_content = message_content

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        target_channel = interaction.client.get_channel(self.target_channel_id)
        if target_channel:
            await target_channel.send(self.message_content)
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
        await interaction.message.delete()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="❌")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="❌ Canceled",
            description="Message sending has been canceled.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.message.delete()

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="✏️ Edit Message",
            description="Type the new message content below.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=interaction.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            new_message = await interaction.client.wait_for('message', check=check, timeout=300)
            await new_message.delete()
            self.message_content = new_message.content
            embed = interaction.message.embeds[0]
            embed.description = f"**Preview:**\n{self.message_content}"
            await interaction.message.edit(embed=embed)
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

class StatusUpdateView(discord.ui.View):
    def __init__(self, product, client):
        super().__init__(timeout=60)
        self.product = product
        self.client = client

    async def update_status(self, interaction: discord.Interaction, status: str, emoji: str):
        doc_ref = db.collection("product_status").document(self.product)
        doc_ref.update({"status": status})
        embed = discord.Embed(
            title="✅ Status Updated",
            description=f"Set to {emoji} **{status}**",
            color=discord.Color.red()
        )
        embed.set_footer(text="Powered by SuspectServices • Moderation Section", icon_url=self.client.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
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

class FluentStatusView(discord.ui.View):
    def __init__(self, product, client):
        super().__init__(timeout=60)
        self.product = product
        self.client = client
        self.fluent_status = None
        self.spoofer_status = None

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
        await update_status_embed(self.client)
        await asyncio.sleep(3)
        await confirmation_message.delete()
        await interaction.message.delete()

class FluentStatusButtons(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)
        self.parent_view = parent_view

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

class SpooferStatusButtons(discord.ui.View):
    def __init__(self, parent_view):
        super().__init__(timeout=60)
        self.parent_view = parent_view

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
    products = db.collection("product_status").stream()

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

        # If a built-in spoofer status is present, display only its emoji.
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

    embed.add_field(
        name="🔑 Status Key",
        value="🟢 Undetected: Fully safe to use\n🟡 Use at Own Risk: Caution advised\n🔴 Detected: Not safe to use\n🔵 Updating: Currently in maintenance",
        inline=False
    )

    # Increase the delay by waiting a bit before purging to ensure the sticky embed is suppressed.
    await asyncio.sleep(2)
    await channel.purge(limit=10)
    await channel.send(embed=embed)

class StickyBotEmbedRemover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # If the message is from the sticky bot (ID: 628400349979344919) and contains embeds,
        # wait a bit before suppressing them.
        if message.channel.id == STATUS_CHANNEL_ID and message.author.id == 628400349979344919:
            if message.embeds:
                await asyncio.sleep(2)
                await message.edit(suppress=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(StickyBotEmbedRemover(bot))

Moderation.product_status.autocomplete("product")(product_autocomplete)