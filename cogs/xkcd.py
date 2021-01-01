import discord
import xkcd_wrapper
from discord.ext import commands


class Xkcd(commands.Cog):
    """
    Commands that deal with XKCD webcomics
    """

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🗨️'
        self.xkcd_api_client = xkcd_wrapper.AsyncClient()

    def embed_comic(self, xkcd_comic, color=None):
        comic = discord.Embed()
        comic.set_author(name=f'xkcd #{xkcd_comic.id}: {xkcd_comic.title}',
                         url=f'https://xkcd.com/{xkcd_comic.id}',
                         icon_url='https://xkcd.com/s/0b7742.png')
        comic.set_image(url=xkcd_comic.image_url)
        comic.set_footer(text=xkcd_comic.description)
        return comic

    ##########
    # COMMANDS
    #########

    # XKCD
    @commands.group(name='xkcd', ignore_extra=False, invoke_without_command=True)
    async def command_xkcd(self, context):
        """
        Shows a random xkcd comic

        Retrieves a random xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd`
        """
        random_comic = await self.xkcd_api_client.random(raw_comic_image=False)
        embed_comic = self.embed_comic(random_comic)
        await context.send(embed=embed_comic)

    @command_xkcd.command(name='id', ignore_extra=False, aliases=['n', '-n', 'number'])
    async def command_xkcd_id(self, context, comic_id):
        comic_id = int(comic_id)

        """
        Shows the selected xkcd comic
        Retrieves the xkcd webcomic with the specified ID from xkcd.com
        ex:
        `<prefix>xkcd id` 100
        `<prefix>xkcd n` 1234
        """
        comic = await self.xkcd_api_client.get(comic_id, raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)

    # XKCD LATEST
    @command_xkcd.command(name='latest', ignore_extra=False, aliases=['l', '-l', 'last'])
    async def command_xkcd_latest(self, context):
        """
        Shows the latest xkcd comic

        Retrieves the latest xkcd webcomic from xkcd.com

        ex:
        `<prefix>xkcd latest`
        `<prefix>xkcd l`
        """
        comic = await self.xkcd_api_client.latest(raw_comic_image=False)
        embed_comic = self.embed_comic(comic)
        await context.send(embed=embed_comic)


def setup(bot):
    bot.add_cog(Xkcd(bot))
