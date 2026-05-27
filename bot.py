import discord
import os
import requests
import random
import asyncio
from discord import app_commands

# -------------------------
# AI STATE
# -------------------------
ai_enabled = False

# -------------------------
# INTENTS
# -------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# ECONOMY + GAME DATA
# -------------------------
user_currency = {}
game_state = {}
round_winner = {}

ROLE_ID = 1509137943174840392


# -------------------------
# AI FUNCTION
# -------------------------
def ask_ai(prompt):
    try:
        headers = {
            "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
            "Content-Type": "application/json",
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "you are a chaotic gen z discord bot. "
                        "you speak lowercase, slang, short replies."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )

        if r.status_code != 200:
            return "ai broke 💀"

        return r.json()["choices"][0]["message"]["content"]

    except:
        return "ai error 💀"


# -------------------------
# ECONOMY HELPERS
# -------------------------
def get_balance(user_id):
    return user_currency.get(user_id, 0)


def add_currency(user_id, amount):
    user_currency[user_id] = get_balance(user_id) + amount


async def check_role(member):
    if get_balance(member.id) >= 500:
        role = member.guild.get_role(ROLE_ID)
        if role and role not in member.roles:
            await member.add_roles(role)


# -------------------------
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")


# -------------------------
# SLASH COMMANDS (YOUR ORIGINAL)
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
# NEW GAME COMMANDS
# -------------------------
@tree.command(name="guess_number")
async def guess_number(interaction: discord.Interaction):

    game_state[interaction.channel.id] = {
        "type": "number",
        "answer": random.randint(1, 100)
    }

    round_winner[interaction.channel.id] = None

    await interaction.response.send_message(
        "🎮 Guess the number (1–100)! Type in chat."
    )


@tree.command(name="guess_member")
async def guess_member(interaction: discord.Interaction):

    members = [m for m in interaction.guild.members if not m.bot]

    game_state[interaction.channel.id] = {
        "type": "member",
        "answer": random.choice(members).id
    }

    await interaction.response.send_message(
        "👥 Guess the member! Ping them in chat."
    )


@tree.command(name="balance")
async def balance(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"💰 {get_balance(interaction.user.id)} currency"
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
    channel_id = message.channel.id

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
    # AI CHAT
    # -------------------------
    if ai_enabled:
        if msg.startswith("ai "):
            reply = ask_ai(message.content[3:])
            await message.channel.send(reply)
            return

    # -------------------------
    # ADMIN GREETING GIF
    # -------------------------
    is_owner = message.guild and message.author.id == message.guild.owner_id
    is_admin = message.author.guild_permissions.administrator

    if (is_owner or is_admin) and msg in ["hi", "hello", "hey", "yo"]:

        embed = discord.Embed(
            description="👋 admin greeted the server!",
            color=0x4DA6FF
        )

        embed.set_image(
            url="https://media.tenor.com/MY_ULOc6jpcAAAPo/crtsfiles-juhoon.mp4"
        )

        await message.channel.send(embed=embed)
        return

    # -------------------------
    # SPAM SYSTEM
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
        "venus": "venus is swano’s mommy, swano needs mwommy mwilkies",
        "archa": "i love archa (platonic intention, no sexual intention feet prevention quote motivation,sending love from cosmic comet planet)'",
        "jju": "if u're talking bout juhoon then ouhh shiii👀👀",
        "sean": "ouhh my eom freakk 😋😋",
        "keonho": "you mean the gayest and cutest member? thats tuff dayummm",
        "juhoon": "OH MY FRICKING GOSH JUHOON AHAHAHAH, THATS SWANO'S HUBBYYY",
        "martin": "Those holy predator smexy eyes 👀",
        "james": "WANNA SEE MY HELICOPTER??? 🚁",
        "gojo": "are you 19+??? gojo is mah goat",
        "hori": "Likeee the only who likes james feet? she's so horny for jems🥹👀"
    }

    for key, reply in responses.items():
        if key in msg:

            embed = discord.Embed(
                description=reply,
                color=0x4DA6FF
            )

            await message.channel.send(embed=embed)
            return

    # -------------------------
    # GAME SYSTEM
    # -------------------------
    if channel_id in game_state:

        game = game_state[channel_id]

        # -------------------------
        # NUMBER GAME
        # -------------------------
        if game["type"] == "number":

            if message.content.isdigit():

                guess = int(message.content)
                answer = game["answer"]

                if guess == answer:

                    if round_winner[channel_id] is None:
                        round_winner[channel_id] = message.author.id
                        add_currency(message.author.id, 20)
                        await message.channel.send("⚡die ihy. +20")
                    else:
                        add_currency(message.author.id, 10)
                        await message.channel.send("🎉 i guess?" +10")

                    await check_role(message.author)

                    del game_state[channel_id]
                    del round_winner[channel_id]
                    return

                await message.channel.send("⬆️ higher" if guess < answer else "⬇️ lower")
                return

        # -------------------------
        # MEMBER GAME
        # -------------------------
        if game["type"] == "member":

            if message.mentions:

                if message.mentions[0].id == game["answer"]:

                    add_currency(message.author.id, 10)
                    await message.channel.send("🎉 ok???? +10")

                    await check_role(message.author)

                    del game_state[channel_id]
                    return


client.run(os.getenv("TOKEN"))
