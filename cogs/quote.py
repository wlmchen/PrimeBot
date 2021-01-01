import discord
import requests_cache
import requests
import json
from discord.ext import commands


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        s = requests_cache.CachedSession()
        with s.cache_disabled():
            response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        embedQuote = discord.Embed(title="Inspirational Quote", description=quote, color=0x282828)
        await ctx.send(embed=embedQuote)


def setup(bot):
    bot.add_cog(Quote(bot))
