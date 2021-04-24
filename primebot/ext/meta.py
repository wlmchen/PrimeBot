import discord
from difflib import get_close_matches
import asyncio
import primebot
import itertools
import pygit2
from discord.ext import commands
import datetime
import platform
from cpuinfo import get_cpu_info
import time
import psutil


class EmbeddedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={"help": "Shows help for the bot, a category, or a command."}
        )
        self.subcommand_not_found = self.command_not_found

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"{command.name}|{aliases}"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{self.clean_prefix}{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or "\u200bUncategorised"

        bot = self.context.bot
        embed = discord.Embed(title=f"{bot.user.name} Help", color=discord.Color.blurple())
        description = (
            f"Use `{self.clean_prefix}help <command/category>` for more help\n\n"
        )
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        for cog, cmds in itertools.groupby(entries, key=key):
            cmds = sorted(cmds, key=lambda c: c.name)
            description += f'**{cog}**\n{" • ".join([c.name for c in cmds])}\n'
        embed.description = description
        await self.context.send(embed=embed)

    @staticmethod
    def cog_group_common_fmt(embed, description, entries):
        description += "\n".join(
            [
                f'{"⇶" if isinstance(c, commands.Group) else "-"} **{c.name}** -'
                f' {c.short_doc or "No description"}'
                for c in entries
            ]
        )
        embed.set_footer(text="⇶ indicates subcommands")
        embed.description = description

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"{cog.qualified_name} Category", color=discord.Color.blurple())
        description = f'{cog.description or ""}\n\n'
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        self.cog_group_common_fmt(embed, description, entries)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group), color=discord.Color.blurple())
        description = f'{group.help or "No description provided"}\n\n'
        entries = await self.filter_commands(group.commands, sort=True)
        self.cog_group_common_fmt(embed, description, entries)
        footer = embed.footer.text
        embed.set_footer(text=footer)
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blurple())
        description = f'{command.help or "No description provided"}\n\n'
        embed.description = description
        await self.context.send(embed=embed)

    def command_not_found(self, *args):
        invalid_input_string = " ".join(map(str, args))
        offered_commands = (
            cmd.qualified_name for cmd in self.context.bot.walk_commands()
        )
        return (
            get_close_matches(invalid_input_string, offered_commands)
            or invalid_input_string
        )

    async def send_error_message(self, error):
        if isinstance(error, list):
            suggestions = "\n- ".join(error)
            embed = discord.Embed(title="Did you mean...", color=discord.Color.blurple())
            embed.description = f"- {suggestions}"
            return await self.context.send(embed=embed)
        elif isinstance(error, str):
            return await self.context.send(
                f"No command named '{error}', and no similarly named commands found"
            )
        else:
            await super().send_error_message(error)


class Meta(commands.Cog):
    """
    Commands that show information about the bot
    """

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = EmbeddedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.start_time = datetime.datetime.fromtimestamp(time.time())
        self.system_embed = self.create_system_embed()

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

#     @commands.command()
#     async def help(self, ctx):
#
#         embedHelp = discord.Embed(title="Help", description="Default Prefix: >\nCommands:\n`>ping`\n`>quote`\n`>prime`\n`>ban`\n`>kick`\n`>roll`\n`>8ball (question)`\n`>clear (amount)`\n`>unban (member)`\n`>poll question item1 item2 ...`\n`>xkcd`\n`>xkcd latest`\n`>xkcd n <number>`\n`>sys`\n`>info`\n`>flip`\n`>distro (distro)`\n`>distro random`\n`>apod`\n`>apod (date)`\n`>archwiki (search)`\n`>define (term)`\n`>figlet (text)`\n`>invite`\n`>b64encode`\n`>b64decode`\n`>b32encode`\n`>b32decode`\n`>b16encode`\n`>b16decode`\n`>b85encode`\n`>b85decode`\n\nGet a complete list of commands [here](https://gitlab.com/pryme-svg/primebot#commands)\n\nThis Bot is Open Source! Check out the repo [here](https://gitlab.com/pryme-svg/primebot)", color=0x282828)
#         embedHelp.set_footer(text="Created by PrimeTime09#1847")
#         await ctx.send(embed=embedHelp)

    @staticmethod
    def os_name():
        os = platform.system()
        version = platform.version()
        architecture = platform.architecture()
        architecture = architecture[0] if architecture else ''
        return f'{os} {version} {architecture}'

    @staticmethod
    def cpu_info():
        cores = psutil.cpu_count()
        cores = f'{cores} cores' if cores > 1 else f'{cores} core'
        model = get_cpu_info()['brand_raw']
        return model + cores + ' ({:.2f}GHz)'.format(psutil.cpu_freq().current / 1000)

    @staticmethod
    def ram():
        return psutil._common.bytes2human(psutil.virtual_memory().total)

    @staticmethod
    def python_version():
        return platform.python_version()

    @staticmethod
    def discord_version():
        return discord.__version__

    def get_last_commits(self, count=3):
        repo = pygit2.Repository('.git')
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
        return '\n'.join(self.format_commit(c) for c in commits)

    def format_commit(self, commit):
        short, _, _ = commit.message.partition('\n')
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        return f'[`{short_sha2}`](https://github.com/pryme-svg/PrimeBot/commit/{commit.hex}) {short} ({commit_time})'

    async def uptime(self):
        now = datetime.datetime.fromtimestamp(time.time())
        up_time = now - self.start_time
        return str(up_time).rsplit('.', maxsplit=1)[0]

    def create_system_embed(self):
        embed = discord.Embed(title='\u200b')
        embed.set_author(name='🖥️ Host System Information')
        embed.add_field(name='📟  OS', value=(self.os_name()) + '\n\u200b')
        embed.add_field(name='🎛️ CP', value=(self.cpu_info()) + '\n\u200b')
        embed.add_field(name='🧠 RAM', value=(self.ram()) + '\n\u200b')
        embed.add_field(name='🐍 Python version', value=(self.python_version()) + '\n\u200b')
        embed.set_footer(text="Created by PrimeTime09#1847")

        return embed

    # INFO
    @commands.command(aliases=['information', 'about'])
    async def info(self, ctx):
        """
        About the bot
        """
        embed = discord.Embed(title='\u200b', description='Lastest Changes:\n' + self.get_last_commits() + '\n')
        embed.add_field(name='📁 Repo',
                        value='[Gitlab](https://gitlab.com/pryme-svg/primebot) [Github](https://github.com/pryme-svg/primebot)'
                              '\n\u200b')
        embed.add_field(name='🕒 uptime',
                        value=await self.uptime()
                        )
        embed.set_footer(text="Created by PrimeTime09#1847")
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)

    @commands.command(name="uptime")
    async def _uptime(self, ctx):
        """Get bot uptime"""
        await ctx.send(embed=discord.Embed(title='🕒 Uptime', description=await self.uptime()))

    # SYSTEM
    @commands.command(name='system', ignore_extra=False, aliases=['sys'])
    async def command_system(self, context):
        """
        Shows bot host system information

        OS, CPU, RAM, Python version and Uptime

        ex:
        `<prefix>system`
        `<prefix>sys`
        """
        embed = self.system_embed
        embed.add_field(name='🕒 Uptime', value=(await self.uptime()) + '\n\u200b')

        await context.send(embed=embed)

        embed.remove_field(-1)

    @commands.command(hidden=True)
    async def prime(self, ctx):
        embed = discord.Embed(title="Prime", description="Thanks for using my bot! Feel free to browse my [github](https://github.com/pryme-svg)\nOr check out my [gitlab](https://gitlab.com/pryme-svg)\nThis bot is open source, please star the repository! [gitlab](https://gitlab.com/pryme-svg/primebot/) [github](https://github.com/pryme-svg/primebot/)!")
        await ctx.send(embed=embed)

    @commands.command(aliases=['src'])
    async def source(self, ctx):
        """Show Source Code"""
        title = "View Source"
        description = "https://github.com/pryme-svg/primebot"
        # TODO: src for individual commands
        await ctx.send(embed=discord.Embed(title=title, description=description))

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """
        Shows bot invite
        """
        embed = discord.Embed(title="Invite", description="Invite PrimeBot [here]({})".format(primebot.conf['invite']))
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Gets the bot's latency"""
        start = time.perf_counter()
        message = await ctx.send(
            embed=discord.Embed(title="🏓 Pong", description=f":electric_plug: **Websocket** {round(self.bot.latency * 1000, 3)}ms"))
        end = time.perf_counter()
        duration = (end - start) * 1000
        em = message.embeds[0].copy()
        em.description += (
            f'\n<:discord:822019576606228500> **API** {duration:.3f}ms'
        )
        await asyncio.sleep(0.25)
        await message.edit(embed=em)


def setup(bot):
    bot.add_cog(Meta(bot))
