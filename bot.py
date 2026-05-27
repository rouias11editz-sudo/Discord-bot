import discord
import os
import requests
import random
from discord import app_commands

ai_enabled = False

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# AI FUNCTION
# -------------------------
def ask_ai(prompt):
    headers = {
        "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
        "Content-Type": "application/json",
        "HTTP-Referer": "https://discordbot.local",
        "X-Title": "Discord Bot"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a friendly Discord chatbot."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return f"AI Error {response.status_code}"

    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# BOT READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

# -------------------------
# SLASH COMMANDS
# -------------------------
@tree.command(name="gay", description="Check how gay someone is")
async def gay(interaction: discord.Interaction, user: discord.Member):
    percent = random.randint(0, 100)

    await interaction.response.send_message(
        f"{user.mention} is {percent}% gay 🌈"
    )

@tree.command(name="autism", description="Check autism percentage")
async def autism(interaction: discord.Interaction, user: discord.Member):
    percent = random.randint(0, 100)

    await interaction.response.send_message(
        f"{user.mention} is {percent}% autistic 🧩"
    )

@tree.command(name="ship", description="Ship two users together")
async def ship(
    interaction: discord.Interaction,
    user1: discord.Member,
    user2: discord.Member
):
    # SPECIAL PAIR = ALWAYS 100%
    special_ids = {
        1434299997133865030,
        652988923672395779
    }

    if {user1.id, user2.id} == special_ids:
        percent = 100
    else:
        percent = random.randint(0, 100)

    await interaction.response.send_message(
        f"ouhh swanus mentioned?? {user1.mention} + {user2.mention} = {percent}% compatibility 👀👀👀"
    )

# -------------------------
# MESSAGE EVENTS
# -------------------------
@client.event
async def on_message(message):
    global ai_enabled

    if message.author.bot:
        return

    msg = message.content.lower()

    # -------------------------
    # SPECIFIC GIF RESPONSE
    # -------------------------
    if "1508831915568926880/caption.gif" in msg:
        await message.channel.send(
            "pls stop chumeul chwo, sindeullin maxxing"
        )
        return

    # -------------------------
    # AI TOGGLE
    # -------------------------
    if msg == "ai work":
        ai_enabled = True
        await message.channel.send("hello this me crewmate ai trustt🤖")
    
        return

    if msg == "ai stop":
        ai_enabled = False
        await message.channel.send("stop using me now im tired📴")
        return

    # -------------------------
    # AUTO RESPONSES
    # -------------------------
    responses = {
        "help": "help is on it’s way",
        "swano": "swano is the goat! leave mah goat alone",
        "venus": "venus is swano’s mommy, swano needs mama mwilkies",
        "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)"
    }

    for key, reply in responses.items():
        if key in msg:
            await message.channel.send(reply)
            return

    # -------------------------
    # AI CHAT
    # -------------------------
    if ai_enabled:
        reply = ask_ai(message.content)
        await message.channel.send(reply)
        return

client.run(os.getenv("TOKEN"))
