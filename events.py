import discord
import asyncio
import json

NAVY = 0x1B2B5B

def setup_events(client):

    @client.event
    async def on_message(message):

        if message.author.bot:
            return

        msg = message.content.lower()

        channel_id = message.channel.id

        # -------------------------
        # GUESS NUMBER GAME
        # -------------------------
        if channel_id in client.game_state:

            if message.content.isdigit():

                guess = int(message.content)

                # WARNING IF ABOVE 100
                if guess > 100:

                    embed = discord.Embed(
                        title="🚨 invalid number",
                        description="the number is only between 1-100",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    return

                game = client.game_state[channel_id]

                answer = game["answer"]

                game["attempts"] -= 1

                # CORRECT
                if guess == answer:

                    with open("money.json", "r") as f:
                        data = json.load(f)

                    user_id = str(message.author.id)

                    if user_id not in data:
                        data[user_id] = 0

                    data[user_id] += 50

                    with open("money.json", "w") as f:
                        json.dump(data, f, indent=4)

                    embed = discord.Embed(
                        title="🎉 correct!",
                        description=(
                            f"{message.author.mention} guessed the number!\n\n"
                            "💰 +50 swucks"
                        ),
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    del client.game_state[channel_id]

                    return

                # NO ATTEMPTS LEFT
                if game["attempts"] <= 0:

                    embed = discord.Embed(
                        title="💀 no attempts left",
                        description=f"the number was **{answer}**",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    del client.game_state[channel_id]

                    return

                # HIGHER
                elif guess < answer:

                    embed = discord.Embed(
                        title="⬆️ higher",
                        description=f"{game['attempts']} attempts left",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                # LOWER
                else:

                    embed = discord.Embed(
                        title="⬇️ lower",
                        description=f"{game['attempts']} attempts left",
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                return

        # -------------------------
        # GUESS MEMBER GAME
        # -------------------------
        if channel_id in client.member_game:

            correct_member_id = client.member_game[channel_id]

            correct_member = message.guild.get_member(correct_member_id)

            if correct_member:

                if msg == correct_member.display_name.lower():

                    with open("money.json", "r") as f:
                        data = json.load(f)

                    user_id = str(message.author.id)

                    if user_id not in data:
                        data[user_id] = 0

                    data[user_id] += 50

                    with open("money.json", "w") as f:
                        json.dump(data, f, indent=4)

                    embed = discord.Embed(
                        title="🎉 correct!",
                        description=(
                            f"{message.author.mention} guessed the member!\n\n"
                            "💰 +50 swucks"
                        ),
                        color=NAVY
                    )

                    await message.channel.send(embed=embed)

                    del client.member_game[channel_id]

                    return

        # -------------------------
        # OWNER / ADMIN GREETING
        # -------------------------
        is_owner = (
            message.guild and
            message.author.id == message.guild.owner_id
        )

        is_admin = message.author.guild_permissions.administrator

        greetings = ["hi", "hello", "hey", "yo"]

        if (is_owner or is_admin) and msg in greetings:

            embed = discord.Embed(
                description="👋",
                color=NAVY
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
        # AI TOGGLE
        # -------------------------
        if msg == "ai work":

            client.ai_enabled = True

            embed = discord.Embed(
                title="🤖 ai enabled",
                description="yoo its me crewmate ai wsg!!",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        if msg == "ai stop":

            client.ai_enabled = False

            embed = discord.Embed(
                title="💤 ai disabled",
                description="baaalright im gone now bai",
                color=NAVY
            )

            await message.channel.send(embed=embed)

            return

        # -------------------------
        # SPAM COMMAND
        # -------------------------
        allowed_spammers = {
            1208382519611760670,
            1434299997133865030,
            652988923672395779,
            1148948508481699850
        }

        if (
            message.author.id in allowed_spammers
            and msg.startswith("spam ")
        ):

            spam_text = message.content[5:]

            for i in range(5):

                await message.channel.send(spam_text)

                await asyncio.sleep(0.6)

            return

        # -------------------------
        # AUTO RESPONSES
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
            "martin": "Those holy predatory eyes 👀 👀",
            "james": "WANNA SEE MY HELICOPTER??? 🚁",
            "gojo": "are you 19+??? gojo is mah goat",
            "hori": "Isn't that james's #1 feet licker??? she's so horny for jems 🥹👀"
        }

        for key, reply in responses.items():

            if key in msg:

                embed = discord.Embed(
                    description=reply,
                    color=NAVY
                )

                embed.set_author(
                    name="AUTO RESPONSE",
                    icon_url=message.author.display_avatar.url
                )

                await message.channel.send(embed=embed)

                return

        # -------------------------
        # AI CHAT
        # -------------------------
        if client.ai_enabled:

            reply = client.ask_ai(message.content)

            await message.channel.send(reply)

            return
