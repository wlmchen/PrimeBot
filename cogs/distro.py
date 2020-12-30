import discord 
import random
from discord.ext import commands 

class Distro(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 
 
    @commands.command()
    async def distro(self, ctx, *, arg):
        mintdesc = "Linux Mint is an Ubuntu-based distribution whose goal is to provide a classic desktop experience with many convenient, custom tools and optional out-of-the-box multimedia support. It also adds a custom desktop and menus, several unique configuration tools, and a web-based package installation interface. Linux Mint is compatible with Ubuntu software repositories."
        ubuntudesc = "Ubuntu is a complete desktop Linux operating system, freely available with both community and professional support. The Ubuntu community is built on the ideas enshrined in the Ubuntu Manifesto: that software should be available free of charge, that software tools should be usable by people in their local language and despite any disabilities, and that people should have the freedom to customise and alter their software in whatever way they see fit. Ubuntu is an ancient African word, meaning humanity to others. The Ubuntu distribution brings the spirit of Ubuntu to the software world. "
        manjarodesc = " Manjaro Linux is a fast, user-friendly, desktop-oriented operating system based on Arch Linux. Key features include intuitive installation process, automatic hardware detection, stable rolling-release model, ability to install multiple kernels, special Bash scripts for managing graphics drivers and extensive desktop configurability. Manjaro Linux offers Xfce as the core desktop options, as well as KDE, GNOME and a minimalist Net edition for more advanced users. Community-supported desktop flavours are also available."
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
