import discord
import requests
import random
from discord.ext import commands


class Urban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alises=["ud", "urbandict"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, *, arg):

        url = "https://api.urbandictionary.com/v0/define?term=" + arg
        json1 = requests.get(url)
        data = json1.json()
        if not data["list"]:
            await ctx.send("Word not Found!")
            return
        definition = data["list"][0]["definition"]
        title = "Urban Dictionary: " + arg
        if len(definition) > 2000:
            definition = definition[0:2000]
            title = title + " (Truncated)"
        embed = discord.Embed(title=title, description=definition)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Urban(bot))
