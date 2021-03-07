import discord
import primebot
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
#        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.guilds)} servers!"))
        await self.bot.change_presence(activity=discord.Game(name=">help | {} servers".format(len(self.bot.guilds))))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content[0] == '>' and message.content[1] != ' ':
            logChannel = self.bot.get_channel(primebot.conf['log_channel'])
            await logChannel.send('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(message.author, message.content, message.guild.name, message.channel.name))
            with open('log.txt', 'a') as log:
                log.write('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(message.author, message.content, message.guild.name, message.channel.name))
        if 'happy birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        if 'i want to die' in message.content.lower():
            await message.channel.send("Are you considering suicide? You are not alone. If you feel suicidal, please call the suicide prevention hotline at 800-273-8255.")


def setup(bot):
    bot.add_cog(Events(bot))
