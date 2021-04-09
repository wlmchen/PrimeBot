import discord
from async_timeout import timeout
import asyncio
import primebot
import requests
import requests_cache
import json
from discord.ext import commands
import random
from pyfiglet import Figlet
import xkcd_wrapper


class Fun(commands.Cog):
    def __init__(self, bot):
        self.xkcd_api_client = xkcd_wrapper.AsyncClient()
        self.bot = bot

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        """
        Ask an 8ball
        """
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def flip(self, ctx):
        """Flip a Coin"""
        randint = random.randint
        value = randint(1, 2)
        if value == 1:
            coinflipembed = discord.Embed(title="Coin Flip", description=":coin: Heads!")
            await ctx.send(embed=coinflipembed)
        if value == 2:
            coinflipembed = discord.Embed(title="Coin Flip", description=":coin: Tails!")
            await ctx.send(embed=coinflipembed)

    def embed_comic(self, xkcd_comic, color=None):
        comic = discord.Embed()
        comic.set_author(name=f'xkcd #{xkcd_comic.id}: {xkcd_comic.title}',
                         url=f'https://xkcd.com/{xkcd_comic.id}',
                         icon_url='https://xkcd.com/s/0b7742.png')
        comic.set_image(url=xkcd_comic.image_url)
        comic.set_footer(text=xkcd_comic.description)
        return comic

    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True)
    async def command_xkcd(self, context):
        """Show a random xkcd comic"""
        random_comic = await self.xkcd_api_client.random(raw_comic_image=False)
        embed_comic = self.embed_comic(random_comic)
        await context.send(embed=embed_comic)

    @command_xkcd.command(name='id', ignore_extra=False, aliases=['n', '-n', 'number'])
    async def command_xkcd_id(self, context, comic_id):
        """
        Shows the selected xkcd comic
        Retrieves the xkcd webcomic with the specified ID from xkcd.com
        ex:
        `<prefix>xkcd id` 100
        `<prefix>xkcd n` 1234
        """
        comic_id = int(comic_id)
        comic = await self.xkcd_api_client.get(comic_id, raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)

    # XKCD LATEST
    @command_xkcd.command(name='latest', ignore_extra=False, aliases=['l', '-l', 'last'])
    async def command_xkcd_latest(self, context):
        """
        Shows the latest xkcd comic

        Retrieves the latest xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd latest`
        `<prefix>xkcd l`
        """
        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)

    @commands.command()
    async def roll(self, ctx):
        """Roll a dice"""
        randint = random.randint
        value = randint(1, 6)
        await ctx.send("{} has rolled a {}!".format(ctx.message.author, value))

    @commands.command(aliases=["ud", "urbandict", "df"])
    async def define(self, ctx, *, arg):
        """Search Urban Dictionary"""
        url = "https://api.urbandictionary.com/v0/define?term=" + arg
        json1 = requests.get(url)
        data = json1.json()
        if not data["list"]:
            await ctx.send("Word not Found!")
            return
        embeds = []
        for word in data['list']:
            definition = word["definition"]
            arg = word["word"]
            title = "Urban Dictionary: " + arg
            url = word["permalink"]
            votes = "👍 " + str(word["thumbs_up"]) + "👎 " + str(word['thumbs_down'])
            definition = definition[0:2048]
            embed = discord.Embed(title=title, description=definition, url=url, color=discord.Color.blurple())
            embed.add_field(name="Example", value=word['example'][:1024], inline=False)
            embed.set_footer(text=votes)
            embeds.append(embed)
        pages = primebot.utils.paginator.EmbedsSource(embeds)
        menu = primebot.utils.paginator.Menu(pages)
        await menu.start(ctx)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)  # cooldown because of rate limiting
    async def quote(self, ctx):
        """Get an inspirational quote"""
        # don't cache this page or every quote will be the same
        with requests_cache.disabled():
            response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        embedQuote = discord.Embed(title="Inspirational Quote", description=quote, color=0x282828)
        await ctx.send(embed=embedQuote)

    @commands.command(aliases=['ascii'])
    async def figlet(self, ctx, *, arg):
        """Get ASCII art"""
        f = Figlet(font='slant')
        text = f.renderText(arg)
        msg = '```fix\n' + text + '\n```'
        if len(msg) >= 2000:
            await ctx.send("Discord API limits message content to 2000 characters, please send a shorter message")
            return
        await ctx.send(msg)

    @commands.command(aliases=['cf'])
    async def catfact(self, ctx):
        """Get a random catfact"""
        url = "https://catfact.ninja/facts"
        with requests_cache.disabled():
            response = requests.get(url)
        data = json.loads(response.text)
        fact = data['data'][0]['fact']
        embed = discord.Embed(title="Cat Fact", description=fact)
        embed.set_footer(text="🐱")
        await ctx.send(embed=embed)

    @commands.command()
    async def name(self, ctx):
        """Get a random name"""
        url = "https://nekos.life/api/v2/name"

        with requests_cache.disabled():
            response = requests.get(url)
        data = json.loads(response.text)
        name = data['name']
        embed = discord.Embed(title="Name", description=name)
        embed.set_footer(text="📛")
        await ctx.send(embed=embed)

    @commands.command()
    async def spoiler(self, ctx, *, text):
        url = "https://nekos.life/api/v2/spoiler?text=" + text
        json1 = requests.get(url)
        data = json1.json()
        try:
            if data['msg']:
                raise commands.CommandError(data['msg'])
        except KeyError:  # should be caught if no arg but why not
            pass
        await ctx.send(data['owo'])

    @commands.group(name='who', invoke_without_command=True)
    @commands.max_concurrency(1, commands.BucketType.channel)  # only one per channel
    async def command_who(self, ctx):
        """Guess who someone is from their avatar"""
        user = random.choice(ctx.guild.members)
        prefix = primebot.db.prefixes.find_one({"guild_id": ctx.message.guild.id})['prefix']
        accepted_strings = ["{}giveup".format(prefix), "{}gu".format(prefix)]
        embed = discord.Embed().set_image(url=user.avatar_url_as(static_format="png", size=128))
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text="Use {}giveup to giveup".format(prefix))
        sent = await ctx.send(embed=embed)
        try:
            async with timeout(10):
                while True:
                    try:
                        message = await self.bot.wait_for(
                            "message",
                            timeout=10.0,
                            check=lambda m: m.author.bot is False,
                        )
                        if (user.name.lower() in message.content.lower() or user.display_name.lower() in message.content.lower()):
                            await ctx.send(f"{message.author.mention} got it!")
                            if primebot.db.who_game.find_one({"user_id": message.author.id, "guild_id": message.guild.id}) is None:
                                e = {"user_id": message.author.id, "name": message.author.name, "guild_id": message.guild.id, "points": 1}
                                primebot.db.who_game.insert_one(e)
                            else:
                                query = {"guild_id": message.guild.id, "user_id": message.author.id}
                                oldpoints = primebot.db.who_game.find_one({"user_id": message.author.id})['points']
                                new = {"$set": {"points": oldpoints + 1}}
                                primebot.db.who_game.update_one(query, new)
                            return
                        if message.content in accepted_strings and message.author == ctx.message.author:
                            embed.add_field(name="Gave Up!", value=user.mention)
                            embed.set_footer(text=user)
                            return await sent.edit(embed=embed)
                    except asyncio.TimeoutError:
                        continue
        except (asyncio.TimeoutError, asyncio.CancelledError):
            return await ctx.send(f"Time's up! It was {user}")

    @command_who.command(name='leaderboard', aliases=['l'])
    async def command_who_leaderboard(self, ctx):
        query = {'guild_id': ctx.guild.id}
        scores = list(primebot.db.who_game.find(query))
        if scores:
            description = ''
            sorts = sorted(scores, key=lambda k: k['points'], reverse=True)
            for count, score in enumerate(sorts, 1):
                user = await self.bot.fetch_user(score['user_id'])
                description = description + "{}. {} - {}\n".format(count, user.mention, score['points'])
            embed = discord.Embed(title="Leaderboard", description=description, color=0x282828)
            await ctx.send(embed=embed)
            return
        await ctx.send("No points found")

    @commands.command(hidden=True)
    async def neofetch(self, ctx):
        e = "```\n" + "                   -`                    pryme-svg@computer\n                  .o+`                   --------------\n                 `ooo/                   OS: Arch Linux x86_64\n                `+oooo:                  Host: HP Pavilion Laptop 15-cs0xxx\n               `+oooooo:                 Kernel: 5.10.24-1-lts\n               -+oooooo+:                Uptime: 1 day, 2 hours, 5 mins\n             `/:-:++oooo+:               Packages: 1142 (pacman)\n            `/++++/+++++++:              Shell: bash 5.1.4\n           `/++++++++++++++:             Resolution: 1920x1080\n          `/+++ooooooooooooo/`           WM: bspwm\n         ./ooosssso++osssssso+`          Theme: Gruvbox [GTK2/3]\n        .oossssso-``/ossssss+`         Icons: Adwaita [GTK2/3]\n       -osssssso.      :ssssssso.        Terminal: st\n      :osssssss/        osssso+++.       Terminal Font: JoyPixels\n     /ossssssss/        +ssssooo/-       CPU: Intel i7-7500U (4) @ 3.500GHz\n   `/ossssso+/:-        -:/+osssso+-     GPU: Intel HD Graphics 620\n  `+sso+:-`                 `.-/+oso:    GPU: NVIDIA GeForce MX150\n `++:.                           `-/+/   Memory: 668iB / 11856MiB\n .`                                 `/\n" + "```"
        await ctx.send(e)


def setup(bot):
    bot.add_cog(Fun(bot))
