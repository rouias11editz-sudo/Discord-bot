import discord
from discord.ext import commands

MOD_CHANNEL_ID = 1510608455856029750

MOD_ROLE_IDS = [
    1510271113651818717,
    1510273045691109417,
    1510273298850910348,
    1510273221172396032
]

AUTO_RESPONSES = {
    "gojo": "are you 19+??? gojo is mah goat",
    "hori": "Isn't that james's #1 feet licker??? she's so excited for jems 🥹👀",
    "swano": "BOII WHAT U SAY BOUT MAH GOAT SWANO! BOIII TS AINT TUFFF! 😐🫱🫱🫱",
    "venus": "venus likes to call swano good puppy and swano likes it",
    "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet ☄️)",
    "jju": "OMG JUHOON MY BABYYYY! If ure talking bout sum other jju then dttm, leave asap.",
    "juhoon": "OMG JUHOON SIAOAJIDJDKS THATS SWANOS HUBBYYY",
    "martin": "those holy predatory godly eyes 👀",
    "james": "WANNA SEE MY HELICOPTER?? 🚁",
    "sean": "my eom freak 👅 👅 👅 👅 sean one chance pls",
    "keonho": "AWHH URE TALKIJG ANOUT THE CUTEST AND GAYEST MEMBERRR! we love gay keonho<3",
    "devil": "never knew the devil was a twink.",
    "kisi": "IM IN THE THICK OF IT EVERYBODY KNOWS"
}

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower().strip()

        # ───── AUTO RESPONSES (EXACT MATCH ONLY) ─────
        if content in AUTO_RESPONSES:
            embed = discord.Embed(
                description=AUTO_RESPONSES[content],
                color=0x001f3f  # navy blue
            )
            await message.channel.send(embed=embed)
            return

        # ───── MODS SYSTEM ─────
        if "mods" in content:
            channel = self.bot.get_channel(MOD_CHANNEL_ID)

            if channel:
                role_mentions = " ".join([f"<@&{r}>" for r in MOD_ROLE_IDS])

                link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

                embed = discord.Embed(
                    title="🚨 mod needed asap",
                    description=
                    f"{role_mentions}\n\n"
                    f"📍 {message.channel.mention}\n"
                    f"🔗 [Jump to message]({link})",
                    color=0x001f3f
                )

                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
