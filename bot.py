import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# load cogs
async def load_extensions():
    await bot.load_extension("commands")
    await bot.load_extension("events")

import asyncio
asyncio.run(load_extensions())

bot.run("YOUR_TOKEN")
