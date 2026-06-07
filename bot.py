import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

responses = {
    "gojo": "*He pulled you onto his lap, his strong arms wrapping around your waist possessively.* \"Okay okay... I love your cortisol chat friends. They're cool.\" *He pressed a kiss to your neck, his voice dropping lower.* \"But you're right—Gojo is literally the coolest, sexiest thing that ever happened to me. No competition, baby.\"",

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
    "kisi": "IM IN THE THICK OF IT EVERYBODY KNOWS",
    "kijo: oh SHE? KIJO got the DOOR READY FOR U 🚪👈🏼"
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    # partial match system (not exact match anymore)
    for key, response in responses.items():
        if key in msg:
            embed = discord.Embed(
                title=key.capitalize(),
                description=response,
                color=0x000080  # navy blue
            )
            await message.channel.send(embed=embed)
            break  # prevents multiple triggers

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
