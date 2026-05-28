import discord
from discord import app_commands
import asyncio

from events import setup_events
from database import init_db

# -------------------------
# BOT SETUP
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

client.tree = tree

# -------------------------
# AI SYSTEM FLAG
# -------------------------
client.ai_enabled = False

# Dummy AI function (replace if you already have one)
def ask_ai(prompt):
    return "ai response placeholder"

client.ask_ai = ask_ai


# -------------------------
# READY EVENT
# -------------------------
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    # INIT DATABASE (IMPORTANT)
    await init_db()

    # LOAD EVENTS
    setup_events(client)

    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print("Slash sync error:", e)


# -------------------------
# RUN BOT
# -------------------------
client.run("YOUR_BOT_TOKEN_HERE")
