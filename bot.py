import discord
import os
ai_enabled = False

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    global ai_enabled

    if message.author.bot:
        return

    msg = message.content.lower()

    # TURN AI ON
    if msg == "ai work":
        ai_enabled = True
        await message.channel.send("AI is now online 🤖")
        return

    # TURN AI OFF
    if msg == "ai stop":
        ai_enabled = False
        await message.channel.send("AI is now offline 📴")
        return

    # NORMAL RESPONSES (your old system)
    responses = {
        "help": "help is on it’s way",
        "swano": "swano is the goat! leave mah goat alone",
        "venus": "venus is swano’s mommy, swano needs mama mwilkies",
        "archa": "i love archa (platonic intention no sexual intention feet prevention quote motivation, sending love from cosmic comet planet)"
    }

    for key, reply in responses.items():
        if key in msg:
            await message.channel.send(reply)
            return

    # AI MODE (placeholder for now)
    if ai_enabled:
        await message.channel.send("AI is thinking... (we will connect real AI next)")

client.run(os.getenv("TOKEN"))
