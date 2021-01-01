import discord
import random
from discord.ext import commands


class MyQuote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def myquote(self, ctx):
        quotes = [
                "I'm tired of trying to do something worthwhile for the human race, they simply don't want to change! - August Dvorak",
                "More than 95% of people could be using a computer from 2008 or before without any problems. - Luke Smith",
                "A computer is like air conditioning – it becomes useless when you open Windows. - Linus Torvalds"]
        quote = random.choice(quotes)
        embedQuote = discord.Embed(title="Quotes curated by PrimeTime", description=quote, color=0x282828)
        await ctx.send(embed=embedQuote)


def setup(bot):
    bot.add_cog(MyQuote(bot))
