import discord
import asyncio
import random

# -------------------------
# EVENTS SETUP
# -------------------------
def setup_events(client):

    @client.event
    async def on_message(message):

        if message.author.bot:
            return

        msg = message.content.lower()

        # -------------------------
        # OWNER / ADMIN GREETING GIF (UNCHANGED STYLE)
        # -------------------------
        is_owner = message.guild and message.author.id == message.guild.owner_id
        is_admin = message.author.guild_permissions.administrator

        greetings = ["hi", "hello", "hey", "yo"]

        if (is_owner or is_admin) and msg in greetings:

            embed = discord.Embed(
                description="👋",
                color=0x1B2B5B
            )

            embed.set_image(
                url="https://media.tenor.com/crtsfiles-juhoon-cortis-hi-waving/0.gif"
            )

            embed.set_author(
                name=f"Greetings from {message.author.display_name}",
                icon_url=message.author.display_avatar.url
            )

            await message.channel.send(embed=embed)
            return

        # -------------------------
        # SPAM SYSTEM (UNCHANGED LOGIC)
        # -------------------------
        allowed_spammers = {
            1208382519611760670,
            1434299997133865030,
            652988923672395779,
            1148948508481699850
        }

        if message.author.id in allowed_spammers and msg.startswith("spam "):

            spam_text = message.content[5:]

            for i in range(5):
                await message.channel.send(spam_text)
                await asyncio.sleep(0.6)

            return

        # -------------------------
        # AUTO RESPONSES (UNCHANGED CONTENT)
        # -------------------------
        responses = {
            "help": "help is on it’s way",
            "swano": "swano is the goat! leave mah goat alone",
            "venus": "venus is swano’s mommy, swano needs mama mwilkies",
            "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)",
            "jju": "if u're talking bout juhoon then ouhh shiii👀👀 twinkie jju? Ok, dttm, LEAVE.",
            "sean": "ouhh my eom freakk 😋😋😝😝 give me one chance seannnn",
            "keonho": "did you just talk about the cutest and gayest member of the group? Thats tuff dayummm",
            "juhoon": "OH MY FRICKING GOSH JUHHOON HISKAJSJS JUHOON JUHOON",
            "martin": "Those holy eyes 👀 👀",
            "james": "WANNA SEE MY HELICOPTER??? 🚁",
            "gojo": "are you 19+??? gojo is mah goat",
            "hori": "👀👀"
        }

        for key, reply in responses.items():
            if key in msg:

                embed = discord.Embed(
                    description=reply,
                    color=0x1B2B5B
                )

                embed.set_author(
                    name="AUTO RESPONSE",
                    icon_url=message.author.display_avatar.url
                )

                await message.channel.send(embed=embed)
                return

        # -------------------------
        # AI CHAT (ONLY IF ENABLED)
        # -------------------------
        if getattr(client, "ai_enabled", False):

            # IMPORTANT: your bot.py must set this flag
            # client.ai_enabled = True / False

            reply = await client.loop.run_in_executor(
                None,
                client.ask_ai,
                message.content
            )

            await message.channel.send(reply)
            return
