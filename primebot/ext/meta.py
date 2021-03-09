import discord
import itertools
import pygit2
from discord.ext import commands
import datetime
import platform
from cpuinfo import get_cpu_info
import time
import psutil


class Meta(commands.Cog):
    """
    Commands that show information about the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.fromtimestamp(time.time())
        self.info_embed = self.create_info_embed()
        self.system_embed = self.create_system_embed()

    @commands.command()
    async def help(self, ctx):

        embedHelp = discord.Embed(title="Help", description="Default Prefix: >\nCommands:\n`>ping`\n`>quote`\n`>prime`\n`>ban`\n`>kick`\n`>roll`\n`>8ball (question)`\n`>clear (amount)`\n`>unban (member)`\n`>poll question item1 item2 ...`\n`>xkcd`\n`>xkcd latest`\n`>xkcd n <number>`\n`>sys`\n`>info`\n`>flip`\n`>distro (distro)`\n`>distro random`\n`>apod`\n`>apod (date)`\n`>archwiki (search)`\n`>define (term)`\n`>figlet (text)`\n`>invite`\n`>b64encode`\n`>b64decode`\n`>b32encode`\n`>b32decode`\n`>b16encode`\n`>b16decode`\n`>b85encode`\n`>b85decode`\n\nGet a complete list of commands [here](https://gitlab.com/pryme-svg/primebot#commands)\n\nThis Bot is Open Source! Check out the repo [here](https://gitlab.com/pryme-svg/primebot)", color=0x282828)
        embedHelp.set_footer(text="Created by PrimeTime09#1847")
        await ctx.send(embed=embedHelp)

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

    async def uptime(self):
        now = datetime.datetime.fromtimestamp(time.time())
        up_time = now - self.start_time
        return str(up_time).rsplit('.', maxsplit=1)[0]

    def create_info_embed(self):
        embed = discord.Embed(title='\u200b', description='Lastest Changes:\n' + self.get_last_commits())
        embed.set_author(name='📓 About')
        embed.add_field(name='👨‍💻 Author',
                        value='[pryme-svg](https://github.com/pryme-svg) \n\u200b')
        embed.add_field(name='🏗️ Framework',
                        value=f'[discord.py v{self.discord_version()}]'
                              '(https://github.com/Rapptz/discord.py) \n\u200b')
        embed.add_field(name='📁 Repo',
                        value='[Gitlab](https://gitlab.com/pryme-svg/primebot) [Github](https://github.com/pryme-svg/primebot)'
                              '\n\u200b')
        embed.add_field(name='🕒 Uptime',
                        value=await self.uptime
                        )
        embed.set_footer(text="Created by PrimeTime09#1847")
        return embed

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
        await ctx.send(embed=self.info_embed)

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

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """
        Shows bot invite
        """
        embed = discord.Embed(title="Invite", description="Invite PrimeBot [here](https://discord.com/api/oauth2/authorize?client_id=788810436535386112&permissions=8198&scope=bot)")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
