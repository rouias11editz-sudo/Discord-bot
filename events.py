import discord
import aiosqlite
import random
import asyncio
from datetime import datetime, timedelta

NAVY = 0x1B2B5B

AI_ENABLED = True
WORK_COOLDOWNS = {}


# -------------------------
# DATABASE HELPERS
# -------------------------
async def add_money(user_id, amount):
    async with aiosqlite.connect("swano.db") as db:
        await db.execute("""
        INSERT INTO economy (user_id, money)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET money = money + ?
        """, (user_id, amount, amount))
        await db.commit()


async def get_money(user_id):
    async with aiosqlite.connect("swano.db") as db:
        async with db.execute("SELECT money FROM economy WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def add_message(user_id):
    async with aiosqlite.connect("swano.db") as db:
        await db.execute("""
        INSERT INTO levels (user_id, messages)
        VALUES (?, 1)
        ON CONFLICT(user_id) DO UPDATE SET messages = messages + 1
        """, (user_id,))
        await db.commit()


# -------------------------
# EVENTS SETUP
# -------------------------
async def setup_events(bot):

    @bot.event
    async def on_message(message):

        global AI_ENABLED

        if message.author.bot:
            return

        msg = message.content.lower()

        # -------------------------
        # LEVEL SYSTEM
        # -------------------------
        await add_message(message.author.id)

        async with aiosqlite.connect("swano.db") as db:
            async with db.execute("SELECT messages FROM levels WHERE user_id=?", (message.author.id,)) as cur:
                row = await cur.fetchone()

            if row:
                level = row[0] // 150

                await db.execute("""
                INSERT INTO levels (user_id, level)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET level=?
                """, (message.author.id, level, level))

                await db.commit()

        # -------------------------
        # AUTORESPONSES (UNCHANGED EXACT)
        # -------------------------
        responses = {
            "gojo": "are you 19+??? gojo is mah goat",
            "hori": "Isn't that james's #1 feet licker??? she's so horny for jems 🥹👀",
            "swano": "BOII WHAT U SAY BOUT MAH GOAT SWANO! BOIII TS AINT TUFFF! 😐🫱🫱🫱",
            "venus": "venus is swanie’s mommyyyy, swano needs mwommy mwilkies *blush*",
            "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet ☄️)",
            "jju": "OMG JUHOON MY BABYYYY! If ure talking bout sum twinkie jju then dttm, leave asap.",
            "juhoon": "OMG JUHOON SIAOAJIDJDKS THATS SWANOS HUBBYYY",
            "martin": "those holy predatory godly sexy eyes 👀",
            "james": "WANNA SEE MY HELICOPTER?? 🚁",
            "sean": "my eom freak 👅 👅 👅 👅 sean one chance pls",
            "keonho": "AWHH URE TALKIJG ANOUT THE CUTEST AND GAYEST MEMBERRR! we love gay keonho<3",
            "devil": "never knew the devil was a twink.",
            "kisiel": "IM IN THE THICK OF IT EVERYBODY KNOWS"
        }

        for key in responses:
            if key in msg:
                await message.channel.send(responses[key])
                break

        # -------------------------
        # AI TOGGLE (UNCHANGED)
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
        # 8BALL (UNCHANGED EXACT)
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
                "ask again later",
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
        # WORK / JOBS
        # -------------------------
        if msg.startswith("swano work"):

            user_id = message.author.id
            now = datetime.utcnow()

            if user_id in WORK_COOLDOWNS:
                if now < WORK_COOLDOWNS[user_id]:
                    remaining = int((WORK_COOLDOWNS[user_id] - now).seconds / 60)
                    await message.channel.send(f"wait {remaining} min ⏳")
                    return

            async with aiosqlite.connect("swano.db") as db:
                async with db.execute("SELECT level FROM levels WHERE user_id=?", (user_id,)) as cur:
                    row = await cur.fetchone()
                    level = row[0] if row else 0

            jobs = [
                ("Janitor", 3, 1),
                ("Barista", 8, 5),
                ("Police Officer", 15, 10),
                ("Firefighter", 25, 15),
                ("Chef", 30, 20),
                ("Doctor", 40, 25),
                ("CEO", 50, 30)
            ]

            available = [j for j in jobs if level >= j[2]]

            if not available:
                await message.channel.send("no jobs unlocked yet 💀")
                return

            job = random.choice(available)

            await add_money(user_id, job[1])

            WORK_COOLDOWNS[user_id] = now + timedelta(minutes=30)

            await message.channel.send(f"💼 worked as {job[0]} +{job[1]} swucks")
            return

        # -------------------------
        # SWANO BUY (EXACT SHOP SYSTEM)
        # -------------------------
        if msg.startswith("swano buy"):

            user_id = message.author.id
            item = msg.replace("swano buy", "").strip()

            shop = {
                "#1": ("Swano meowing vm", 500),
                "#2": ("Custom role", 30),
                "#3": ("Dare swano to do anything", 1000)
            }

            if item not in shop:
                await message.channel.send("invalid item 💀")
                return

            name, price = shop[item]

            money = await get_money(user_id)

            if money < price:
                await message.channel.send("fricking brokie go get rich 💀")
                return

            await add_money(user_id, -price)

            await message.channel.send(
                f"✅ {message.author.mention} purchased {name} for {price} swucks"
            )
            return

        # -------------------------
        # SPAM (ADMIN ONLY)
        # -------------------------
        if msg.startswith("swano spam"):

            if not message.author.guild_permissions.administrator:
                await message.channel.send("admins only")
                return

            parts = message.content.split()

            try:
                times = int(parts[-1])
            except:
                return

            if times > 15:
                await message.channel.send("max 15")
                return

            text = " ".join(parts[2:-1])

            for _ in range(times):
                await message.channel.send(text)
                await asyncio.sleep(0.3)

            return

        # -------------------------
        # ADMIN GRANT
        # -------------------------
        if msg.startswith("swano grant"):

            if not message.author.guild_permissions.administrator:
                return

            parts = message.content.split()

            if not message.mentions:
                return

            try:
                amount = int(parts[2].replace("sw", ""))
            except:
                return

            if amount > 1000:
                return

            target = message.mentions[0]

            await add_money(target.id, amount)
            await message.channel.send(f"gave {amount} swucks to {target.mention}")
            return

        # -------------------------
        # ADMIN GIVE (MESSAGES)
        # -------------------------
        if msg.startswith("swano give"):

            if not message.author.guild_permissions.administrator:
                return

            parts = message.content.split()

            if not message.mentions:
                return

            try:
                amount = int(parts[2])
            except:
                return

            target = message.mentions[0]

            for _ in range(amount):
                await add_message(target.id)

            await message.channel.send(f"gave {amount} messages to {target.mention}")
            return

        # -------------------------
        # PROCESS COMMANDS
        # -------------------------
        await bot.process_commands(message)
