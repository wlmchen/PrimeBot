from discord.ext import menus
from discord.ext.commands import Paginator as CommandPaginator
import discord


class Menu(menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=90.0, source=source)

    async def finalize(self, timed_out):
        try:
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()
        except discord.HTTPException:
            pass


class EmbedsSource(menus.ListPageSource):
    def __init__(self, embeds):
        self.embeds = embeds
        super().__init__([*range(len(embeds))], per_page=1)

    async def format_page(self, menu, page):
        maximum = len(self.embeds)
        if maximum > 1:
            footer = f'Page {page + 1}/{len(self.embeds)}'
            self.embeds[page].set_footer(text=footer)
        return self.embeds[page]

class TextPageSource(menus.ListPageSource):
    def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
        pages = CommandPaginator(prefix=prefix, suffix=suffix, max_size=max_size - 200)
        for line in text.split('\n'):
            pages.add_line(line)

        super().__init__(entries=pages.pages, per_page=1)

    async def format_page(self, menu, content):
        maximum = self.get_max_pages()
        if maximum > 1:
            return f'{content}\nPage {menu.current_page + 1}/{maximum}'
        return content
