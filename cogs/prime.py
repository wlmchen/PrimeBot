import discord
from discord.ext import commands

class Prime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prime(self, ctx):
        await ctx.send("Thanks for using my bot! Feel free to browse my github at https://github.com/pryme-svg")

def setup(bot): 
    bot.add_cog(Prime(bot) 
)
