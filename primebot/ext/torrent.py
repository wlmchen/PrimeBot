import discord
import asyncio
import json
import primebot
import datetime
from discord.ext import commands
from primebot.utils.checks import is_pt

def convertBytes(num):
    step_unit = 1000.0
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


class Torrent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def shorten_all(self,urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.shorten(url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


    async def shorten(self, magnet):
        url = "http://mgnet.me/api/create?&format=json&opt=&m={}".format(magnet)
        e = await self.bot.session.get(url)
        e = json.loads(await e.text())
        return e['shorturl']


    async def search_rarbg(self, query):
        torrents = []
        magnets = []
        i = 0
        url = f"https://torrentapi.org/pubapi_v2.php?mode=search&search_string={query}&token={self.bot.rarbg_token}&app_id=torrent-api&format=json_extended&sort=seeders"
        source = await self.bot.cached_session.get(url)
        source = await source.text()
        source = json.loads(source)
        try:
            for torrent in source['torrent_results']:
                torrents.append({
                    "name": torrent['title'],
                    "seeds": torrent['seeders'],
                    "leeches": torrent['leechers'],
                    "size": convertBytes(torrent['size']),
                    "magnet": torrent['download'],
                    "category": torrent['category']
                    })
                magnets.append(torrent['download'])
        except:
            return []

        shortlinks = await self.shorten_all(magnets)

        for torrent, magnet in zip(torrents, shortlinks):
            torrent['shortlink'] = magnet

        return torrents


    @commands.command(hidden=True, aliases=['1337'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _1337(self, ctx, *, query):
        async with ctx.channel.typing():
            url = 'https://torrent-api1.herokuapp.com/getTorrents?site=1337x&query={}'.format(query)
            r = await self.bot.cached_session.get(url)
            json = await r.json()
            embed = discord.Embed(color=0xD63600)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url="https://1337x.to/images/logo.svg")
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
            r = await self.bot.cached_session.get(url)
            json = await r.json()
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
    @commands.cooldown(1, 2, commands.BucketType.default)
    async def rarbg(self, ctx, *, query):
        async with ctx.channel.typing():
            i=0
            json = await self.search_rarbg(query)
            embed = discord.Embed(color=0x0083FF)
            embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url="https://dyncdn2.com/static/20/img/logo_dark_nodomain2_optimized.png")
            print(json)
            if not json:
                embed = discord.Embed(description=":x: Query not found", color=0xD63600)
                await ctx.send(embed=embed)
                return
            for torrent in json:
                desc = "**[magnet]({})** | Seeds: {} | Leeches: {} | Size: {}".format(torrent['shortlink'], torrent['seeds'], torrent['leeches'], torrent['size'])
                embed.add_field(name=torrent['name'], value=desc, inline=False)
                i+=1
                if i >= 3:
                    break
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
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
