import random
import discord
from discord.ext import commands


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(20, 30, commands.BucketType.user)
    @commands.command()
    async def test(self, ctx, *, word):
        if "@" in ctx.message.content:
            await ctx.send("You may not tag everyone in this command {}".format(ctx.message.author.mention))
            return
        await ctx.send(word)


def setup(bot):
    bot.add_cog(test(bot))
