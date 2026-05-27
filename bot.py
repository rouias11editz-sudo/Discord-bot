import discord
import os
import requests
import random
import asyncio
from discord import app_commands

ai_enabled = False

# -------------------------
# GUESS NUMBER GAME DATA
# -------------------------
game_state = {}

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
                    "never be formal or robotic."
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
# GUESS NUMBER COMMAND
# -------------------------
@tree.command(name="guess_number")
async def guess_number(interaction: discord.Interaction):

    game_state[interaction.channel.id] = {
        "answer": random.randint(1, 100),
        "attempts": 10
    }

    await interaction.response.send_message(
        "🎮 Guess the number (1-100)!\n⏰ You have 1 minute and 10 attempts."
    )

    await asyncio.sleep(60)

    if interaction.channel.id in game_state:

        answer = game_state[interaction.channel.id]["answer"]

        await interaction.channel.send(
            f"⏰ time's up!! the number was **{answer}**"
        )

        del game_state[interaction.channel.id]

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
    # GUESS NUMBER GAME
    # -------------------------
    channel_id = message.channel.id

    if channel_id in game_state:

        if message.content.isdigit():

            guess = int(message.content)

            # WARNING IF ABOVE 100
            if guess > 100:

                await message.channel.send(
                    "🚨 bro the number is ONLY between 1-100"
                )

                return

            game = game_state[channel_id]

            answer = game["answer"]

            game["attempts"] -= 1

            # CORRECT
            if guess == answer:

                await message.channel.send(
                    f"🎉 {message.author.mention} guessed the number!"
                )

                del game_state[channel_id]

                return

            # NO ATTEMPTS LEFT
            if game["attempts"] <= 0:

                await message.channel.send(
                    f"💀 no attempts left! the number was **{answer}**"
                )

                del game_state[channel_id]

                return

            # HIGHER / LOWER
            elif guess < answer:

                await message.channel.send(
                    f"⬆️ higher ({game['attempts']} attempts left)"
                )

            else:

                await message.channel.send(
                    f"⬇️ lower ({game['attempts']} attempts left)"
                )

            return

    # -------------------------
    # OWNER / ADMIN GREETING GIF
    # -------------------------
    is_owner = message.guild and message.author.id == message.guild.owner_id
    is_admin = message.author.guild_permissions.administrator

    greetings = ["hi", "hello", "hey", "yo"]

    if (is_owner or is_admin) and msg in greetings:

        embed = discord.Embed(
            description="👋",
            color=0x4DA6FF
        )

        embed.set_image(
            url="https://media.tenor.com/crtsfiles-juhoon-cortis-hi-waving/0.gif"
        )

        embed.set_author(
            name=f"Greetings from {message.author.display_name}",
            icon_url=message.author.display_avatar.url
        )

        await message.channel.send(embed=embed)
        return

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
    # AUTO RESPONSES (EMBEDS)
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

            embed = discord.Embed(
                description=reply,
                color=0x4DA6FF
            )

            embed.set_author(
                name="AUTO RESPONSE",
                icon_url=message.author.display_avatar.url
            )

            await message.channel.send(embed=embed)

            return

    # -------------------------
    # AI CHAT
    # -------------------------
    if ai_enabled:

        reply = ask_ai(message.content)

        await message.channel.send(reply)

        return

client.run(os.getenv("TOKEN"))
