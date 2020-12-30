import discord 
import requests
from bs4 import BeatifulSoup
import random
from discord.ext import commands 

class Distro(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 
 
    @commands.command()
    async def distro(self, ctx, *, arg):
        soup = BeautifulSoup(
    requests.get("https://distrowatch.com/mint").content,
    "html.parser")
        mintdesc = soup.(id="text")
        ubuntudesc = 
        manjarodesc = 
        if 'mint' in arg:
            mintEmbed = discord.Embed(title="Linux Mint", description=mintdesc)
            mintEmbed.set_footer(text="Powered by DistroWatch")
            await ctx.send(embed=mintEmbed)
        if arg.lower == "ubuntu":
            ubuntuEmbed = discord.Embed(title="Ubuntu", description=ubuntudesc)
            ubuntuHead.set_footer(text="Powered by DistroWatch")
            await ctx.send(embed=ubuntuEmbed)
        if 'manjaro' in arg:
            manjaroEmbed = discord.Embed(title="Manjaro", description=manjarodesc)
            manjaroHead.set_footer(text="Powered by DistroWatch")
            await ctx.send(embed=manjaroEmbed)

def setup(bot):
    bot.add_cog(Distro(bot))
