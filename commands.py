import discord
import random
import asyncio
import requests

NAVY = 0x1B2B5B

def setup_commands(tree, client):

    # -------------------------
    # HOW GAY
    # -------------------------
    @tree.command(name="howgay")
    async def howgay(interaction, user: discord.Member):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🌈 how gay",
                description=f"{user.mention} is **{random.randint(0,100)}% gay**",
                color=NAVY
            )
        )

    # -------------------------
    # HOW AUTISTIC
    # -------------------------
    @tree.command(name="howautistic")
    async def howautistic(interaction, user: discord.Member):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="🧩 how autistic",
                description=f"{user.mention} is **{random.randint(0,100)}% autistic**",
                color=NAVY
            )
        )

    # -------------------------
    # COMPATIBILITY
    # -------------------------
    @tree.command(name="compatibility")
    async def compatibility(interaction, user1: discord.Member, user2: discord.Member):

        score = random.randint(0, 100)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="💘 compatibility",
                description=f"{user1.mention} + {user2.mention}\n**{score}%**",
                color=NAVY
            )
        )

    # -------------------------
    # GLAZE (AI)
    # -------------------------
    @tree.command(name="glaze")
    async def glaze(interaction, user: discord.Member, style: str = "sigma"):

        prompt = f"glaze {user.display_name} in {style} style, funny gen z tone, 2 sentences max"

        result = client.ask_ai(prompt)

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"🔥 glaze ({style})",
                description=result,
                color=NAVY
            )
        )

    # -------------------------
    # GUESS NUMBER
    # -------------------------
    @tree.command(name="guess_number")
    async def guess_number(interaction):

        client.game_state[interaction.channel.id] = {
            "answer": random.randint(1, 100),
            "attempts": 10
        }

        await interaction.response.send_message(
            embed=discord.Embed(
                title="🎮 guess number",
                description="1-100 | 10 attempts | 60 seconds",
                color=NAVY
            )
        )

        await asyncio.sleep(60)

        if interaction.channel.id in client.game_state:
            ans = client.game_state[interaction.channel.id]["answer"]

            await interaction.channel.send(
                f"⏰ time up — answer was **{ans}**"
            )

            del client.game_state[interaction.channel.id]

    # -------------------------
    # GUESS MEMBER (NO PING)
    # -------------------------
    @tree.command(name="guess_member")
    async def guess_member(interaction):

        members = [m for m in interaction.guild.members if not m.bot]
        chosen = random.choice(members)

        client.member_game[interaction.channel.id] = chosen.id

        await interaction.response.send_message(
            embed=discord.Embed(
                title="👤 guess member",
                description="type their DISPLAY NAME",
                color=NAVY
            )
        )

        await asyncio.sleep(60)

        if interaction.channel.id in client.member_game:
            member = interaction.guild.get_member(client.member_game[interaction.channel.id])

            await interaction.channel.send(
                f"⏰ time up — it was **{member.display_name}**"
            )

            del client.member_game[interaction.channel.id]
