import discord
import asyncio
import json
import random
import time

NAVY = 0x1B2B5B

daily_cooldown = {}
work_cooldown = {}

# -------------------------
# FILE HELPERS
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
# SETUP
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

            embed = discord.Embed(
                title="🎉 LEVEL UP",
                description=f"you are now level **{levels[user_id]['level']}**",
                color=NAVY
            )

            await message.channel.send(embed=embed)

        save_levels(levels)

        # -------------------------
        # SWANO LEVEL
        # -------------------------
        if msg == "swano level":

            embed = discord.Embed(
                title="📊 YOUR LEVEL",
                description=(
                    f"level: **{levels[user_id]['level']}**\n"
                    f"progress: **{levels[user_id]['messages']}/150 messages**"
                ),
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # 8BALL
        # -------------------------
        if msg.startswith("swano 8ball"):

            answers = [
                "🎱 probably",
                "🎱 maybe",
                "🎱 yes",
                "🎱 no",
                "🎱 100% yes",
                "🎱 not happening",
                "🎱 never",
                "🎱 ask again later"
            ]

            question = message.content[12:].strip()

            embed = discord.Embed(
                title="🎱 8BALL",
                description=f"**Q:** {question}\n\n**A:** {random.choice(answers)}",
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # LEADERBOARD
        # -------------------------
        if msg == "swano leaderboard":

            sorted_users = sorted(
                levels.items(),
                key=lambda x: x[1]["level"],
                reverse=True
            )[:10]

            desc = ""

            for i, (uid, data) in enumerate(sorted_users, start=1):
                desc += f"**{i}.** <@{uid}> — level {data['level']}\n"

            embed = discord.Embed(
                title="🏆 LEADERBOARD",
                description=desc if desc else "no data yet",
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # AI TOGGLE
        # -------------------------
        if msg == "ai work":
            client.ai_enabled = True
            await message.channel.send("🤖 ai on")
            return

        if msg == "ai stop":
            client.ai_enabled = False
            await message.channel.send("💤 ai off")
            return

        # -------------------------
        # BALANCE
        # -------------------------
        if msg == "swano balance":

            money = load_money()

            if user_id not in money:
                money[user_id] = 0

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
                    await message.channel.send("⏳ come back later")
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
                    await message.channel.send("⏳ 30 min cooldown")
                    return

            work_cooldown[user_id] = now

            level = levels[user_id]["level"]

            jobs = [
                (30, "💼 CEO", 50, "you fired employees, congrats ure corrupt!"),
                (25, "🩺 Doctor", 40, "you healed people from mental ilnesses! swano thanks u for making her healthy"),
                (20, "👨‍🍳 Chef", 30, "you burned water?????"),
                (15, "🔥 Firefighter", 25, "you saved cats woww such a hero"),
                (10, "🚔 Police", 15, "you arrested an inflatable boat??} Ok..."),
                (5, "☕ Barista", 8, "you made coffee w a messed up  name ok!!"),
                (1, "🧹 Janitor", 3, "you cleaned toilet and got stains on ur hand, wow.")
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
                    "#1 Swano meowing VM - 500\n"
                    "#2 Custom role - 30\n"
                    "#3 Dare swano to do anything - 1000"
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

            def not_enough():
                return discord.Embed(
                    title="💀 BROKIE",
                    description="fricking brokie go get rich",
                    color=NAVY
                )

            if item == "#1":

                if money[user_id] < 500:
                    await message.channel.send(embed=not_enough())
                    return

                money[user_id] -= 500
                save_money(money)

                await message.channel.send("<@1434299997133865030> chop chop city boii")
                return

            elif item == "#2":

                if money[user_id] < 30:
                    await message.channel.send(embed=not_enough())
                    return

                money[user_id] -= 30
                save_money(money)

                await message.channel.send("<@1434299997133865030> role bought")
                return

            elif item == "#3":

                if money[user_id] < 1000:
                    await message.channel.send(embed=not_enough())
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
                await message.channel.send("max 1000")
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

            for _ in range(5):
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
