import primebot
from discord.ext import commands

token = primebot.conf['token']
bot = commands.Bot(command_prefix=primebot.conf['prefix'])
bot.remove_command('help')

# load cogs
for cog in primebot.conf['cogs']:
    print('cogs.{}'.format(cog))
    bot.load_extension('primebot.cogs.{}'.format(cog))

bot.run(token)
