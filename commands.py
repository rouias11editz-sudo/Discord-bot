import discord
import random
import asyncio
import requests
import json
import time

NAVY = 0x1B2B5B

# -------------------------
# MONEY FUNCTIONS
# -------------------------
def load_money():
    with open("money.json", "r") as f:
        return json.load(f)

def save_money(data):
    with open("money.json", "w") as f:
        json.dump(data, f, indent=4)

daily_cooldown = {}

def setup_commands(tree, client):

    # -------------------------
    # HOW GAY
    # -------------------------
    @tree.command(name="howgay")
    async def howgay(interaction: discord.Interaction, user: discord.Member):

        embed = discord.Embed(
            title="🌈 how gay",
            description=f"{user.mention} is **{random.randint(0,100)}% gay**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # HOW AUTISTIC
    # -------------------------
    @tree.command(name="howautistic")
    async def howautistic(interaction: discord.Interaction, user: discord.Member):

        embed = discord.Embed(
            title="🧩 how autistic",
            description=f"{user.mention} is **{random.randint(0,100)}% autistic**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # COMPATIBILITY
    # -------------------------
    @tree.command(name="compatibility")
    async def compatibility(
        interaction: discord.Interaction,
        user1: discord.Member,
        user2: discord.Member
    ):

        if (
            (user1.id == 1434299997133865030 and user2.id == 652988923672395779)
            or
            (user1.id == 652988923672395779 and user2.id == 1434299997133865030)
        ):

            result = (
                f"ouhh swanus mentioned??\n"
                f"{user1.mention} + {user2.mention}\n\n"
                f"💍 **100% compatibility** 👀👀👀"
            )

        else:

            result = (
                f"{user1.mention} + {user2.mention}\n\n"
                f"💘 **{random.randint(0,100)}% compatibility**"
            )

        embed = discord.Embed(
            title="💘 compatibility",
            description=result,
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # GLAZE
    # -------------------------
    @tree.command(name="glaze")
    async def glaze(
        interaction: discord.Interaction,
        user: discord.Member,
        style: str = "sigma"
    ):

        prompt = (
            f"glaze {user.display_name} "
            f"in {style} style, funny gen z tone, short response"
        )

        result = client.ask_ai(prompt)

        embed = discord.Embed(
            title=f"🔥 {style} glaze",
            description=result,
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # GUESS NUMBER
    # -------------------------
    @tree.command(name="guess_number")
    async def guess_number(interaction: discord.Interaction):

        client.game_state[interaction.channel.id] = {
            "answer": random.randint(1, 100),
            "attempts": 10
        }

        embed = discord.Embed(
            title="🎮 guess number",
            description=(
                "guess a number between **1-100**\n\n"
                "⏰ 1 minute\n"
                "🎯 10 attempts"
            ),
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(60)

        if interaction.channel.id in client.game_state:

            answer = client.game_state[interaction.channel.id]["answer"]

            timeout_embed = discord.Embed(
                title="⏰ time up",
                description=f"the number was **{answer}**",
                color=NAVY
            )

            await interaction.channel.send(embed=timeout_embed)

            del client.game_state[interaction.channel.id]

    # -------------------------
    # GUESS MEMBER
    # -------------------------
    @tree.command(name="guess_member")
    async def guess_member(interaction: discord.Interaction):

        members = [
            m for m in interaction.guild.members
            if not m.bot
        ]

        chosen = random.choice(members)

        client.member_game[interaction.channel.id] = chosen.id

        embed = discord.Embed(
            title="👤 guess member",
            description=(
                "guess the member by typing\n"
                "their display name\n\n"
                "⏰ 1 minute"
            ),
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(60)

        if interaction.channel.id in client.member_game:

            member = interaction.guild.get_member(
                client.member_game[interaction.channel.id]
            )

            timeout_embed = discord.Embed(
                title="⏰ time up",
                description=f"it was **{member.display_name}**",
                color=NAVY
            )

            await interaction.channel.send(embed=timeout_embed)

            del client.member_game[interaction.channel.id]

    # -------------------------
    # 8BALL
    # -------------------------
    @tree.command(name="8ball")
    async def eightball(
        interaction: discord.Interaction,
        question: str
    ):

        thinking_embed = discord.Embed(
            title="🎱 8ball",
            description=(
                f"**Question:** {question}\n\n"
                "🤔 Thinking....."
            ),
            color=NAVY
        )

        await interaction.response.send_message(embed=thinking_embed)

        msg = await interaction.original_response()

        await asyncio.sleep(2)

        answers = [
            "Probably",
            "Maybe",
            "Yes",
            "Maybe not",
            "Maybe yes",
            "Not happening",
            "100% true",
            "Nope",
            "Not at all",
            "Never"
        ]

        result = random.choice(answers)

        result_embed = discord.Embed(
            title="🎱 8ball",
            description=(
                f"**Question:** {question}\n\n"
                f"🎯 {result}"
            ),
            color=NAVY
        )

        await msg.edit(embed=result_embed)

    # -------------------------
    # BALANCE
    # -------------------------
    @tree.command(name="balance")
    async def balance(interaction: discord.Interaction):

        data = load_money()

        user_id = str(interaction.user.id)

        if user_id not in data:
            data[user_id] = 0
            save_money(data)

        embed = discord.Embed(
            title="💰 swucks balance",
            description=f"you have **{data[user_id]} swucks**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # DAILY
    # -------------------------
    @tree.command(name="daily")
    async def daily(interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        current_time = time.time()

        if user_id in daily_cooldown:

            last_claim = daily_cooldown[user_id]

            if current_time - last_claim < 86400:

                remaining = int(
                    (86400 - (current_time - last_claim)) / 3600
                )

                embed = discord.Embed(
                    title="⏳ daily cooldown",
                    description=f"come back in {remaining} hours",
                    color=NAVY
                )

                await interaction.response.send_message(embed=embed)

                return

        daily_cooldown[user_id] = current_time

        data = load_money()

        if user_id not in data:
            data[user_id] = 0

        reward = 50

        data[user_id] += reward

        save_money(data)

        embed = discord.Embed(
            title="🎁 daily swucks",
            description=f"you received **{reward} swucks**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # SHOP
    # -------------------------
    @tree.command(name="shop")
    async def shop(interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛒 swucks shop",
            description=(
                "🐱 **swano meowing VM** — 500 swucks\n\n"
                "🎨 **custom role** — 30 swucks\n\n"
                "😈 **dare swano to do anything** — 1000 swucks"
            ),
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)
