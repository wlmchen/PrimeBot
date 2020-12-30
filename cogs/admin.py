import discord
import subprocess
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send("{} has been loaded".format(extension))

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send("{} has been unloaded".format(extension))

    @commands.command()
    @commands.is_owner()
    async def admintest(self, ctx):
        await ctx.send('You are the owner')

    @commands.command()
    @commands.is_owner()
    async def check_cogs(self, ctx, cog_name):
        try:
            self.bot.load_extension(f"cogs.{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("Cog is loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Cog not found")
        else:
            await ctx.send("Cog is unloaded")
            self.bot.unload_extension(f"cogs.{cog_name}")

    @commands.command()
    @commands.is_owner()
    async def restartBot(self, ctx):
        await ctx.send(":robot: Bot is restarting")
        subprocess.call(["git", "pull --rebase"])
        await ctx.bot.logout()
        await login(TOKEN, bot=True)

def setup(bot):
    bot.add_cog(Admin(bot))

#
