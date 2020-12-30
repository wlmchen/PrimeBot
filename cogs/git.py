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
        if len(head.stdout.decode('utf-8')) > 6000:
            mystr = head.stdout.decode('utf-8')
            mystr = mystr[0:5000]
        else:
            mystr = head.stdout.decode('utf-8')
        mystr = "```diff\n" + mystr + "```"
        embedLog = discord.Embed(title="Git Head", description=mystr)
        await ctx.send(embed=embedLog)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gitlog(self, ctx):
        log = subprocess.run(['git', '--no-pager', 'log'], stdout=subprocess.PIPE)
        if len(log.stdout.decode('utf-8')) > 6000:
            mystr = log.stdout.decode('utf-8')
            mystr = mystr[0:2048]
        else:
            mystr = log.stdout.decode('utf-8')
            mystr = "```\n" + mystr + "```"
        embedLog = discord.Embed(title="Git Log(truncated)", description=mystr)
        await ctx.send(embed=embedLog)

def setup(bot):
    bot.add_cog(Git(bot))
