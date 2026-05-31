import discord
from discord.ext import commands

class SwanoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x001f3f

    # ───── P4P ─────
    @commands.command()
    async def swano_p4p(self, ctx):
        embed = discord.Embed(
            description=
            "୨୧ ────────────── ୨୧\n\n"
            "♡ Ping 4 Ping\n\n"
            "✧ Send our ad in your partnership channel\n\n"
            "✧ Send an uncropped screenshot as proof\n\n"
            "✧ Send your ad here so we can post it as soon as possible\n\n"
            "₊˚ Thank you for partnering with us! ♡\n\n"
            "୨୧ ────────────── ୨୧",
            color=self.color
        )
        await ctx.send(embed=embed)

    # ───── PARTNERSHIP ─────
    @commands.command()
    async def swano_partnership(self, ctx):
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
            "₊˚ Thank you for your interest in partnering with us!\n\n"
            "୨୧ ────────────── ୨୧",
            color=self.color
        )
        await ctx.send(embed=embed)

    # ───── BLIST ─────
    @commands.command()
    async def swano_blist(self, ctx):
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
            "₊˚ Thank you for helping keep our community safe ♡\n\n"
            "୨୧ ────────────── ୨୧",
            color=self.color
        )
        await ctx.send(embed=embed)

    # ───── HELP ─────
    @commands.command()
    async def swano_help(self, ctx):
        embed = discord.Embed(
            description=
            "୨୧ ────────────── ୨୧\n\n"
            "🆘 Help & Support\n\n"
            "✧ Need help? Explain below\n\n"
            "• Questions\n• Issues\n• Support\n\n"
            "₊˚ We’re happy to help! ♡\n\n"
            "୨୧ ────────────── ୨୧",
            color=self.color
        )
        await ctx.send(embed=embed)

    # ───── APPLY ─────
    @commands.command()
    async def swano_apply(self, ctx):
        embed = discord.Embed(
            description=
            "୨୧ ────────────── ୨୧\n\n"
            "🛡️ Moderator Applications\n\n"
            "✧ Level 25+\n"
            "✧ 1 week+ in server\n"
            "✧ 500+ messages\n\n"
            "₊˚ Good luck! ♡\n\n"
            "୨୧ ────────────── ୨୧",
            color=self.color
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(SwanoCommands(bot))
