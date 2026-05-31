import discord
from discord.ext import commands
import asyncio

# ───── INTENTS ─────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ───── READY EVENT ─────
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ───── LOAD EXTENSIONS ─────
async def load_extensions():
    try:
        await bot.load_extension("commands")
        print("Loaded commands.py")

        await bot.load_extension("events")
        print("Loaded events.py")

    except Exception as e:
        print(f"Error loading extensions: {e}")

# ───── MAIN STARTUP ─────
async def main():
    async with bot:
        await load_extensions()
        await bot.start("YOUR_BOT_TOKEN")  # 🔴 REPLACE THIS

# ───── RUN ─────
asyncio.run(main())
