import discord
import subprocess
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from discord.ext import commands
import primebot
import git
import asyncio


class Dev(commands.Cog):
    """Dev commands"""
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    @commands.command(hidden=True)
    async def login(self, ctx, service):
        """Relogin to Services after Timeout"""
        if service == 'sows':
            primebot.sows._login()
            await ctx.send("Logged in")
        if service == "ops":
            primebot.ops._login()
            await ctx.send("Logged in")

    @commands.command(hidden=True)
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
    async def admintest(self, ctx):
        """Test if you are the owner"""
        await ctx.send('You are the owner of this bot')

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e: # noqa
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(hidden=True, aliases=['shell'])
    async def sh(self, ctx, *, command):
        """Runs a shell command."""
        async with ctx.typing():
            stdout, stderr = await self.run_process(command)

        if stderr:
            text = f'stdout:\n{stdout}\nstderr:\n{stderr}'
        else:
            text = stdout

        await ctx.send(f"```\n{text}```")

    @commands.command(hidden=True)
    async def dm(self, ctx, member, *, message: str):
        """DM a user"""
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
    async def check_cogs(self, ctx, cog_name):
        """Check if a cog is loaded"""
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
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        """Change the precense of the bot"""
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
    async def changestatus(self, ctx, status: str):
        """Change the status of the bot"""
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
    async def leaveserver(self, ctx, guildid):
        """Leave a server"""
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
    async def echo(self, ctx, *, a):
        """Echo something into the channel"""
        await ctx.send(a)
        await ctx.message.delete()

    @commands.command(hidden=True)
    async def reply(self, ctx, *, a=None):
        """Reply to a message"""
        if a is None:
            await ctx.reply('replied')
        else:
            await ctx.send(a)

    @commands.command(hidden=True)
    async def nickname(self, ctx, *name):
        """Set the nickname of the bot"""
        nickname = ' '.join(name)
        me = ctx.me
        await me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Nickname changed to: **{nickname}**'
        else:
            msg = ':ok: Reset nickname'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def pull(self, ctx):
        """Pull from upstream git repo"""
        g = git.cmd.Git('.')
        msg = g.pull()
        await ctx.send('```\n' + msg + '\n```')

    @commands.command(hidden=True, aliases=['reboot'])
    async def restart(self, ctx):
        """Restart the bot"""
        await ctx.send(":robot: Bot is restarting")
        await self.bot.closeman()
        await self.bot.login(primebot.conf['token'], bot=True)

    @commands.command(hidden=True)
    async def serverlist(self, ctx):
        """Get a list of servers"""
        list = []
        for guild in self.bot.guilds:
            list.append(guild.name + ':' + str(len(guild.members)))
        await ctx.send(list)

    @commands.command(hidden=True)
    async def botservers(self, ctx):
        """Get the number of servers the bot is in"""
        await ctx.send("I'm in " + str(len(self.bot.guilds)) + " servers")


def setup(bot):
    bot.add_cog(Dev(bot))
