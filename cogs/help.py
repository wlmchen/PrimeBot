import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedHelp = discord.Embed(title="Help", description="Prefix: >\nCommands:\n`>ping`\n`>quote`\n`>test (text)`\n`>prime`\n`>ban`\n`>kick`\n`>roll`\n`>8ball (question)`\n`>clear (amount)`\n`unban (member)`\n`poll question item1 item2 ...`\n`xkcd`\n`xkcd latest`\n`xkcd n <number`\n\nThis Bot is Open Source! https://gitlab.com/pryme-svg/primebot", color=0x282828)
        embedHelp.set_footer(text="Made by GNU/PrimeTime09#1847, Running on Debian GNU/Linux")
        await ctx.send(embed = embedHelp)

def setup(bot): 
    bot.add_cog(Help(bot) 
)
