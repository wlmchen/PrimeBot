from discord.ext import commands
import base64


class Encoding(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def b64encode(self, ctx, *, arg):
        to_encode = arg
        encoded = base64.b64encode(bytes(to_encode, 'utf-8'))
        await ctx.send(encoded)

    @commands.command()
    async def b64decode(self, ctx, *, arg):
        to_decode = arg
        decoded = base64.b64decode(to_decode)
        await ctx.send(decoded)

    @commands.command()
    async def b16encode(self, ctx, *, arg):
        to_encode = arg
        encoded = base64.b16encode(bytes(to_encode, 'utf-8'))
        await ctx.send(encoded)

    @commands.command()
    async def b16decode(self, ctx, *, arg):
        to_decode = arg
        decoded = base64.b16decode(to_decode)
        await ctx.send(decoded)

    @commands.command()
    async def a85encode(self, ctx, *, arg):
        to_encode = arg
        encoded = base64.a85encode(bytes(to_encode, 'utf-8'))
        await ctx.send(encoded)

    @commands.command()
    async def a85decode(self, ctx, *, arg):
        to_decode = arg
        decoded = base64.a85decode(to_decode)
        await ctx.send(decoded)

    @commands.command()
    async def b85encode(self, ctx, *, arg):
        to_encode = arg
        encoded = base64.b85encode(bytes(to_encode, 'utf-8'))
        await ctx.send(encoded)

    @commands.command()
    async def b85decode(self, ctx, *, arg):
        to_decode = arg
        decoded = base64.b85decode(to_decode)
        await ctx.send(decoded)


def setup(bot):
    bot.add_cog(Encoding(bot))
