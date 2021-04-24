import discord
# import math
from discord.ext import commands
import primebot
import traceback


class Error(commands.Cog):
    """Handle bot errors"""
    def __init__(self, bot):
        self.bot = bot

    async def log_error(self, ctx, error, errorChannel, tb):
        await errorChannel.send('Unhandled Message: {} \n Content: {} \n Error: {}\n'.format(ctx.message, ctx.message.content, error))
        new = {
            "message": ctx.message.content,
            "error": str(error),
            "traceback": str(tb)
        }
        primebot.db.errors.insert_one(new)
        with open('error.log', 'a') as f:
            f.write('Unhandled Message: {} \n Content: {} \n Error: {}\n'.format(ctx.message, ctx.message.content, error))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errorChannel = self.bot.get_channel(primebot.conf['log']['error_channel'])
        original_error = error
        ignore_errors = (
            commands.CommandNotFound,
        )

        if isinstance(error, ignore_errors):
            return
        if isinstance(error, commands.NotOwner):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: This command can only be used by developers"))
            return
        if isinstance(error, commands.errors.MaxConcurrencyReached):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: " + str(error)))
            return
        if isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: Incorrect Parameters"))
            return
        if isinstance(error, commands.errors.PartialEmojiConversionFailure):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: Could not convert to custom emoji"))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            # await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The command is incomplete, missing one or more parameters!"))
            await ctx.send_help(ctx.command)
            return
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(color=discord.Color.red(), description=":x: This is not an nsfw channel")
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.message.add_reaction("⏰")
            # await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))

        tb = "".join(traceback.format_exception(type(original_error), original_error, original_error.__traceback__))

        if len(tb) > 1980:
            tb = tb[:1980]
        await errorChannel.send("Traceback\n```{}\n```".format(tb))

        if str(error) is not None:
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: " + str(error)))
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: You don't have the permission to execute this bot command!"))
        # elif isinstance(error, commands.CommandNotFound):
        #     await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The bot command doesn't exist!"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The command was entered incorrectly, one or more parameters are wrong or in the wrong place!"))

        await self.log_error(ctx, error, errorChannel, tb)


def setup(bot):
    bot.add_cog(Error(bot))
