import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(20, 30, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['clean'])
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Clear(bot))
