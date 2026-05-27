import discord
import asyncio

NAVY = 0x1B2B5B

def setup_events(client):

    @client.event
    async def on_message(message):

        if message.author.bot:
            return

        msg = message.content.lower()

        # -------------------------
        # GREETINGS
        # -------------------------
        is_owner = message.guild and message.author.id == message.guild.owner_id
        is_admin = message.author.guild_permissions.administrator

        greetings = ["hi", "hello", "hey", "yo"]

        if (is_owner or is_admin) and msg in greetings:

            embed = discord.Embed(
                description="👋",
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

        if message.author.id in allowed_spammers and msg.startswith("spam "):

            for i in range(5):
                await message.channel.send(message.content[5:])
                await asyncio.sleep(0.5)

            return

        # -------------------------
        # AUTO RESPONSES (UNCHANGED)
        # -------------------------
        responses = {
            "help": "help is on it’s way",
            "swano": "swano is the goat! leave mah goat alone",
            "venus": "venus is swano’s mommy, swano needs mama mwilkies",
            "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)",
            "jju": "if u're talking bout juhoon then ouhh shiii👀👀 twinkie jju? Ok, dttm, LEAVE.",
            "sean": "ouhh my eom freakk 😋😋😝😝 give me one chance seannnn",
            "keonho": "did you just talk about the cutest and gayest member of the group? Thats tuff dayummm",
            "juhoon": "OH MY FRICKING GOSH JUHHOON HISKAJSJS JUHOON JUHOON THATS SWANO'S BABYYYY",
            "martin": "Those holy eyes 👀 👀",
            "james": "WANNA SEE MY HELICOPTER??? 🚁",
            "gojo": "are you 19+??? gojo is mah goat",
            "hori": "Isn't that james's #1 feet licker??? she's so horny for jems 🥹👀"
        }

        for key, reply in responses.items():
            if key in msg:
                await message.channel.send(
                    embed=discord.Embed(
                        description=reply,
                        color=NAVY
                    )
                )
                return

        # -------------------------
        # AI CHAT
        # -------------------------
        if getattr(client, "ai_enabled", False):
            reply = client.ask_ai(message.content)
            await message.channel.send(reply)
