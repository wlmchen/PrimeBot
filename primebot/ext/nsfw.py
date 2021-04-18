import discord
import json
from discord.ext import commands


class Nsfw(commands.Cog):
    """NSFW commands 🔞"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def neko(self, ctx, query=None):
        """
        Get neko

        Example:

        <prefix>neko tickle

        Queries: '8ball', 'Random_hentai_gif', 'meow', 'erok', 'lizard', 'feetg', 'baka', 'v3', 'bj', 'erokemo', 'tickle', 'feed', 'neko', 'kuni', 'femdom', 'futanari', 'smallboobs', 'goose', 'nekoapi_v3.1', 'poke', 'les', 'trap', 'pat', 'boobs', 'blowjob', 'hentai', 'hololewd', 'ngif', 'fox_girl', 'wallpaper', 'lewdk', 'solog', 'pussy', 'yuri', 'lewdkemo', 'lewd', 'anal', 'pwankg', 'nsfw_avatar', 'eron', 'kiss', 'pussy_jpg', 'woof', 'hug', 'keta', 'cuddle', 'eroyuri', 'slap', 'cum_jpg', 'waifu', 'gecg', 'tits', 'avatar', 'holoero', 'classic', 'kemonomimi', 'feet', 'gasm', 'spank', 'erofeet', 'ero', 'solo', 'cum', 'smug', 'holo', 'nsfw_neko_gif'
        """
        queries = ['8ball', 'Random_hentai_gif', 'meow', 'erok', 'lizard', 'feetg', 'baka', 'v3', 'bj', 'erokemo', 'tickle', 'feed', 'neko', 'kuni', 'femdom', 'futanari', 'smallboobs', 'goose', 'nekoapi_v3.1', 'poke', 'les', 'trap', 'pat', 'boobs', 'blowjob', 'hentai', 'hololewd', 'ngif', 'fox_girl', 'wallpaper', 'lewdk', 'solog', 'pussy', 'yuri', 'lewdkemo', 'lewd', 'anal', 'pwankg', 'nsfw_avatar', 'eron', 'kiss', 'pussy_jpg', 'woof', 'hug', 'keta', 'cuddle', 'eroyuri', 'slap', 'cum_jpg', 'waifu', 'gecg', 'tits', 'avatar', 'holoero', 'classic', 'kemonomimi', 'feet', 'gasm', 'spank', 'erofeet', 'ero', 'solo', 'cum', 'smug', 'holo', 'nsfw_neko_gif']
        if query is None:
            query = "tits"

        if query not in queries:
            raise commands.CommandError("Invalid query for neko")
        neko_url = "https://nekos.life/api/v2/img/" + query
        response = await self.bot.session.get(neko_url)
        data = json.loads(await response.text())
        url = data['url']
        embed = discord.Embed(title="Neko")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nsfw(bot))
