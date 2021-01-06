import discord
import requests_cache
import requests
import json
from discord.ext import commands

import requests
import random

import math
import random
import random
import discord
import xkcd_wrapper
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.xkcd_api_client = xkcd_wrapper.AsyncClient()
        self.bot = bot

        mathpi = math.pi
        randint = random.randint

    @commands.cooldown(20, 30, commands.BucketType.user)
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        if "@" in ctx.message.content:
            await ctx.send("You may not tag everyone in this command {}".format(ctx.message.author.mention))
            return
        responses = [ "It is certain.",
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

    ##########
    # COMMANDS
    #########

    # XKCD
    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True)
    async def command_xkcd(self, context):
        """
        Shows a random xkcd comic

        Retrieves a random xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd`
        """
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
        """
        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)



    @commands.command()
    async def roll(self, ctx):
        value = randint(1, 7)
        if value == 7:
            await ctx.send("{} has rolled a pi! :pie: {} ".format(ctx.message.author, mathpi))
            return
        await ctx.send("{} has rolled a {}!".format(ctx.message.author, value))

    @commands.command(alises=["ud", "urbandict"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, *, arg):

        url = "https://api.urbandictionary.com/v0/define?term=" + arg
        json1 = requests.get(url)
        data = json1.json()
        if not data["list"]:
            await ctx.send("Word not Found!")
            return
        definition = data["list"][0]["definition"]
        title = "Urban Dictionary: " + arg
        if len(definition) > 2000:
            definition = definition[0:2000]
            title = title + " (Truncated)"
        embed = discord.Embed(title=title, description=definition)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def quote(self, ctx):
        s = requests_cache.CachedSession()
        with s.cache_disabled():
            response = s.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        embedQuote = discord.Embed(title="Inspirational Quote", description=quote, color=0x282828)
        await ctx.send(embed=embedQuote)

    @commands.command()
    async def myquote(self, ctx):
        quotes = [
                "I'm tired of trying to do something worthwhile for the human race, they simply don't want to change! - August Dvorak",
                "More than 95% of people could be using a computer from 2008 or before without any problems. - Luke Smith",
                "A computer is like air conditioning – it becomes useless when you open Windows. - Linus Torvalds"]
        quote = random.choice(quotes)
        embedQuote = discord.Embed(title="Quotes curated by PrimeTime", description=quote, color=0x282828)
        await ctx.send(embed=embedQuote)

def setup(bot):
    bot.add_cog(Fun(bot))

