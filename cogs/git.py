import subprocess
import discord
from discord.ext import commands
import subprocess

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def githead(self, ctx):
        head = subprocess.run(['git', '--no-pager', 'show', 'HEAD'], stdout-subprocess.PIPE)
        await ctx.send(head)

    @commands.command()
    async def gitlog(self, ctx):
        log = subprocess.run(['git', '--no-pager', 'log'], stdout-subprocess.PIPE)
        await ctx.send(log)
