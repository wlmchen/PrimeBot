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
        await ctx.send('You are the owner of this bot')

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


    @commands.command(hidden=True, aliases=['game'])
    @commands.is_owner()
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        gameType = gameType.lower()
        if gameType == 'playing':
            await self.bot.change_presence(activity=discord.Game(name=gameName))
        elif gameType == 'watching':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=gameName))
        elif gameType == 'listening':
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=gameName))
        elif gameType == 'streaming':
            await self.bot.change_presence(activity=discord.Streaming(name=gameName, url="https://www.twitch.tv/primebot5"))
        else:
            await ctx.send("The only game types are available: playing, streaming, watching, listening, streaming.")
            return
        await ctx.send(f'**:ok:** Changed the game to: {gameType} **{gameName}**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def changestatus(self, ctx, status: str):
        status = status.lower()
        if status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'online' or status == 'on':
            discordStatus = discord.Status.online
        else:
            await ctx.send("The only statuses available are online and idle.")
            return
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**:ok:** Changed the status to: **{discordStatus}**')

    @commands.command()
    @commands.is_owner()
    async def leaveserver(self, ctx, guildid):
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid).leave()
            msg = f':ok: I have left {guild.name}!'

        await ctx.send(msg)


    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, a):
        await ctx.send(a)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nickname(self, ctx, *name):
        nickname = ' '.join(name)
        me = ctx.me
        await me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Nickname changed to: **{nickname}**'
        else:
            msg = f':ok: Reset nickname'
        await ctx.send(msg)

    @commands.command()
    @commands.is_owner()
    async def restartBot(self, ctx):
        await ctx.send(":robot: Bot is restarting")
        await ctx.send("Performing `git pull`")
        subprocess.call(["git", "pull", "--rebase"])
        await ctx.bot.logout()
        await bot.login(TOKEN, bot=True)

    @commands.command()
    @commands.is_owner()
    async def serverlist(self, ctx):
        for guild in self.bot.guilds:
            await ctx.send(guild.name)

    @commands.cooldown(20, 30, commands.BucketType.user)
    @commands.command()
    async def botservers(self, ctx):
        await ctx.send("I'm in " + str(len(self.bot.guilds)) + " servers")


def setup(bot):
    bot.add_cog(Admin(bot))
