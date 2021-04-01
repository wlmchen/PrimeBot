from discord.ext import commands
import primebot


def is_pt():
    async def predicate(ctx):
        if ctx.guild.id == primebot.conf['pt_guild']:
            return True
        elif await ctx.bot.is_owner(ctx.author):
            return True
        else:
            return False
    return commands.check(predicate)
