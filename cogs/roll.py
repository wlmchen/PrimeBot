import discord
from discord.ext import commands
import random

randint = random.randint

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
       value = randint(1,6)
       await ctx.send("{} has rolled a {}!".format(ctx.message.author, value))

def setup(bot):
    bot.add_cog(Roll(bot))
