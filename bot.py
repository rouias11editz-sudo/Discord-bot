import discord
import os
import requests
import random
import asyncio
from discord import app_commands

# -------------------------
# INTENTS
# -------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------
# DATA
# -------------------------
user_currency = {}
game_state = {}
round_winner = {}

ROLE_ID = 1509137943174840392


# -------------------------
# ECONOMY HELPERS
# -------------------------
def get_balance(user_id):
    return user_currency.get(user_id, 0)


async def add_currency(user_id, amount):
    user_currency[user_id] = get_balance(user_id) + amount


async def check_role(member):
    if get_balance(member.id) >= 500:
        role = member.guild.get_role(ROLE_ID)
        if role and role not in member.roles:
            await member.add_roles(role)


# -------------------------
# SAFE GAME CLEANUP (NO CRASH TIMER)
# -------------------------
async def end_game_later(channel_id, delay=180):
    await asyncio.sleep(delay)

    if channel_id not in game_state:
        return

    game = game_state[channel_id]

    channel = client.get_channel(channel_id)
    if not channel:
        return

    if game["type"] == "number":
        await channel.send(f"⏱ time’s up! the number was **{game['answer']}** 💀")

    elif game["type"] == "member":
        await channel.send("⏱ time’s up! nobody guessed it 💀")

    game_state.pop(channel_id, None)
    round_winner.pop(channel_id, None)


# -------------------------
# AI (OPTIONAL)
# -------------------------
def ask_ai(prompt):
    headers = {
        "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "you are a chaotic gen z discord bot. short funny replies."
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
        return "AI error 💀"

    return r.json()["choices"][0]["message"]["content"]


# -------------------------
# READY
# -------------------------
@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")


# -------------------------
# GUESS NUMBER GAME
# -------------------------
@tree.command(name="guess_number")
async def guess_number(interaction: discord.Interaction):

    number = random.randint(1, 100)

    game_state[interaction.channel.id] = {
        "type": "number",
        "answer": number
    }

    round_winner[interaction.channel.id] = None

    await interaction.response.send_message(
        "🎮 GUESS THE NUMBER (1–100)\n"
        "Type your guesses in chat for 3 minutes!"
    )

    asyncio.create_task(end_game_later(interaction.channel.id))


# -------------------------
# GUESS MEMBER GAME
# -------------------------
@tree.command(name="guess_member")
async def guess_member(interaction: discord.Interaction):

    members = [m for m in interaction.guild.members if not m.bot]
    target = random.choice(members)

    game_state[interaction.channel.id] = {
        "type": "member",
        "answer": target.id
    }

    await interaction.response.send_message(
        "👥 GUESS THE MEMBER!\n"
        "Ping the user in chat!"
    )

    asyncio.create_task(end_game_later(interaction.channel.id))


# -------------------------
# LEADERBOARD (SAFE)
# -------------------------
@tree.command(name="leaderboard")
async def leaderboard(interaction: discord.Interaction):

    if not user_currency:
        await interaction.response.send_message("no data 💀")
        return

    sorted_users = sorted(user_currency.items(), key=lambda x: x[1], reverse=True)[:10]

    desc = ""

    for i, (uid, bal) in enumerate(sorted_users, start=1):

        try:
            user = await client.fetch_user(uid)
            desc += f"**{i}. {user.name}** — {bal} 💰\n"
        except:
            desc += f"**{i}. Unknown** — {bal} 💰\n"

    embed = discord.Embed(
        title="🏆 SWANO LEADERBOARD",
        description=desc,
        color=0x4DA6FF
    )

    await interaction.response.send_message(embed=embed)


# -------------------------
# BALANCE
# -------------------------
@tree.command(name="balance")
async def balance(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"💰 {get_balance(interaction.user.id)} swano currency"
    )


# -------------------------
# MESSAGE GAME LOGIC
# -------------------------
@client.event
async def on_message(message):

    if message.author.bot:
        return

    channel_id = message.channel.id
    msg = message.content.lower()

    # -------------------------
    # AI CHAT
    # -------------------------
    if msg.startswith("ai "):
        reply = ask_ai(message.content[3:])
        await message.channel.send(reply)
        return

    # -------------------------
    # GAME LOGIC
    # -------------------------
    if channel_id not in game_state:
        return

    game = game_state[channel_id]

    # -------------------------
    # NUMBER GAME
    # -------------------------
    if game["type"] == "number" and message.content.isdigit():

        guess = int(message.content)
        answer = game["answer"]

        if guess == answer:

            if round_winner[channel_id] is None:
                round_winner[channel_id] = message.author.id
                await message.channel.send("⚡ DAYUM u fast asf homie!! +20 currency")
                await add_currency(message.author.id, 20)
            else:
                await message.channel.send("🎉 ouhh shiii!! +10 currency")
                await add_currency(message.author.id, 10)

            await check_role(message.author)

            game_state.pop(channel_id, None)
            round_winner.pop(channel_id, None)
            return

        diff = abs(guess - answer)

        if diff <= 5:
            hint = "🔥 very close u idiot"
        elif diff <= 15:
            hint = "📉 close ok ure almost far"
        else:
            hint = "❄️ far how do u suck that much"

        direction = "⬆️ higher" if guess < answer else "⬇️ lower"

        await message.channel.send(f"{direction} — {hint}")
        return

    # -------------------------
    # MEMBER GAME
    # -------------------------
    if game["type"] == "member":

        if message.mentions:

            if message.mentions[0].id == game["answer"]:

                await message.channel.send("🎉 wow u got it correct somehoe?!! +10 currency")
                await add_currency(message.author.id, 10)
                await check_role(message.author)

                game_state.pop(channel_id, None)
                return


# -------------------------
# RUN
# -------------------------
client.run(os.getenv("TOKEN"))
