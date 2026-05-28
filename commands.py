import discord
import random

NAVY = 0x1B2B5B

def setup_commands(tree, client):

    # -------------------------
    # HOW GAY
    # -------------------------
    @tree.command(name="howgay")
    async def howgay(
        interaction: discord.Interaction,
        user: discord.Member
    ):

        embed = discord.Embed(
            title="🌈 how gay",
            description=(
                f"{user.mention} is "
                f"**{random.randint(0,100)}% gay**"
            ),
            color=NAVY
        )

        await interaction.response.send_message(embed=embed)

    # -------------------------
    # HOW AUTISTIC
    # -------------------------
    @tree.command(name="howautistic")
    async def howautistic(
        interaction: discord.Interaction,
        user: discord.Member
    ):

        embed = discord.Embed(
            title="🧩 how autistic",
            description=(
                f"{user.mention} is "
                f"**{random.randint(0,100)}% autistic**"
            ),
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

        # SWANUS CANON
        if (
            (user1.id == 1434299997133865030 and user2.id == 652988923672395779)
            or
            (user1.id == 652988923672395779 and user2.id == 1434299997133865030)
        ):

            result = (
                "💍 **100% compatibility**\n"
                "ouhh swanus mentioned 👀👀👀"
            )

        else:

            result = (
                f"💘 **{random.randint(0,100)}% compatibility**"
            )

        embed = discord.Embed(
            title="💘 compatibility",
            description=(
                f"{user1.mention} + {user2.mention}\n\n"
                f"{result}"
            ),
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
            f"in {style} style, "
            f"funny gen z tone, chaotic, lowercase"
        )

        result = client.ask_ai(prompt)

        embed = discord.Embed(
            title=f"🔥 {style} glaze",
            description=result,
            color=NAVY
        )

        embed.set_footer(
            text=f"requested by {interaction.user.display_name}"
        )

        await interaction.response.send_message(embed=embed)
