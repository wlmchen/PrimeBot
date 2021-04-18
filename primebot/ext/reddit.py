import discord
import requests_cache
import requests
from discord.ext import commands


class Reddit(commands.Cog):
    """Consoom reddit"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx, arg=None):
        """Get a random meme"""
        url = "https://www.reddit.com/r/dankmemes/random/.json"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
        with requests_cache.disabled():
            r = requests.get(url, headers=headers)
        json = r.json()
        embed = discord.Embed(title=json[0]['data']['children'][0]['data']['title'], url=json[0]['data']['permalink'])
        embed.set_image(url=json[0]['data']['children'][0]['data']['url_overridden_by_dest'])
        embed.set_footer(text="🔼 {} 🔽 {}".format(json[0]['data']['children'][0]['data']['score'], json[0]['data']['children'][0]['data']['upvote_ratio']))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
