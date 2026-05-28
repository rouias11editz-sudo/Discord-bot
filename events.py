import discord
import asyncio
import json
import random
import time

NAVY = 0x1B2B5B

# -------------------------
# COOLDOWNS
# -------------------------
daily_cooldown = {}
work_cooldown = {}

# -------------------------
# MONEY FUNCTIONS
# -------------------------
def load_money():

    with open("money.json", "r") as f:
        return json.load(f)

def save_money(data):

    with open("money.json", "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# LEVEL FUNCTIONS
# -------------------------
def load_levels():

    with open("levels.json", "r") as f:
        return json.load(f)

def save_levels(data):

    with open("levels.json", "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# EVENTS
# -------------------------
def setup_events(client):

    @client.event
    async def on_message(message):

        if message.author.bot:
            return

        msg = message.content.lower()

        user_id = str(message.author.id)

        # -------------------------
        # LEVEL SYSTEM
        # -------------------------
        levels = load_levels()

        if user_id not in levels:

            levels[user_id] = {
                "messages": 0,
                "level": 0
            }

        levels[user_id]["messages"] += 1

        if levels[user_id]["messages"] >= 150:

            levels[user_id]["messages"] = 0
            levels[user_id]["level"] += 1

            level = levels[user_id]["level"]

            unlocks = {
                1: "🧹 Janitor",
                5: "☕ Barista",
                10: "🚔 Police Officer",
                15: "🔥 Firefighter",
                20: "👨‍🍳 Chef",
                25: "🩺 Doctor",
                30: "💼 CEO"
            }

            embed = discord.Embed(
                title="🎉 LEVEL UP",
                description=f"you reached level **{level}**",
                color=NAVY
            )

            if level in unlocks:

                embed.add_field(
                    name="NEW JOB UNLOCKED",
                    value=unlocks[level],
                    inline=False
                )

            await message.channel.send(embed=embed)

        save_levels(levels)

        # -------------------------
        # AI TOGGLE
        # -------------------------
        if msg == "ai work":

            client.ai_enabled = True

            embed = discord.Embed(
                title="🤖 AI ENABLED",
                description="yoo its me crewmate ai wsg",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        if msg == "ai stop":

            client.ai_enabled = False

            embed = discord.Embed(
                title="💤 AI DISABLED",
                description="baaalright im gone now bai",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
        # BALANCE
        # -------------------------
        if msg == "swano balance":

            money = load_money()

            if user_id not in money:
                money[user_id] = 0
                save_money(money)

            embed = discord.Embed(
                title="💰 SWUCKS BALANCE",
                description=f"you have **{money[user_id]} swucks**",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
        # DAILY
        # -------------------------
        if msg == "swano daily":

            current_time = time.time()

            if user_id in daily_cooldown:

                if current_time - daily_cooldown[user_id] < 86400:

                    embed = discord.Embed(
                        title="⏳ DAILY COOLDOWN",
                        description="come back tomorrow",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    return

            daily_cooldown[user_id] = current_time

            money = load_money()

            if user_id not in money:
                money[user_id] = 0

            money[user_id] += 250

            save_money(money)

            embed = discord.Embed(
                title="🎁 DAILY REWARD",
                description="+250 swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
        # WORK
        # -------------------------
        if msg == "swano work":

            current_time = time.time()

            if user_id in work_cooldown:

                if current_time - work_cooldown[user_id] < 1800:

                    embed = discord.Embed(
                        title="⏳ WORK COOLDOWN",
                        description="wait 30 minutes",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    return

            work_cooldown[user_id] = current_time

            level = levels[user_id]["level"]

            jobs = [
                (30, "💼 CEO", 50, "you fired 37 employees today"),
                (25, "🩺 Doctor", 40, "you diagnosed someone with skill issue"),
                (20, "👨‍🍳 Chef", 30, "you burned 4 steaks"),
                (15, "🔥 Firefighter", 25, "you saved a cat from a microwave"),
                (10, "🚔 Police Officer", 15, "you arrested a raccoon"),
                (5, "☕ Barista", 8, "you misspelled 14 starbucks names"),
                (1, "🧹 Janitor", 3, "you unclogged the school toilet")
            ]

            chosen_job = None

            for req, name, pay, text in jobs:

                if level >= req:
                    chosen_job = (name, pay, text)
                    break

            if not chosen_job:

                embed = discord.Embed(
                    title="❌ NO JOB UNLOCKED",
                    description="reach level 1 first",
                    color=NAVY
                )

                await message.channel.send(embed=embed)

                return

            name, pay, text = chosen_job

            money = load_money()

            if user_id not in money:
                money[user_id] = 0

            money[user_id] += pay

            save_money(money)

            embed = discord.Embed(
                title=name,
                description=f"{text}\n\n💰 +{pay} swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
        # SHOP
        # -------------------------
        if msg == "swano shop":

            embed = discord.Embed(
                title="🛒 SWUCKS SHOP",
                description=(
                    "#1 🐱 Swano Meowing VM — 500 swucks\n\n"
                    "#2 🎨 Custom Role — 30 swucks\n\n"
                    "#3 😈 Dare Swano To Do Anything — 1000 swucks"
                ),
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
# BUY
# -------------------------
if msg.startswith("swano buy"):

    split = msg.split()

    if len(split) < 3:
        return

    item = split[2]

    money = load_money()

    if user_id not in money:
        money[user_id] = 0

    # ITEM #1
    if item == "#1":

        cost = 500

        if money[user_id] < cost:

            embed = discord.Embed(
                title="💀 BROKE",
                description="you dont have enough swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        money[user_id] -= cost

        save_money(money)

        await message.channel.send(
            "<@1434299997133865030> chop chop city boii"
        )

    # ITEM #2
    elif item == "#2":

        cost = 30

        if money[user_id] < cost:

            embed = discord.Embed(
                title="💀 LMFAO broke mf",
                description="you dont have enough swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        money[user_id] -= cost

        save_money(money)

        await message.channel.send(
            "<@1434299997133865030> custom role purchased chop chop"
        )

    # ITEM #3
    elif item == "#3":

        cost = 1000

        if money[user_id] < cost:

            embed = discord.Embed(
                title="💀 fucking brokie",
                description="you dont have enough swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        money[user_id] -= cost

        save_money(money)

        await message.channel.send(
            "<@1434299997133865030> chop chop do the dare"
        )

    return

        # -------------------------
        # ADMIN GRANT
        # -------------------------
        if msg.startswith("swano grant"):

            if not message.author.guild_permissions.administrator:

                embed = discord.Embed(
                    title="❌ ADMINS ONLY",
                    color=NAVY
                )

                await message.channel.send(embed=embed)

                return

            split = message.content.split()

            if len(split) < 4:
                return

            amount_text = split[2].lower()

            if not amount_text.endswith("sw"):
                return

            try:
                amount = int(amount_text.replace("sw", ""))

            except:
                return

            if amount > 1000:

                embed = discord.Embed(
                    title="❌ woah calm the max is 1000",
                    description="max grant is 1000 swucks",
                    color=NAVY
                )

                await message.channel.send(embed=embed)

                return

            if len(message.mentions) == 0:
                return

            target = message.mentions[0]

            money = load_money()

            target_id = str(target.id)

            if target_id not in money:
                money[target_id] = 0

            money[target_id] += amount

            save_money(money)

            embed = discord.Embed(
                title="💸 ok its given leave me alone",
                description=(
                    f"gave **{amount} swucks** "
                    f"to {target.mention}"
                ),
                color=NAVY
            )

            await message.channel.send(embed=embed)

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

        if (
            message.author.id in allowed_spammers
            and msg.startswith("swano spam ")
        ):

            spam_text = message.content[12:]

            for i in range(5):

                await message.channel.send(spam_text)

                await asyncio.sleep(0.6)

            return

        # -------------------------
        # OWNER / ADMIN GREETING
        # -------------------------
        is_owner = (
            message.guild and
            message.author.id == message.guild.owner_id
        )

        is_admin = message.author.guild_permissions.administrator

        greetings = ["hi", "hello", "hey", "yo"]

        if (is_owner or is_admin) and msg in greetings:

            embed = discord.Embed(
                description="👋",
                color=NAVY
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
            "juhoon": "OH MY FRICKING GOSH JUHHOON HISKAJSJS JUHOON SWANO'S BABYYY JUHOON",
            "martin": "Those holy predatory eyes 👀 👀",
            "james": "WANNA SEE MY HELICOPTER??? 🚁",
            "gojo": "are you 19+??? gojo is mah goat",
            "hori": "Isn't that james's #1 feet licker??? she's so horny for jems 🥹👀"
        }

        for key, reply in responses.items():

            if key in msg:

                embed = discord.Embed(
                    description=reply,
                    color=NAVY
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
        if client.ai_enabled:

            reply = client.ask_ai(message.content)

            await message.channel.send(reply)

            return
