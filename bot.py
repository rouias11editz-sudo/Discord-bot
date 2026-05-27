import discord
import os
from discord import app_commands

from commands import setup_commands
from events import setup_events

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# LOAD MODULES
# -------------------------
setup_commands(tree, client)
setup_events(client)

# -------------------------
# READY EVENT
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")
    print("bot is online 🚀")

# -------------------------
# RUN BOT
# -------------------------
client.run(os.getenv("TOKEN"))
