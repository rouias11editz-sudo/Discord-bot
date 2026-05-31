import discord
from discord.ext import commands

class SwanoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower().strip()

        # ───── ONLY SWANO COMMANDS ─────
        if not content.startswith("swano "):
            return

        color = 0x001f3f  # navy blue

        # ───── P4P ─────
        if content == "swano p4p":
            embed = discord.Embed(
                description=
                "୨୧ ────────────── ୨୧\n\n"
                "♡ Ping 4 Ping\n\n"
                "✧ Send our ad in your partnership channel\n\n"
                "✧ Send an uncropped screenshot as proof\n\n"
                "✧ Send your ad here so we can post it as soon as possible\n\n"
                "₊˚ Thank you for partnering with us! ♡\n\n"
                "୨୧ ────────────── ୨୧",
                color=color
            )
            await message.channel.send(embed=embed)
            return

        # ───── PARTNERSHIP ─────
        elif content == "swano partnership":
            embed = discord.Embed(
                description=
                "୨୧ ────────────── ୨୧\n\n"
                "🤝 Partnership Request\n\n"
                "✧ Send your server advertisement below\n\n"
                "✧ Partnership Requirements\n"
                "• 50+ members\n"
                "• Fully SFW community\n"
                "• Stox community\n\n"
                "✧ A staff member will review your request\n\n"
                "✧ Please be patient while waiting for a response ♡\n\n"
                "₊˚ Thank you for your interest in partnering with us!\n\n"
                "୨୧ ────────────── ୨୧",
                color=color
            )
            await message.channel.send(embed=embed)
            return

        # ───── BLIST ─────
        elif content == "swano blist":
            embed = discord.Embed(
                description=
                "୨୧ ────────────── ୨୧\n\n"
                "📋 Blacklist Submission\n\n"
                "✧ Submit your blacklist report below\n\n"
                "✧ Please include:\n"
                "• User ID\n"
                "• Reason for blacklist\n"
                "• Valid proof/evidence\n\n"
                "✧ Reports without sufficient proof may be denied\n\n"
                "✧ A staff member will review your submission\n\n"
                "✧ Please be patient while waiting for a response ♡\n\n"
                "₊˚ Thank you for helping keep our community safe ♡\n\n"
                "୨୧ ────────────── ୨୧",
                color=color
            )
            await message.channel.send(embed=embed)
            return

        # ───── HELP ─────
        elif content == "swano help":
            embed = discord.Embed(
                description=
                "୨୧ ────────────── ୨୧\n\n"
                "🆘 Help & Support\n\n"
                "✧ Need help with something? Feel free to explain your issue below!\n\n"
                "✧ You may use this ticket for:\n"
                "• Questions or concerns\n"
                "• Reporting issues\n"
                "• Server-related assistance\n"
                "• General support\n\n"
                "✧ Please provide as much detail as possible so we can assist you better ♡\n\n"
                "✧ Please be patient while waiting for a staff member to respond\n\n"
                "₊˚ We’re happy to help! ♡\n\n"
                "୨୧ ────────────── ୨୧",
                color=color
            )
            await message.channel.send(embed=embed)
            return

        # ───── APPLY ─────
        elif content == "swano apply":
            embed = discord.Embed(
                description=
                "୨୧ ────────────── ୨୧\n\n"
                "🛡️ Moderator Applications\n\n"
                "✧ Interested in becoming a moderator? Send your application below!\n\n"
                "✧ Requirements\n"
                "• Level 25+\n"
                "• Must have been in the server for at least 1 week\n"
                "• 500+ messages overall\n\n"
                "✧ Applications will be reviewed by staff\n\n"
                "✧ Please be honest and detailed in your application ♡\n\n"
                "₊˚ Good luck! We look forward to reading your application ♡\n\n"
                "୨୧ ────────────── ୨୧",
                color=color
            )
            await message.channel.send(embed=embed)
            return


async def setup(bot):
    await bot.add_cog(SwanoCommands(bot))
