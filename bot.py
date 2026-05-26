import discord
import os
import requests

ai_enabled = False

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ---------------------------
# GROQ AI SETUP
# ---------------------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a friendly Discord chatbot."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    # safety check (prevents crash if API fails)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "AI error: try again later."

# ---------------------------
# BOT EVENTS
# ---------------------------
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
