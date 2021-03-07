from discord.ext import commands


def is_owner():
    async def predicate(ctx):
        is_owner = await ctx.bot.is_owner(ctx.author)
        if not is_owner:
            raise commands.CheckFailure(
                "This command can only be used by developers"
            )
        return True

    return commands.check(predicate)
