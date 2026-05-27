import discord
import os
import requests
from discord import app_commands

from commands import setup_commands
from events import setup_events

# -------------------------
# INTENTS
# -------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# AI FUNCTION
# -------------------------
def ask_ai(prompt):

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "you are a chaotic gen z discord bot, short funny replies"
                    },
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )

        if r.status_code != 200:
            return f"AI ERROR {r.status_code}"

        return r.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI FAILED: {e}"

# -------------------------
# GLOBAL STATE
# -------------------------
client.ask_ai = ask_ai
client.ai_enabled = False
client.game_state = {}
client.member_game = {}

# -------------------------
# LOAD MODULES
# -------------------------
setup_commands(tree, client)
setup_events(client)

# -------------------------
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()  # GLOBAL SYNC FIX
    print(f"logged in as {client.user}")
    print("commands synced")

# -------------------------
# RUN
# -------------------------
client.run(os.getenv("TOKEN"))
