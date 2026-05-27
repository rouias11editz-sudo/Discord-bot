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
# AI FUNCTION (GLOBAL)
# -------------------------
def ask_ai(prompt):

    headers = {
        "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
        "Content-Type": "application/json",
        "HTTP-Referer": "https://discordbot.local",
        "X-Title": "Crewmate AI"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "you are a chaotic gen z discord bot. "
                    "you speak lowercase, slang, short replies, funny tone."
                )
            },
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if r.status_code != 200:
        return f"{r.status_code} | {r.text}"

    return r.json()["choices"][0]["message"]["content"]

# -------------------------
# SHARE AI WITH EVENTS
# -------------------------
client.ask_ai = ask_ai
client.ai_enabled = False

# -------------------------
# GAME STORAGE (GLOBAL)
# -------------------------
client.game_state = {}
client.member_game = {}

# -------------------------
# SETUP COMMANDS + EVENTS
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
