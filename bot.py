import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    msg = message.content.lower()

    if "help" in msg:
        await message.channel.send("help is on it’s way")

    if "swano" in msg:
        await message.channel.send("swano is the goat! leave mah goat alone")

client.run(os.getenv("TOKEN"))
