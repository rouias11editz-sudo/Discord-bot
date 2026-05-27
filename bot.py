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
        "X-Title": "Crewmate AI"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "you are crewmate ai, a chaotic gen z discord bot. "
                    "you ONLY speak in lowercase. "
                    "you talk like a real discord user and use modern slang naturally. "
                    "you say things like bro, ngl, fr, cooked, insane, wild, goofy, nahhh, HELP, crying, etc. "
                    "you are funny, unserious, chaotic, and expressive. "
                    "keep responses short and casual. "
                    "never sound formal, robotic, corporate, or like customer support. "
                    "avoid long explanations. "
                    "use emojis sometimes like 😭💀🙏🔥"
                )
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
        return f"ai error {response.status_code}"

    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# BOT READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")

# -------------------------
# SLASH COMMANDS
# -------------------------
@tree.command(name="gay", description="check how gay someone is")
async def gay(interaction: discord.Interaction, user: discord.Member):
    percent = random.randint(0, 100)

    await interaction.response.send_message(
        f"{user.mention} is {percent}% gay 🌈"
    )

@tree.command(name="autism", description="check autism percentage")
async def autism(interaction: discord.Interaction, user: discord.Member):
    percent = random.randint(0, 100)

    await interaction.response.send_message(
        f"{user.mention} is {percent}% autistic 🧩"
    )

@tree.command(name="ship", description="ship two users together")
async def ship(
    interaction: discord.Interaction,
    user1: discord.Member,
    user2: discord.Member
):

    # SPECIAL USERS
    if (
        (user1.id == 1434299997133865030 and user2.id == 652988923672395779)
        or
        (user1.id == 652988923672395779 and user2.id == 1434299997133865030)
    ):
        percent = 100

        await interaction.response.send_message(
            f"ouhh swanus mentioned?? {user1.mention} + {user2.mention} = {percent}% compatibility 👀👀👀"
        )

    else:
        percent = random.randint(0, 100)

        await interaction.response.send_message(
            f"hmm… {user1.mention} + {user2.mention} = {percent}% compatibility ahaha ig…."
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
    # GIF RESPONSE
    # -------------------------
    if "1508831915568926880/caption.gif" in msg:
        await message.channel.send(
            "pls stop chumeul chwo, sindeullin maxxing"
        )
        return

    # -------------------------
    # AI ON
    # -------------------------
    if msg == "ai work":
        ai_enabled = True

        await message.channel.send(
            "yoo its me crewmate ai wsg!! send a message to speak"
        )
        return

    # -------------------------
    # AI OFF
    # -------------------------
    if msg == "ai stop":
        ai_enabled = False

        await message.channel.send(
            "baaalright, im gone now bai"
        )
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
