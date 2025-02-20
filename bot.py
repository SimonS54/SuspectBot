import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["/", "!"], intents=intents)

async def load_cogs():
    for cog in ["commands", "support", "stats", "moderation", "payment", "docs", "epvp"]:
        await bot.load_extension(f"cogs.{cog}")

@bot.event
async def on_ready():
    await load_cogs()
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

bot.run(TOKEN)
