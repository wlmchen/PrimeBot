import discord
import datetime
import requests
from discord.ext import commands


class Torrent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def torrent(self, ctx, query):
        async with ctx.channel.typing():
            url = 'https://torrent-api1.herokuapp.com/getTorrents?site=1337x&query={}'.format(query)
            r = requests.get(url)
            json = r.json()
            embed = discord.Embed(color=0xD63600)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            if not json['torrents']:
                embed = discord.Embed(description=":x: Query not found", color=0xFF0000)
                await ctx.send(embed=embed)
                return
            for torrent in json['torrents']:
                desc = "**[magnet]({})** | **[1337]({})** | Seeds: {} | Leeches: {} | Size: {}".format(torrent['shortlink'], torrent['link'], torrent['seeds'], torrent['leeches'], torrent['size'])
                embed.add_field(name=torrent['name'], value=desc, inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Torrent(bot))
