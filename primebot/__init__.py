from .config.config_loader import * # noqa
from primebot.utils import errors
import primebot
import discord
from discord.ext import commands


class PrimeBot(commands.Bot):

    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all()  # enable all intents
        super().__init__(command_prefix=self.get_prefix,
                         intents=intents,
                         allowed_mentions=allowed_mentions,
                         )

        self.add_check(self.check_blacklist)
        self._cd = commands.CooldownMapping.from_cooldown(2, 3, commands.BucketType.user)
        self.add_check(self.global_cooldown, call_once=True)

        for ext in primebot.conf['exts']:
            self.load_extension('primebot.ext.{}'.format(ext))

    async def global_cooldown(self, ctx):
        bucket = self._cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after and not await self.is_owner(ctx.author):
            raise commands.CommandOnCooldown(bucket, retry_after)
        return True

    async def get_prefix(bot, message):
        try:
            guild_id = message.guild.id
        except AttributeError:  # errors if in dm
            prefix = primebot.conf['prefix']
            return commands.when_mentioned_or(prefix)(bot, message)
        # if guild doesn't exist in db
        if primebot.db.prefixes.find_one({'guild_id': guild_id}) is None:
            new = {
                "guild_id": guild_id,
                "guild_name": message.guild.name,
                "prefix": primebot.conf['prefix']
            }
            primebot.db.prefixes.insert_one(new)
        prefix = primebot.db.prefixes.find_one({"guild_id": guild_id})['prefix']
        return commands.when_mentioned_or(prefix)(bot, message)  # allow ping as prefix

    def check_blacklist(self, ctx):
        if ctx.author.id in primebot.conf["blacklist"]:
            raise errors.Blacklisted()
        else:
            return True

    async def closeman(self):
        await super().close()
        await self.logout()
        primebot.db.close()

    def run(self):
        super().run(primebot.conf['token'])
