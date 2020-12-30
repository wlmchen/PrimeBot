import discord
from discord.ext import commands

class Prime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prime(self, ctx):
        embed=discord.Embed(title="Prime", description="Thanks for using my bot! Feel free to browse my [github](https://github.com/pryme-svg)\nOr check out my [gitlab](https://gitlab.com/pryme-svg)\nThis bot is open source, please star the [repository](https://gitlab.com/pryme-svg/primebot/)!")
        await ctx.send(embed=embed)

def setup(bot): 
    bot.add_cog(Prime(bot) 
)
