import json
import discord
from discord.ext import commands
import urllib
import requests
import os
from dotenv import load_dotenv

class Apod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def apod(self, ctx, date = None):
        load_dotenv()
        API_KEY = os.getenv('API_KEY')

        if date == None:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY
        else:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY + "&date=" + date

        r = requests.get(url)

        json_file = r.json()
        if 'code' in json_file:
            await ctx.send(json_file['msg'])
            return

        embedApod = discord.Embed(title=json_file['title'] , description = json_file['explanation'])
        embedApod.set_footer(text=json_file['date'])
        embedApod.set_image(url=json_file['url'])
        await ctx.send(embed=embedApod)


def setup(bot):
    bot.add_cog(Apod(bot))
