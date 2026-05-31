import discord
from discord.ext import commands

class SwanoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ───── P4P ─────
    @commands.command()
    async def p4p(self, ctx):
        await self.send_embed(ctx, "♡ Ping 4 Ping\n\n✧ Send our ad in your partnership channel\n\n✧ Send an uncropped screenshot as proof\n\n✧ Send your ad here so we can post it as soon as possible\n\n₊˚ Thank you for partnering with us! ♡")

    # ───── PARTNERSHIP ─────
    @commands.command()
    async def partnership(self, ctx):
        await self.send_embed(ctx, "🤝 Partnership Request\n\n✧ Send your server advertisement below\n\n✧ Requirements\n• 50+ members\n• Fully SFW community\n• Stox community\n\n✧ A staff member will review your request")

    # ───── BLIST ─────
    @commands.command()
    async def blist(self, ctx):
        await self.send_embed(ctx, "📋 Blacklist Submission\n\n✧ Include:\n• User ID\n• Reason\n• Proof\n\n✧ Reports without proof may be denied")

    # ───── HELP ─────
    @commands.command()
    async def help(self, ctx):
        await self.send_embed(ctx, "🆘 Help & Support\n\n✧ Questions, issues, support\n\n✧ Please explain your issue clearly ♡")

    # ───── APPLY ─────
    @commands.command()
    async def apply(self, ctx):
        await self.send_embed(ctx, "🛡️ Moderator Applications\n\n✧ Level 25+\n✧ 1 week+ in server\n✧ 500+ messages\n\n✧ Be honest and detailed ♡")

    # ───── SAFE EMBED FUNCTION ─────
    async def send_embed(self, ctx, text):
        embed = discord.Embed(
            description="୨୧ ────────────── ୨୧\n\n" + text + "\n\n୨୧ ────────────── ୨୧",
            color=0x001f3f
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SwanoCommands(bot))
