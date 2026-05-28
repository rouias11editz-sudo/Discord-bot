import discord
from discord import app_commands

NAVY = 0x1B2B5B


# You must already have this somewhere in your bot
# async def call_openrouter(prompt): ...


async def setup_commands(tree):

    # -------------------------
    # COMPATIBILITY / SHIP
    # -------------------------
    @tree.command(name="ship", description="check compatibility between two users")
    async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):

        import random

        SWANUS_1 = 652988923672395779
        SWANUS_2 = 1434299997133865030

        # special override
        if (user1.id == SWANUS_1 and user2.id == SWANUS_2) or \
           (user1.id == SWANUS_2 and user2.id == SWANUS_1):

            embed = discord.Embed(
                title="💞 COMPATIBILITY TEST",
                description="SWANUS MENTIONEDD??!! ouhhh shiiii 100000% compatibility 👀👀",
                color=NAVY
            )

            await interaction.response.send_message(embed=embed)
            return

        score = random.randint(0, 100)

        embed = discord.Embed(
            title="💞 COMPATIBILITY TEST",
            description=f"{user1.mention} ❤️ {user2.mention}\n\ncompatibility: **{score}%**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)


    # -------------------------
    # GLAZE (REAL OPENROUTER AI)
    # -------------------------
    @tree.command(name="glaze", description="AI glazes a user in a chosen style")
    async def glaze(interaction: discord.Interaction, user: discord.Member, style: str):

        await interaction.response.defer()

        prompt = f"""
You are an AI that writes a single expressive paragraph glazing a user.

Target: {user.name}
Style: {style}

Rules:
- One paragraph only
- Fully AI-generated (no templates)
- Style must influence tone heavily (anime = dramatic, sigma = motivational, etc.)
- No sexual content
- Make it feel like hype narration or character introduction
- You're gen Z.
"""

        text = await call_openrouter(prompt)

        embed = discord.Embed(
            title="✨ AI GLAZE",
            description=text,
            color=NAVY
        )

        embed.add_field(name="👤 target", value=user.mention, inline=True)
        embed.add_field(name="🎨 style", value=style, inline=True)

        await interaction.followup.send(embed=embed)


    # -------------------------
    # GAY CHECK
    # -------------------------
    @tree.command(name="gay", description="check gay percentage")
    async def gay(interaction: discord.Interaction, user: discord.Member):

        import random

        score = random.randint(0, 100)

        embed = discord.Embed(
            title="🌈 GAY DETECTOR",
            description=f"{user.mention} is **{score}% gay**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)


    # -------------------------
    # AUTISM CHECK
    # -------------------------
    @tree.command(name="autistic", description="check autism level")
    async def autistic(interaction: discord.Interaction, user: discord.Member):

        import random

        score = random.randint(0, 100)

        embed = discord.Embed(
            title="🧠 AUTISM SCANNER",
            description=f"{user.mention} is **{score}% autistic**",
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)
