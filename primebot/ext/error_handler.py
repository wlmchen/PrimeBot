import discord
import math
from discord.ext import commands
import primebot
import traceback


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_error(self, ctx, error, errorChannel):
        await errorChannel.send('Unhandled Message: {} \n Content: {} \n Error: {}\n'.format(ctx.message, ctx.message.content, error))
        with open('error.log', 'a') as f:
            f.write('Unhandled Message: {} \n Content: {} \n Error: {}\n'.format(ctx.message, ctx.message.content, error))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        errorChannel = self.bot.get_channel(primebot.conf['error_channel'])
        ignore_errors = (
            commands.CommandNotFound,
            commands.NotOwner,
        )

        if isinstance(error, ignore_errors):
            return

        await errorChannel.send("Traceback\n```{}\n```".format(traceback.format_exc()))

        if str(error) is not None:
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: " + str(error)))
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: You don't have the permission to execute this bot command!"))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The bot command doesn't exist!"))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The command is incomplete, missing one or more parameters!"))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(color=discord.Color.red(), description=":x: The command was entered incorrectly, one or more parameters are wrong or in the wrong place!"))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))

        await self.log_error(ctx, error, errorChannel)


def setup(bot):
    bot.add_cog(Error(bot))
