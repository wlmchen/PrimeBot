import discord 
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, *,  avamember):
        await convert.convert(ctx, avamember)
        userAvatarUrl = avamember.avatar_url
        embedAvatar = discord.Embed(title=str(avamember), description = '')
        embedAvatar.set_image(url=userAvatarUrl)
        await ctx.send(embed=embedAvatar)

def setup(bot):
    bot.add_cog(Avatar(bot))
