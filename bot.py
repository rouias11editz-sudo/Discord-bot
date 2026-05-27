import discord
import os
from discord import app_commands

from commands import setup_commands

# -------------------------
# INTENTS
# -------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# SHARED DATA (IMPORTANT)
# -------------------------
client.game_state = {}
client.member_game = {}
client.openrouter_key = os.getenv("OPENROUTER_API_KEY")

# -------------------------
# LOAD COMMANDS
# -------------------------
setup_commands(tree, client)

# -------------------------
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")
    print("bot is online 🚀")

# -------------------------
# RUN
# -------------------------
client.run(os.getenv("TOKEN"))
