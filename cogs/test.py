import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, arg):
            await ctx.send(arg)

def setup(bot): 
    bot.add_cog(Test(bot) 
)
