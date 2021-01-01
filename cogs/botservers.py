import discord
from discord.ext import commands


class Botservers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(20, 30, commands.BucketType.user)
    @commands.command()
    async def botservers(self, ctx):
        await ctx.send("I'm in " + str(len(self.bot.guilds)) + " servers")


def setup(bot):
    bot.add_cog(Botservers(bot))
