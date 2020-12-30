import discord 
from bs4 import BeautifulSoup
import requests
import lxml.html
from urllib.parse import urljoin
from discord.ext import commands 

class Distro(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 
 
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def distro(self, ctx, arg):
        url = urljoin("http://www.distrowatch.com/", arg)
        html_string = requests.get(url).content

        html_string = html_string.decode('utf-8')

        for line in html_string.splitlines():
            if len(line) > 100 and not '<' in line and 'is a' in line:
                description = line
                break

        soup = BeautifulSoup(html_string)
        title = soup.title.string
        embed = discord.Embed(title=title, description = description)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Distro(bot))

