from .config.config_loader import * # noqa
import primebot
import discord
from discord.ext import commands


async def get_prefix(bot, message):
    guild_id = message.guild.id
    # if guild doesn't exist in db
    if primebot.db.prefixes.prefixes.find_one({'guild_id': guild_id}) is None:
        new = {
            "guild_id": guild_id,
            "guild_name": message.guild.name,
            "prefix": primebot.conf['prefix']
        }
        primebot.db.prefixes.prefixes.insert_one(new)
    prefix = primebot.db.prefixes.prefixes.find_one({"guild_id": guild_id})['prefix']
    return commands.when_mentioned_or(*prefix)(bot, message)  # allow ping as prefix


class PrimeBot(commands.Bot):

    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all()  # enable all intents
        super().__init__(command_prefix=get_prefix,
                         intents=intents,
                         allowed_mentions=allowed_mentions
                         )

        for ext in primebot.conf['exts']:
            self.load_extension('primebot.ext.{}'.format(ext))

    async def close(self):
        await super().close()
        await self.logout()
        primebot.db.close()

    def run(self):
        super().run(primebot.conf['token'])
