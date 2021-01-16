import datetime
import platform
from cpuinfo import get_cpu_info
import time
import discord
import psutil
from discord.ext import commands


class Info(commands.Cog):
    """
    Commands that show information about the bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.emoji = 'ℹ️'
        self.start_time = datetime.datetime.fromtimestamp(time.time())
        self.info_embed = self.create_info_embed()
        self.system_embed = self.create_system_embed()

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

    async def uptime(self):
        now = datetime.datetime.fromtimestamp(time.time())
        up_time = now - self.start_time
        return str(up_time).rsplit('.', maxsplit=1)[0]

    def create_info_embed(self):
        embed = discord.Embed(title='\u200b')
        embed.set_author(name='📓 Information')
        embed.add_field(name='👨‍💻 Author',
                        value='[pryme-svg](https://github.com/pryme-svg) \n\u200b')
        embed.add_field(name='🏗️ Framework',
                        value=f'[discord.py v{self.discord_version()}]'
                              '(https://github.com/Rapptz/discord.py) \n\u200b')
        embed.add_field(name='📁 Repos',
                        value='[Gitlab](https://gitlab.com/pryme-svg/primebot) [Github](https://github.com/pryme-svg/primebot)'
                              '\n\u200b')
        embed.set_footer(text="Created by PrimeTime09#1847, Running on Heroku")
        return embed

    def create_system_embed(self):
        embed = discord.Embed(title='\u200b')
        embed.set_author(name='🖥️ Host System Information')
        embed.add_field(name='📟  OS', value=(self.os_name()) + '\n\u200b')
        embed.add_field(name='🎛️ CPU', value=(self.cpu_info()) + '\n\u200b')
        embed.add_field(name='🧠 RAM', value=(self.ram()) + '\n\u200b')
        embed.add_field(name='🐍 Python version', value=(self.python_version()) + '\n\u200b')
        embed.set_footer(text="Created by PrimeTime09#1847, Running on Heroku")

        return embed

    ##########
    # COMMANDS
    ##########

    # INFO
    @commands.command(name='info', ignore_extra=False, aliases=['information'])
    async def command_info(self, context):
        """
        Shows author, github page and framework

        ex:
        `<prefix>info`
        `<prefix>information`
        """
        await context.send(embed=self.info_embed)

    # SYSTEM
    @commands.command(name='system', ignore_extra=False, aliases=['sys'])
    async def command_system(self, context):
        """
        Shows bot host system information

        OS, CPU, RAM, Python version and Up time

        ex:
        `<prefix>system`
        `<prefix>sys`
        """
        embed = self.system_embed
        embed.add_field(name='🕒 Up time', value=(await self.uptime()) + '\n\u200b')

        await context.send(embed=embed)

        embed.remove_field(-1)

    @commands.command()
    async def prime(self, ctx):
        embed = discord.Embed(title="Prime", description="Thanks for using my bot! Feel free to browse my [github](https://github.com/pryme-svg)\nOr check out my [gitlab](https://gitlab.com/pryme-svg)\nThis bot is open source, please star the repository! [gitlab](https://gitlab.com/pryme-svg/primebot/) [github](https://github.com/pryme-svg/primebot/)!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
