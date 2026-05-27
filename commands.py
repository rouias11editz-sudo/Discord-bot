import random
import asyncio
import requests
import discord

# -------------------------
# EMBED COLOR THEME (NAVY)
# -------------------------
NAVY = 0x1B2B5B

# -------------------------
# COMMAND SETUP
# -------------------------
def setup_commands(tree, client):

    # -------------------------
    # HOW GAY
    # -------------------------
    @tree.command(name="howgay")
    async def howgay(interaction, user):

        embed = discord.Embed(
            title="🌈 gay detector",
            description=f"{user.mention} is **{random.randint(0,100)}% gay**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # HOW AUTISTIC
    # -------------------------
    @tree.command(name="howautistic")
    async def howautistic(interaction, user):

        embed = discord.Embed(
            title="🧩 autism meter",
            description=f"{user.mention} is **{random.randint(0,100)}% autistic**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # COMPATIBILITY (WITH YOUR SPECIAL IDS)
    # -------------------------
    @tree.command(name="compatibility")
    async def compatibility(interaction, user1, user2):

        if (
            (user1.id == 1434299997133865030 and user2.id == 652988923672395779)
            or
            (user1.id == 652988923672395779 and user2.id == 1434299997133865030)
        ):
            desc = f"🔥 ouuuhhhh shii swanusss\n{user1.mention} + {user2.mention} = **100% compatibility**"
        else:
            desc = f"{user1.mention} + {user2.mention} = **{random.randint(0,100)}% compatibility**"

        embed = discord.Embed(
            title="💘 compatibility test",
            description=desc,
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # GUESS NUMBER
    # -------------------------
    @tree.command(name="guess_number")
    async def guess_number(interaction):

        client.game_state[interaction.channel.id] = {
            "answer": random.randint(1, 100),
            "attempts": 10
        }

        embed = discord.Embed(
            title="🎮 guess the number",
            description="guess a number between **1-100**\n⏰ 1 minute | 10 attempts",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(60)

        if interaction.channel.id in client.game_state:

            answer = client.game_state[interaction.channel.id]["answer"]

            await interaction.channel.send(
                embed=discord.Embed(
                    title="⏰ time's up",
                    description=f"the number was **{answer}**",
                    color=NAVY
                )
            )

            del client.game_state[interaction.channel.id]

    # -------------------------
    # GUESS MEMBER
    # -------------------------
    @tree.command(name="guess_member")
    async def guess_member(interaction):

        members = [m for m in interaction.guild.members if not m.bot]
        chosen = random.choice(members)

        client.member_game[interaction.channel.id] = chosen.id

        embed = discord.Embed(
            title="👤 guess the member",
            description="type their display name (no ping)\n⏰ 1 minute",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

        await asyncio.sleep(60)

        if interaction.channel.id in client.member_game:

            member = interaction.guild.get_member(
                client.member_game[interaction.channel.id]
            )

            await interaction.channel.send(
                embed=discord.Embed(
                    title="⏰ time's up",
                    description=f"it was **{member.display_name}**",
                    color=NAVY
                )
            )

            del client.member_game[interaction.channel.id]

    # -------------------------
    # GLAZE (AI + EMBED + STYLE)
    # -------------------------
    @tree.command(name="glaze")
    async def glaze(interaction, user, style: str = "sigma"):

        styles = ["anime", "sigma", "toxic", "wholesome"]

        if style.lower() not in styles:
            style = "sigma"

        prompt = f"""
        write a short chaotic discord glaze about {user.display_name}.
        style: {style}
        1-2 sentences max, gen z slang, funny tone
        """

        headers = {
            "Authorization": "Bearer " + client.openrouter_key,
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "you are a discord glaze generator."},
                {"role": "user", "content": prompt}
            ]
        }

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if r.status_code != 200:
            await interaction.response.send_message("AI broke 💀")
            return

        result = r.json()["choices"][0]["message"]["content"]

        embed = discord.Embed(
            title=f"🔥 {style.upper()} GLAZE",
            description=result,
            color=NAVY
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed)
