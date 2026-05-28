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
# BOT DATA
# -------------------------
client.ai_enabled = False
client.game_state = {}
client.member_game = {}

# -------------------------
# AI FUNCTION
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
                    "you speak lowercase, funny, unserious, "
                    "short replies, slang, chaotic energy."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if r.status_code != 200:
            return "ai broke itself ngl 💀"

        return r.json()["choices"][0]["message"]["content"]

    except:
        return "openrouter exploded 😭"

# make AI usable in other files
client.ask_ai = ask_ai

# -------------------------
# LOAD COMMANDS / EVENTS
# -------------------------
setup_commands(tree, client)
setup_events(client)

# -------------------------
# READY EVENT
# -------------------------
@client.event
async def on_ready():

    try:

        synced = await tree.sync()

        print("===================================")
        print(f"logged in as {client.user}")
        print(f"synced {len(synced)} slash commands")
        print("bot is online 🔥")
        print("===================================")

    except Exception as e:

        print("FAILED TO SYNC COMMANDS")
        print(e)

# -------------------------
# RUN BOT
# -------------------------
client.run(os.getenv("TOKEN"))
