import discord
from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        pingEmbed = discord.Embed(title="Ping!", description='🏓 Pong! {0}s'.format(self.bot.latency, 1))
        await ctx.send(embed = pingEmbed)

def setup(bot):
    bot.add_cog(Ping(bot))
