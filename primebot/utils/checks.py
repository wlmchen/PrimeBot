from discord.ext import commands
import primebot


def is_owner():
    async def predicate(ctx):
        is_owner = await ctx.bot.is_owner(ctx.author)
        if not is_owner:
            raise commands.CheckFailure(
                "This command can only be used by developers"
            )
        return True

    return commands.check(predicate)


def is_pt():
    async def predicate(ctx):
        if ctx.guild.id == primebot.conf['pt_guild']:
            return True
        elif await ctx.bot.is_owner(ctx.author):
            return True
        else:
            return False
    return commands.check(predicate)
