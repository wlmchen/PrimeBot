import discord
import json
import primebot
import datetime
import requests
from discord.ext import commands
from primebot.utils.checks import is_pt


class Torrent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=['1337'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _1337(self, ctx, *, query):
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

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def nyaa(self, ctx, *, query):
        async with ctx.channel.typing():
            url = 'https://torrent-api1.herokuapp.com/getTorrents?site=nyaa&query={}'.format(query)
            r = requests.get(url)
            json = r.json()
            embed = discord.Embed(color=0x0083FF)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            if not json['torrents']:
                embed = discord.Embed(description=":x: Query not found", color=0xD63600)
                await ctx.send(embed=embed)
                return
            for torrent in json['torrents']:
                desc = "**[magnet]({})** | **[nyaa]({})** | Seeds: {} | Leeches: {} | Size: {}".format(torrent['shortlink'], torrent['link'], torrent['seeds'], torrent['leeches'], torrent['size'])
                embed.add_field(name=torrent['name'], value=desc, inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command(aliases=['rargb'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rarbg(self, ctx, *, query):
        async with ctx.channel.typing():
            url = 'https://torrent-api1.herokuapp.com/getTorrents?site=Rarbg&query={}'.format(query)
            r = requests.get(url)
            json = r.json()
            embed = discord.Embed(color=0x0083FF)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            if not json['torrents']:
                embed = discord.Embed(description=":x: Query not found", color=0xD63600)
                await ctx.send(embed=embed)
                return
            for torrent in json['torrents']:
                if torrent['shortlink'] == "":
                    desc = "**[magnet]({})** | **[rarbg]({})** | Seeds: {} | Leeches: {} | Size: {}".format("magnet not found", torrent['link'], torrent['seeds'], torrent['leeches'], torrent['size'])
                desc = "**[magnet]({})** | **[rarbg]({})** | Seeds: {} | Leeches: {} | Size: {}".format(torrent['shortlink'], torrent['link'], torrent['seeds'], torrent['leeches'], torrent['size'])
                embed.add_field(name=torrent['name'], value=desc, inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command()
    @is_pt()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def sows(self, ctx, *, query):
        raw = primebot.sows.search_torrents(query)
        js = json.loads(raw)
        torrents = []
        index = 0
        for result in js['results']:
            torrents.append({'name': result['groupName'], 'id': result['groupId'], 'size': primebot.utils.convert_size(result['maxSize']), 'seeders': result['totalSeeders'], 'leechers': result['totalLeechers'], 'year': result['groupYear'], 'artist': result['artist']})
            torrents[index]['link'] = "https://bemaniso.ws/torrents.php?id={}".format(str(torrents[index]['id']))
            index += 1
            if index >= 3:
                break
        embed = discord.Embed(color=0x8B008B)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        for torrent in torrents:
            desc = "**[Bemaniso]({})** | Seeds: {} | Leeches: {} | Size: {} | Artist: {} | Year: {}".format(torrent['link'], torrent['seeders'], torrent['leechers'], torrent['size'], torrent['artist'], torrent['year'])
            embed.add_field(name=torrent['name'], value=desc, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @is_pt()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ops(self, ctx, *, query):
        raw = primebot.ops.search_torrents(query)
        js = json.loads(raw)
        torrents = []
        index = 0
        for result in js['results']:
            torrents.append({'name': result['groupName'], 'id': result['groupId'], 'size': primebot.utils.convert_size(result['maxSize']), 'seeders': result['totalSeeders'], 'leechers': result['totalLeechers'], 'artist': result['artist'], 'year': result['groupYear']})
            torrents[index]['link'] = "https://orpheus.network/torrents.php?id={}".format(str(torrents[index]['id']))
            index += 1
            if index >= 3:
                break
        embed = discord.Embed(color=0x0000FF)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        for torrent in torrents:
            desc = "**[Orpheus]({})** | Seeds: {} | Leeches: {} | Size: {} | Artist: {} | Year: {}".format(torrent['link'], torrent['seeders'], torrent['leechers'], torrent['size'], torrent['artist'], torrent['year'])
            embed.add_field(name=torrent['name'], value=desc, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Torrent(bot))
