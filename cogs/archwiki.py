import discord
import requests
from discord.ext import commands
from googlesearch import search 
from bs4 import BeautifulSoup


class Archwiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aw'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def archwiki(self, ctx, *, query):
        query1 = query + "site:https://wiki.archlinux.org"
        
        for j in search(query1): 
            url = j
            break

        html_string = requests.get(url).content
        html_string = html_string.decode('utf-8')
        test1 = html_string[html_string.index("</ul></div>"):html_string.index("Contents")]
        soup = BeautifulSoup(test1, "html.parser")
        description = "".join(soup.strings)


        embedAw= discord.Embed(title="Arch Wiki: " + query, description=description, color=0x1793d1)
        embedAw.set_footer(text=url)
        await ctx.send(embed=embedAw)


def setup(bot):
    bot.add_cog(Archwiki(bot))
