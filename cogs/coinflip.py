import discord
from discord.ext import commands
import random

randint = random.randint

class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
       value = randint(1,2)
       if value == 1:
           embedVar = discord.Embed(title="Coin Flip", description=":coin: Heads!".format)
           await ctx.send(embed=coinflipembed)
       if value == 2:
           embedVar = discord.Embed(title="Coin Flip", description=":coin: Tails!".format)
           await ctx.send(embed=coinflipembed)


def setup(bot):
    bot.add_cog(Flip(bot))
