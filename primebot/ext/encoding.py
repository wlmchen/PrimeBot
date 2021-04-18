from discord.ext import commands
import base64


class Encoding(commands.Cog):
    """Encode text into various bases"""
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
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message

    @staticmethod
    def str_to_b16(arg):
        b = arg.encode("UTF-8")
        e = base64.b16encode(b)
        s1 = e.decode("UTF-8")
        return s1

    @staticmethod
    def b16_to_str(arg):
        b1 = arg.encode("UTF-8")
        d = base64.b16decode(b1)
        s2 = d.decode("UTF-8")
        return s2

    @staticmethod
    def str_to_b32(arg):
        b = arg.encode("UTF-8")
        e = base64.b32encode(b)
        s1 = e.decode("UTF-8")
        return s1

    @staticmethod
    def b32_to_str(arg):
        b1 = arg.encode("UTF-8")
        d = base64.b32decode(b1)
        s2 = d.decode("UTF-8")
        return s2

    @staticmethod
    def str_to_b85(arg):
        b = arg.encode("UTF-8")
        e = base64.b85encode(b)
        s1 = e.decode("UTF-8")
        return s1

    @staticmethod
    def b85_to_str(arg):
        b1 = arg.encode("UTF-8")
        d = base64.b85decode(b1)
        s2 = d.decode("UTF-8")
        return s2

    @commands.command(aliases=['b64e'])
    async def b64encode(self, ctx, *, arg):
        """
        Encode text into base64
        """
        to_encode = arg
        await ctx.send(self.str_to_b64(to_encode))

    @commands.command(aliases=['b64d'])
    async def b64decode(self, ctx, *, arg):
        """
        Decode text from base64
        """
        to_decode = arg
        await ctx.send(self.b64_to_str(to_decode))

    @commands.command(aliases=['b16e'])
    async def b16encode(self, ctx, *, arg):
        """
        Encode text into base16
        """
        to_encode = arg
        await ctx.send(self.str_to_b16(to_encode))

    @commands.command(aliases=['b16d'])
    async def b16decode(self, ctx, *, arg):
        """
        Decode text from base16
        """
        to_decode = arg
        await ctx.send(self.b16_to_str(to_decode))

    @commands.command(aliases=['b32e'])
    async def b32encode(self, ctx, *, arg):
        """
        Encode text into base32
        """
        to_encode = arg
        await ctx.send(self.str_to_b32(to_encode))

    @commands.command(aliases=['b32d'])
    async def b32decode(self, ctx, *, arg):
        """
        Decode text from base32
        """
        to_decode = arg
        await ctx.send(self.b32_to_str(to_decode))

    @commands.command(aliases=['b85e'])
    async def b85encode(self, ctx, *, arg):
        """
        Encode text into base85
        """
        to_encode = arg
        await ctx.send(self.str_to_b85(to_encode))

    @commands.command(aliases=['b85d'])
    async def b85decode(self, ctx, *, arg):
        """
        Decode text from base85
        """
        to_decode = arg
        await ctx.send(self.b85_to_str(to_decode))


def setup(bot):
    bot.add_cog(Encoding(bot))
