import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieve the Discord bot token from environment variables

# Configure bot intents to enable necessary permissions
intents = discord.Intents.default()
intents.message_content = True  # Allow the bot to read message content
intents.members = True  # Allow the bot to access member information

# Initialize the bot with command prefixes and intents
bot = commands.Bot(command_prefix=["/", "!"], intents=intents)

# Function to load all cog extensions dynamically
async def load_cogs():
    # List of cogs to load from the 'cogs' directory
    for cog in ["commands", "support", "stats", "moderation", "payment", "docs", "epvp", "message_filter", "error"]:
        await bot.load_extension(f"cogs.{cog}")  # Load each cog using its module path

# Event handler for when the bot is fully connected and ready
@bot.event
async def on_ready():
    await load_cogs()  # Load all cogs when the bot starts
    await bot.tree.sync()  # Sync slash commands with Discord
    print(f'Logged in as {bot.user.name}')  # Log the bot's successful login

# Start the bot with the provided token
bot.run(TOKEN)