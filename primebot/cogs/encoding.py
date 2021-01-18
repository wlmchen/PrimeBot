from discord.ext import commands
import base64


class Encoding(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def str_to_b64(arg):
        message_bytes = arg.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    @staticmethod
    def b64_to_str(arg):
        base64_bytes = arg.encode('ascii')
        message_btytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message

    @commands.command()
    async def b64encode(self, ctx, *, arg):
        to_encode = arg
        await ctx.send(self.str_to_b64(to_encode))

    @commands.command()
    async def b64decode(self, ctx, *, arg):
        to_decode = arg
        await ctx.send(self.b64_to_str(to_decode))


def setup(bot):
    bot.add_cog(Encoding(bot))
