from .config.config_loader import *
import primebot
from discord.ext import commands
from .utils import *

class PrimeBot(commands.Bot):

    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all() # enable all intents
        super().__init__(
                command_prefix=primebot.conf['prefix'],
                intents=intents,
                allowed_mentions=allowed_mentions
                )

        for ext in primebot.conf['exts']:
            self.load_extension('primebot.ext.{}'.format(ext))

    def run(self):
        super().run(primebot.conf['token'])

