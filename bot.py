import discord
import os
import requests
import random
import asyncio
from discord import app_commands

ai_enabled = False

# -------------------------
# GAME DATA
# -------------------------
game_state = {}
member_game = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # IMPORTANT for member guessing

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
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    synced = await tree.sync()
    print(f"logged in as {client.user}")
    print(f"synced {len(synced)} commands")

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
            f"ouhh swanus mentioned?? {user1.mention} + {user2.mention} = 100% compatibility 👀"
        )
    else:
        await interaction.response.send_message(
            f"hmm… {user1.mention} + {user2.mention} = {random.randint(0,100)}%"
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
        "🎮 Guess the number (1-100)\n⏰ 1 minute + 10 attempts"
    )

    await asyncio.sleep(60)

    if interaction.channel.id in game_state:

        answer = game_state[interaction.channel.id]["answer"]

        embed = discord.Embed(
            title="⏰ Time's Up!",
            description=f"The number was **{answer}**",
            color=0x1B2B5B
        )

        await interaction.channel.send(embed=embed)

        del game_state[interaction.channel.id]

# -------------------------
# GUESS MEMBER COMMAND
# -------------------------
@tree.command(name="guess_member")
async def guess_member(interaction: discord.Interaction):

    members = [
        m for m in interaction.guild.members if not m.bot
    ]

    chosen = random.choice(members)
    member_game[interaction.channel.id] = chosen.id

    await interaction.response.send_message(
        "👤 Guess the member!\nType their name (no ping needed)\n⏰ 1 minute"
    )

    await asyncio.sleep(60)

    if interaction.channel.id in member_game:

        answer = interaction.guild.get_member(member_game[interaction.channel.id])

        embed = discord.Embed(
            title="⏰ Time's Up!",
            description=f"It was **{answer.display_name}**",
            color=0x1B2B5B
        )

        await interaction.channel.send(embed=embed)

        del member_game[interaction.channel.id]

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
    if message.channel.id in game_state:

        if message.content.isdigit():

            guess = int(message.content)
            game = game_state[message.channel.id]

            if guess > 100:

                await message.channel.send("🚨 only 1-100")
                return

            game["attempts"] -= 1
            answer = game["answer"]

            if guess == answer:

                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"{message.author.mention} got it right!",
                    color=0x1B2B5B
                )

                await message.channel.send(embed=embed)
                del game_state[message.channel.id]
                return

            if game["attempts"] <= 0:

                embed = discord.Embed(
                    title="💀 Out of attempts!",
                    description=f"The answer was **{answer}**",
                    color=0x1B2B5B
                )

                await message.channel.send(embed=embed)
                del game_state[message.channel.id]
                return

            if guess < answer:
                await message.channel.send(f"⬆️ higher ({game['attempts']} left)")
            else:
                await message.channel.send(f"⬇️ lower ({game['attempts']} left)")

            return

    # -------------------------
    # GUESS MEMBER GAME
    # -------------------------
    if message.channel.id in member_game:

        guess = message.content.lower()

        answer_id = member_game[message.channel.id]
        member = message.guild.get_member(answer_id)

        if member:

            if guess in member.display_name.lower() or guess in member.name.lower():

                embed = discord.Embed(
                    title="🎉 Correct Guess!",
                    description=f"{message.author.mention} got it!\nIt was **{member.display_name}**",
                    color=0x1B2B5B
                )

                await message.channel.send(embed=embed)
                del member_game[message.channel.id]

            else:

                embed = discord.Embed(
                    title="❌ Wrong",
                    description="not that one 😭",
                    color=0x1B2B5B
                )

                await message.channel.send(embed=embed)

        return

    # -------------------------
    # GREETING
    # -------------------------
    is_owner = message.guild and message.author.id == message.guild.owner_id
    is_admin = message.author.guild_permissions.administrator

    if (is_owner or is_admin) and msg in ["hi", "hello", "hey", "yo"]:

        embed = discord.Embed(
            description="👋 hi",
            color=0x1B2B5B
        )

        embed.set_image(url="https://media.tenor.com/crtsfiles-juhoon-cortis-hi-waving/0.gif")

        await message.channel.send(embed=embed)
        return

    # -------------------------
    # AI TOGGLE
    # -------------------------
    if msg == "ai work":
        ai_enabled = True
        await message.channel.send("ai on")
        return

    if msg == "ai stop":
        ai_enabled = False
        await message.channel.send("ai off")
        return

    # -------------------------
    # SPAM
    # -------------------------
    allowed_spammers = {
        1208382519611760670,
        1434299997133865030,
        652988923672395779,
        1148948508481699850
    }

    if message.author.id in allowed_spammers and msg.startswith("spam "):

        text = message.content[5:]

        for _ in range(5):
            await message.channel.send(text)
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

            embed = discord.Embed(
                description=reply,
                color=0x1B2B5B
            )

            await message.channel.send(embed=embed)
            return

    # -------------------------
    # AI CHAT
    # -------------------------
    if ai_enabled:
        reply = ask_ai(message.content)
        await message.channel.send(reply)

client.run(os.getenv("TOKEN"))
