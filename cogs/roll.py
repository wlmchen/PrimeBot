import discord
import math
from discord.ext import commands
import random

randint = random.randint
mathpi = math.pi


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        value = randint(1, 7)
        if value == 7:
            await ctx.send("{} has rolled a pi! :pie: {} ".format(ctx.message.author, mathpi))
            return
        await ctx.send("{} has rolled a {}!".format(ctx.message.author, value))

def setup(bot):
    bot.add_cog(Roll(bot))
