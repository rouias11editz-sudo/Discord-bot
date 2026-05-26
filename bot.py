import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

responses = {
    "help": "help is on it’s way",
    "swano": "swano is the goat! leave mah goat alone",
    "venus": "venus is swano’s mommy, swano needs mama mwilkies",
    "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)"
}

@client.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    for key, reply in responses.items():
        if key in msg:
            await message.channel.send(reply)

client.run(os.getenv("TOKEN"))
