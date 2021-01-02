import discord
from bs4 import BeautifulSoup
import requests
import random
import requests_cache
from discord.ext import commands


class Distro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    requests_cache.install_cache('distro_cache')

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def distro(self, ctx, arg):
        if arg == "random":
            arg = (random.choice(list(open('linux.list'))))

        url = "http://www.distrowatch.com/table.php?distribution=" + arg
        html_string = requests.get(url).content
        pattern = "<b><a href=\"dwres.php?resource=popularity\">"


        html_string = html_string.decode('utf-8')

#        for line in html_string.splitlines():
#            if len(line) > 100 and '<' not in line and 'is a' in line:
#                description = line
#                break

        for (num, line) in enumerate(html_string.splitlines()):
            if pattern in line:
                linenum = num

        description = html_string.splitlines()[linenum-2]

        try:
            description
        except NameError:
            description = ":x: That distro doesn't exist!"

        soup = BeautifulSoup(html_string)
        title = soup.title.string
        embed = discord.Embed(title=title, description=description)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Distro(bot))
