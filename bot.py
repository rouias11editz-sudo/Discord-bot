import discord
import os
import requests

ai_enabled = False

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# -------------------------
# OPENROUTER AI FUNCTION
# -------------------------
def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://discordbot.local",
        "X-Title": "Discord Bot"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a friendly Discord chatbot."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return f"AI Error {response.status_code}: {response.text}"

    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# BOT EVENTS
# -------------------------
@client.event
async def on_message(message):
    global ai_enabled

    if message.author.bot:
        return

    msg = message.content.lower()

    # AI ON
    if msg == "ai work":
        ai_enabled = True
        await message.channel.send("AI is now online 🤖")
        return

    # AI OFF
    if msg == "ai stop":
        ai_enabled = False
        await message.channel.send("AI is now offline 📴")
        return

    # NORMAL RESPONSES
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

    # AI MODE
    if ai_enabled:
        reply = ask_ai(message.content)
        await message.channel.send(reply)
        return

client.run(os.getenv("TOKEN"))
