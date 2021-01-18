import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        embedHelp = discord.Embed(title="Help", description="Default Prefix: >\nCommands:\n`>ping`\n`>quote`\n`>prime`\n`>ban`\n`>kick`\n`>roll`\n`>8ball (question)`\n`>clear (amount)`\n`>unban (member)`\n`>poll question item1 item2 ...`\n`>xkcd`\n`>xkcd latest`\n`>xkcd n <number>`\n`>sys`\n`>info`\n`>flip`\n`>distro (distro)`\n`>distro random`\n`>apod`\n`>apod (date)`\n`>archwiki (search)`\n`>define (term)`\n`>figlet (text)`\n`>invite`\n`>b64encode`\n`>b64decode`\n\nThis Bot is Open Source! Check out the repo [here](https://gitlab.com/pryme-svg/primebot)", color=0x282828)
        embedHelp.set_footer(text="Created by PrimeTime09#1847, Running on Heroku")
        await ctx.send(embed=embedHelp)


def setup(bot):
    bot.add_cog(Help(bot))
