import discord
from primebot.utils.checks import is_owner
from discord.ext import commands
import primebot
import git


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @is_owner()
    async def admintest(self, ctx):
        await ctx.send('You are the owner of this bot')

    @commands.command(hidden=True)
    @is_owner()
    async def dm(self, ctx, member, *, message: str):
        converter = discord.ext.commands.MemberConverter()
        user = await converter.convert(ctx, member)
        if not user:
            return await ctx.send("Could not find any Umatching UserID ")

        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{member}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")

    @commands.command(hidden=True)
    @is_owner()
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
    @is_owner()
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
    @is_owner()
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

    @commands.command(hidden=True)
    @is_owner()
    async def leaveserver(self, ctx, guildid):
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guildid = int(guildid)
            guild = self.bot.get_guild(guildid)
            if guild is None:
                raise commands.CommandError("I can't find that guild")
            await guild.leave()
        await ctx.send(':ok: I have left {} ({})'.format(guild.name, guild.id))

    @commands.command(pass_context=True, hidden=True)
    @is_owner()
    async def echo(self, ctx, *, a):
        await ctx.send(a)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @is_owner()
    async def reply(self, ctx, *, a=None):
        if a is None:
            await ctx.reply('replied')
        else:
            await ctx.send(a)

    @commands.command(hidden=True)
    @is_owner()
    async def nickname(self, ctx, *name):
        nickname = ' '.join(name)
        me = ctx.me
        await me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Nickname changed to: **{nickname}**'
        else:
            msg = ':ok: Reset nickname'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @is_owner()
    async def pull(self, ctx):
        g = git.cmd.Git('.')
        msg = g.pull()
        await ctx.send('```\n' + msg + '\n```')

    @commands.command(hidden=True, aliases=['reboot'])
    @is_owner()
    async def restart(self, ctx):
        await ctx.send(":robot: Bot is restarting")
        await self.bot.closeman()
        await self.bot.login(primebot.conf['token'], bot=True)

    @commands.command(hidden=True)
    @is_owner()
    async def serverlist(self, ctx):
        list = []
        for guild in self.bot.guilds:
            list.append(guild.name + ':' + str(len(guild.members)))
        await ctx.send(list)

    @commands.command(hidden=True)
    async def botservers(self, ctx):
        await ctx.send("I'm in " + str(len(self.bot.guilds)) + " servers")


def setup(bot):
    bot.add_cog(Dev(bot))
