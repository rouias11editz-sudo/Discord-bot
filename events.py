import discord
import asyncio
import json
import random
import time

NAVY = 0x1B2B5B

daily_cooldown = {}
work_cooldown = {}

# -------------------------
# FILES
# -------------------------
def load_money():
    with open("money.json", "r") as f:
        return json.load(f)

def save_money(data):
    with open("money.json", "w") as f:
        json.dump(data, f, indent=4)


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
            levels[user_id] = {"messages": 0, "level": 0}

        levels[user_id]["messages"] += 1

        if levels[user_id]["messages"] >= 150:

            levels[user_id]["messages"] = 0
            levels[user_id]["level"] += 1

            lvl = levels[user_id]["level"]

            embed = discord.Embed(
                title="🎉 LEVEL UP",
                description=f"you are now level **{lvl}**",
                color=NAVY
            )

            await message.channel.send(embed=embed)

        save_levels(levels)

        # -------------------------
        # ⭐ SWANO LEVEL COMMAND (NEW)
        # -------------------------
        if msg == "swano level":

            lvl = levels[user_id]["level"]
            msgs = levels[user_id]["messages"]

            embed = discord.Embed(
                title="📊 YOUR LEVEL",
                description=(
                    f"level: **{lvl}**\n"
                    f"progress: **{msgs}/150 messages**"
                ),
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # AI TOGGLE
        # -------------------------
        if msg == "ai work":
            client.ai_enabled = True
            await message.channel.send("🤖 wsgg its me auote crewmate ai")
            return

        if msg == "ai stop":
            client.ai_enabled = False
            await message.channel.send("💤 ai is off i schelp")
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
                title="💰 SWUCKS",
                description=f"{money[user_id]} swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # DAILY
        # -------------------------
        if msg == "swano daily":

            now = time.time()

            if user_id in daily_cooldown:
                if now - daily_cooldown[user_id] < 86400:
                    await message.channel.send("⏳ come back later bro")
                    return

            daily_cooldown[user_id] = now

            money = load_money()

            if user_id not in money:
                money[user_id] = 0

            money[user_id] += 250

            save_money(money)

            await message.channel.send("🎁 +250 swucks")
            return

        # -------------------------
        # WORK
        # -------------------------
        if msg == "swano work":

            now = time.time()

            if user_id in work_cooldown:
                if now - work_cooldown[user_id] < 1800:
                    await message.channel.send("⏳ chill wait 30 min")
                    return

            work_cooldown[user_id] = now

            level = levels[user_id]["level"]

            jobs = [
                (30, "💼 CEO", 50, "you fired 37 employees"),
                (25, "🩺 Doctor", 40, "you diagnosed skill issue"),
                (20, "👨‍🍳 Chef", 30, "you burned food"),
                (15, "🔥 Firefighter", 25, "you saved a cat"),
                (10, "🚔 Police", 15, "you arrested raccoon"),
                (5, "☕ Barista", 8, "you spilled coffee"),
                (1, "🧹 Janitor", 3, "you cleaned toilet")
            ]

            job = None

            for req, name, pay, text in jobs:
                if level >= req:
                    job = (name, pay, text)
                    break

            if not job:
                await message.channel.send("❌ no job unlocked")
                return

            name, pay, text = job

            money = load_money()

            if user_id not in money:
                money[user_id] = 0

            money[user_id] += pay

            save_money(money)

            embed = discord.Embed(
                title=name,
                description=f"{text}\n+{pay} swucks",
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # SHOP
        # -------------------------
        if msg == "swano shop":

            embed = discord.Embed(
                title="🛒 SHOP",
                description=(
                    "#1 swano vm — 500\n"
                    "#2 custom role — 30\n"
                    "#3 dare swano — 1000"
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

            if item == "#1":

                if money[user_id] < 500:
                    await message.channel.send("fricking brokie go get rich")
                    return

                money[user_id] -= 500
                save_money(money)

                await message.channel.send(
                    "<@1434299997133865030> chop chop city boii"
                )

            elif item == "#2":

                if money[user_id] < 30:
                    await message.channel.send("fricking brokie go get rich")
                    return

                money[user_id] -= 30
                save_money(money)

                await message.channel.send(
                    "<@1434299997133865030> custom role purchased"
                )

            elif item == "#3":

                if money[user_id] < 1000:
                    await message.channel.send("fricking brokie go get rich")
                    return

                money[user_id] -= 1000
                save_money(money)

                await message.channel.send(
                    f"<@1434299997133865030> chop chop do the dare for {message.author.mention}"
                )

            return

        # -------------------------
        # ADMIN GRANT
        # -------------------------
        if msg.startswith("swano grant"):

            if not message.author.guild_permissions.administrator:
                await message.channel.send("admins only")
                return

            parts = message.content.split()

            if len(parts) < 4:
                return

            amount = int(parts[2].replace("sw", ""))

            if amount > 1000:
                await message.channel.send("max 1000 swucks")
                return

            if len(message.mentions) == 0:
                return

            target = message.mentions[0]

            money = load_money()

            tid = str(target.id)

            if tid not in money:
                money[tid] = 0

            money[tid] += amount

            save_money(money)

            await message.channel.send(
                f"gave {amount} swucks to {target.mention}"
            )

            return

        # -------------------------
        # SPAM
        # -------------------------
        if msg.startswith("swano spam"):

            text = message.content[11:]

            for i in range(5):
                await message.channel.send(text)
                await asyncio.sleep(0.5)

            return

        # -------------------------
        # AI CHAT
        # -------------------------
        if client.ai_enabled:
            reply = client.ask_ai(message.content)
            await message.channel.send(reply)
            return
