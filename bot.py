import discord
import os
import requests
import random
import asyncio
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
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "you are a chaotic gen z discord bot. "
                    "you speak lowercase, slang, short replies, funny tone. "
                    "never sound formal or robotic."
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
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")

# -------------------------
# SLASH COMMANDS
# -------------------------
@tree.command(name="gay")
async def gay(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(
        f"{user.mention} is {random.randint(0,100)}% gay 🌈"
    )

@tree.command(name="autism")
async def autism(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(
        f"{user.mention} is {random.randint(0,100)}% autistic 🧩"
    )

@tree.command(name="ship")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):

    if (
        (user1.id == 1434299997133865030 and user2.id == 652988923672395779)
        or
        (user1.id == 652988923672395779 and user2.id == 1434299997133865030)
    ):
        await interaction.response.send_message(
            f"ouhh swanus mentioned?? {user1.mention} + {user2.mention} = 100% compatibility 👀👀👀"
        )
    else:
        await interaction.response.send_message(
            f"hmm… {user1.mention} + {user2.mention} = {random.randint(0,100)}% compatibility ahaha ig…."
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
    # AI TOGGLE
    # -------------------------
    if msg == "ai work":
        ai_enabled = True
        await message.channel.send("yoo its me crewmate ai wsg!! send a message to speak")
        return

    if msg == "ai stop":
        ai_enabled = False
        await message.channel.send("baaalright, im gone now bai")
        return

    # -------------------------
    # SPAM COMMAND
    # -------------------------
    allowed_spammers = {
        1208382519611760670,
        1434299997133865030,
        652988923672395779,
        1148948508481699850
    }

    if message.author.id in allowed_spammers and msg.startswith("spam "):
        spam_text = message.content[5:]

        for i in range(5):
            await message.channel.send(spam_text)
            await asyncio.sleep(0.6)

        return

    # -------------------------
    # GLAZE COMMAND (EMBEDS)
    # -------------------------
    if msg.startswith("glaze ") and message.mentions:
        user = message.mentions[0]

        glaze_lines = [
            f"{user.display_name} boiii u soo tuff u my little comet!",
            f"if i catch someone talking bad bout {user.display_name} im boutta give em a knuckle sandwhich!",
            f"ur coding IS for the welcome!",
            f"everyone bow down to {user.display_name} 🙏",
            f"{user.display_name} = main character energy 💯"
        ]

        for line in glaze_lines:
            embed = discord.Embed(
                description=line,
                color=0xFF4DFF
            )
            embed.set_author(
                name=f"GLAZING {user.display_name}",
                icon_url=user.display_avatar.url
            )

            await message.channel.send(embed=embed)
            await asyncio.sleep(0.6)

        return

    # -------------------------
    # AUTO RESPONSES
    # -------------------------
    responses = {
        "help": "help is on it’s way",
        "swano": "swano is the goat! leave mah goat alone",
        "venus": "venus is swano’s mommy, swano needs mama mwilkies",
        "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)",
        "jju": "if u're talking bout juhoon then ouhh shiii👀👀 twinkie jju? Ok, dttm, LEAVE.",
        "sean": "ouhh my eom freakk 😋😋😝😝 give me one chance seannnn",
        "keonho": "did you just talk about the cutest and gayest member of the group? Thats tuff dayummm",
        "juhoon": "OH MY FRICKING GOSH JUHHOON HISKAJSJS JUHOON JUHOON, SJAIOAKXXK THAT’S SWANO’s HUBBY JUHOON",
        "martin": "Those holy predatory eyes 👀 👀",
        "james": "WANNA SEE MY HELICOPTER??? 🚁",
        "gojo": "are you 19+??? gojo is mah goat",
        "hori": "Isn't that james's #1 feet licker??? she's so horny for jems 🥹👀"
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
