import discord
import asyncio
import random
import time
import aiosqlite

from database import get_level, add_message, level_up

NAVY = 0x1B2B5B
DB_NAME = "swano.db"

daily_cooldown = {}
work_cooldown = {}

# -------------------------
# SQLITE MONEY
# -------------------------
async def get_money(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        async with db.execute(
            "SELECT money FROM economy WHERE user_id = ?",
            (str(user_id),)
        ) as cursor:

            row = await cursor.fetchone()

            return row[0] if row else 0


async def add_money(user_id, amount):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            INSERT INTO economy (user_id, money)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET money = money + ?
        """, (str(user_id), amount, amount))

        await db.commit()


# -------------------------
# SETUP EVENTS
# -------------------------
def setup_events(client):

    @client.event
    async def on_message(message):

        if message.author.bot:
            return

        msg = message.content.lower()
        user_id = str(message.author.id)

        # -------------------------
        # LEVEL SYSTEM (SQLITE)
        # -------------------------
        await add_message(user_id)

        messages, level, last_msg, last_lvl = await get_level(user_id)

        if messages >= 150:

            await level_up(user_id)

            embed = discord.Embed(
                title="🎉 LEVEL UP",
                description=f"you are now level **{level + 1}**",
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # LEVEL COMMAND
        # -------------------------
        if msg == "swano level":

            embed = discord.Embed(
                title="📊 YOUR LEVEL",
                description=(
                    f"level: **{level}**\n"
                    f"messages: **{messages}/150**\n"
                    f"last message: **{last_msg}**\n"
                    f"last level up: **{last_lvl}**"
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
                "probably",
                "maybe",
                "yes",
                "no",
                "100% yes",
                "not happening",
                "never",
                "ask again later"
                "idfk ask chatgpt",
                "i didnt quite understand buddy",
                "uhmm..",
                "ask again later im on my break",
                "leave me alone."
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
        # AI TOGGLE
        # -------------------------
        if msg == "ai work":
            client.ai_enabled = True
            await message.channel.send("yo wsgg its me ai auote crewmate bot 🤖")
            return

        if msg == "ai stop":
            client.ai_enabled = False
            await message.channel.send("💤 ai off")
            return

        # -------------------------
        # BALANCE
        # -------------------------
        if msg == "swano balance":

            money = await get_money(user_id)

            embed = discord.Embed(
                title="💰 SWUCKS",
                description=f"{money} swucks",
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

            await add_money(user_id, 250)

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

            jobs = [
                (30, "💼 CEO", 50, "you fired employees"),
                (25, "🩺 Doctor", 40, "you healed people"),
                (20, "👨‍🍳 Chef", 30, "you burned food"),
                (15, "🔥 Firefighter", 25, "you saved cats"),
                (10, "🚔 Police", 15, "you arrested raccoon"),
                (5, "☕ Barista", 8, "you made coffee"),
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

            await add_money(user_id, pay)

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
                    "#1 Swano meowing vm - 500 swucks\n"
                    "#2 Custom role - 30 swicks\n"
                    "#3 Dare swano to do anything - 1000 swucks"
                ),
                color=NAVY
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # BUY
        # -------------------------
        if msg.startswith("swano buy"):

            parts = msg.split()
            if len(parts) < 3:
                return

            item = parts[2]
            money = await get_money(user_id)

            def brokie():
                return discord.Embed(
                    title="💀 BROKIE",
                    description="fricking brokie go get rich",
                    color=NAVY
                )

            if item == "#1":
                if money < 500:
                    await message.channel.send(embed=brokie())
                    return

                await add_money(user_id, -500)
                await message.channel.send("<@1434299997133865030> chop chop city boii")
                return

            if item == "#2":
                if money < 30:
                    await message.channel.send(embed=brokie())
                    return

                await add_money(user_id, -30)
                await message.channel.send("<@1434299997133865030> role purchased")
                return

            if item == "#3":
                if money < 1000:
                    await message.channel.send(embed=brokie())
                    return

                await add_money(user_id, -1000)
                await message.channel.send(
                    f"<@1434299997133865030> chop chop do the dare for {message.author.mention}"
                )
                return

        # -------------------------
        # ADMIN GRANT MONEY
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

            if not message.mentions:
                return

            target = message.mentions[0]

            await add_money(target.id, amount)

            await message.channel.send(f"gave {amount} swucks to {target.mention}")
            return

        # -------------------------
        # ADMIN GIVE MESSAGES
        # -------------------------
        if msg.startswith("swano give"):

            if not message.author.guild_permissions.administrator:
                await message.channel.send("admins only")
                return

            parts = message.content.split()

            if len(parts) < 3 or not message.mentions:
                return

            target = message.mentions[0]
            amount = int(parts[-1])

            if amount > 500:
                await message.channel.send("max 500 messages")
                return

            # directly update levels via helper
            for _ in range(amount):
                await add_message(target.id)

            await message.channel.send(f"gave {amount} messages to {target.mention}")
            return

        # -------------------------
        # LEADERBOARD
        # -------------------------
        if msg == "swano leaderboard":

            async with aiosqlite.connect(DB_NAME) as db:

                async with db.execute("""
                    SELECT e.user_id, e.money, COALESCE(l.level, 0)
                    FROM economy e
                    LEFT JOIN levels l ON e.user_id = l.user_id
                    ORDER BY e.money DESC
                    LIMIT 10
                """) as cursor:

                    rows = await cursor.fetchall()

            desc = ""

            for i, (uid, money, lvl) in enumerate(rows, start=1):
                desc += f"**{i}.** <@{uid}> — 💰 {money} swucks | 📊 lvl {lvl}\n"

            embed = discord.Embed(
                title="🏆 SWANO LEADERBOARD",
                description=desc,
                color=NAVY
            )

            await message.channel.send(embed=embed)
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
