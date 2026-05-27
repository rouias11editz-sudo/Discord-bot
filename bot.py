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
                    "content": "you are a chaotic gen z discord bot."
                },
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )

        if r.status_code != 200:
            return f"AI ERROR: {r.status_code}"

        return r.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI BROKE: {e}"

# -------------------------
# SAFE GLOBALS (IMPORTANT)
# -------------------------
client.ask_ai = ask_ai
client.ai_enabled = False
client.game_state = {}
client.member_game = {}

# -------------------------
# LOAD SYSTEMS (SAFE WRAPPED)
# -------------------------
try:
    setup_commands(tree, client)
    print("✅ commands loaded")
except Exception as e:
    print("❌ commands failed:", e)

try:
    setup_events(client)
    print("✅ events loaded")
except Exception as e:
    print("❌ events failed:", e)

# -------------------------
# READY EVENT
# -------------------------
@client.event
async def on_ready():
    try:
        await tree.sync()
        print(f"logged in as {client.user}")
        print("bot is online 🚀")
    except Exception as e:
        print("SYNC ERROR:", e)

# -------------------------
# RUN BOT
# -------------------------
if __name__ == "__main__":
    try:
        client.run(os.getenv("TOKEN"))
    except Exception as e:
        print("FATAL ERROR:", e)
