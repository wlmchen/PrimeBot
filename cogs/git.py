import subprocess
import discord
from discord.ext import commands
import subprocess

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def githead(self, ctx):
        head = subprocess.run(['git', '--no-pager', 'show', 'HEAD'], stdout=subprocess.PIPE)
        if len(head.stdout.decode('utf-8')) > 2000:
            mystr = head.stdout.decode('utf-8')
            mystr = mystr[0:2030]
        else:
            mystr = head.stdout.decode('utf-8')
        mystr = "```diff\n" + mystr + "```"
        embedHead = discord.Embed(title="Git Head", description=mystr)
        embedHead.add_field(name=".", value = "[Git Repository](https://gitlab.com/pryme-svg/primebot)")
        await ctx.send(embed=embedHead)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gitlog(self, ctx):
        log = subprocess.run(['git', '--no-pager', 'log'], stdout=subprocess.PIPE)
        if len(log.stdout.decode('utf-8')) > 2000:
            mystr = log.stdout.decode('utf-8')
            mystr = mystr[0:2030]
            mystr = "```\n" + mystr + "```"
        else:
            mystr = log.stdout.decode('utf-8')
            mystr = "```\n" + mystr + "```"
        embedLog = discord.Embed(title="Git Log(truncated)", description=mystr)
        embedLog.add_field(name=".", value = "[Git Repository](https://gitlab.com/pryme-svg/primebot)")
        await ctx.send(embed=embedLog)

def setup(bot):
    bot.add_cog(Git(bot))
