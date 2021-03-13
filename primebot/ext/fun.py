import discord
from primebot.utils.scrapers import scrape_song_lyrics
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

    @commands.command(aliases=['8ball'])
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
        comic_id = int(comic_id)

        """
        Shows the selected xkcd comic
        Retrieves the xkcd webcomic with the specified ID from xkcd.com
        ex:
        `<prefix>xkcd id` 100
        `<prefix>xkcd n` 1234
        """
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

        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)
        """
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

        definition = data["list"][0]["definition"]
        arg = data["list"][0]["word"]
        title = "Urban Dictionary: " + arg
        url = data["list"][0]["permalink"]
        votes = "👍" + str(data["list"][0]["thumbs_up"]) + "👎" + str(data['list'][0]['thumbs_down'])
        if len(definition) > 2000:
            definition = definition[0:2000]
            title = title + " (Truncated)"
        embed = discord.Embed(title=title, description=definition, url=url)
        embed.set_footer(text=votes)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def lyrics(self, ctx, *query):
        """Get song lyrics"""
        raw = requests.get("https://api.genius.com/search?q={}&access_token={}".format(query, primebot.conf['genius_api_key']))
        raw = raw.json()
        titles = []
        i = 0
        j = 1
        s = ""
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
        if not raw['response']['hits']:
            raise commands.CommandError("Song not Found")
        try:
            if raw['error'] == "invalid_token":
                raise commands.CommandError("Invalid Genius API Key")
        except KeyError:
            pass
        while i < 9:
            titles.append(raw['response']['hits'][i]['result']['full_title'])
            i += 1
        for title in titles:
            s += str(j) + " " + title + "\n"
            j += 1
        react_message = await ctx.send(s)
        for reaction in reactions[:len(titles)]:
            await react_message.add_reaction(reaction)

        # iterate over reactions
        try:
            def check(rctn, user):
                return user.id == ctx.author.id and str(rctn) in reactions

            rctn, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)

            cache_msg = discord.utils.get(self.bot.cached_messages, id=react_message.id)
            for reaction in cache_msg.reactions:
                users = await reaction.users().flatten()
                for user in users:
                    if user == ctx.message.author:
                        selected_music = str(reaction)
        except asyncio.TimeoutError:
            pass

        # replace emoji with int
        reaction = str(selected_music)
        reaction = reaction.replace('1⃣', '1')
        reaction = reaction.replace('2⃣', '2')
        reaction = reaction.replace('3⃣', '3')
        reaction = reaction.replace('4⃣', '4')
        reaction = reaction.replace('5⃣', '5')
        reaction = reaction.replace('6⃣', '6')
        reaction = reaction.replace('7⃣', '7')
        reaction = reaction.replace('8⃣', '8')
        reaction = reaction.replace('9⃣', '9')

        lyric_url = raw['response']['hits'][int(str(reaction))]['result']['url']
        song_title = raw['response']['hits'][int(str(reaction))]['result']['full_title']

        lyrics = scrape_song_lyrics(lyric_url)
        emb = discord.Embed(title=f"{song_title}", description=f"{lyrics}", color=0xa3a3ff, url=lyric_url)
        await ctx.send(embed=emb)

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


def setup(bot):
    bot.add_cog(Fun(bot))
