import discord
import primebot
from discord.ext import commands


async def log_on_message(self, message):
    messageChannel = self.bot.get_channel(primebot.conf['log']['events_channel'])
    await messageChannel.send('Message Author: {}\nMessage Content: ```{}```\nLocation: {} # {}\n\n'.format(message.author, message.content, message.guild.name, message.channel.name))


class Events(commands.Cog):
    """Handle various bot events"""
    def __init__(self, bot):
        self.bot = bot



    async def amp_to_normal(self, url):
        """
        Check if the given URL is an AMP url. If it is, send a request to find the normal URL
        :param url: The URL to check
        :type url: string
        :returns: Returns the non-AMP version of the given URL if it's an AMP URL. Otherwise, it returns None
        :rtype: str or None
        """
        if primebot.utils.parsers.is_amp(url):
            r = await self.bot.cached_session.get(url)
            return r.url
        else:
            return None


    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as ---->', self.bot.user, 'ID:', self.bot.user.id)
        await self.bot.change_presence(activity=discord.Game(name=">help | {} servers".format(len(self.bot.guilds))))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        logChannel = self.bot.get_channel(primebot.conf['log']['log_channel'])
        await logChannel.send('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(ctx.message.author, ctx.message.content, ctx.message.guild.name, ctx.message.channel.name))
        new = {
            "author": str(ctx.message.author),
            "content": str(ctx.message.content),
            "location": ctx.message.guild.name + "#" + ctx.message.channel.name
        }
        primebot.db.executed.insert_one(new)
        with open('log.txt', 'a') as log:
            log.write('Message Author: {}\nMessage Content: {}\nLocation: {} # {}\n\n'.format(ctx.message.author, ctx.message.content, ctx.message.guild.name, ctx.message.channel.name))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        # amp google links
        matches = primebot.utils.parsers.extract_urls(message.content)
        if matches:
            urls = []
            for match in matches:
                if primebot.utils.parsers.is_amp(match):
                    urls.append(await self.amp_to_normal(match))
            if urls:
                embed = discord.Embed(title="Non AMP Links", color=discord.Color.blurple())
                for url in urls:
                    embed.add_field(name="\u200b", value=url, inline=False)
                await message.reply(embed=embed, mention_author=False)
                await log_on_message(self, message)
        # google redirects
        matches = primebot.utils.parsers.extract_urls(message.content)
        if matches:
            urls = []
            for match in matches:
                if primebot.utils.parsers.is_google_redirect(match):
                    urls.append(primebot.utils.parsers.follow_google_redirect(match))
            if urls:
                embed = discord.Embed(title="Un-Googlified Links", color=discord.Color.blurple())
                embed.set_footer(text="Or even better, use DuckDuckGo")
                for url in urls:
                    embed.add_field(name="\u200b", value=url, inline=False)
                await message.reply(embed=embed, mention_author=False)
                await log_on_message(self, message)

        # youtube to indivious
        # matches = primebot.utils.parsers.extract_urls(message.content)
        # if matches:
        #     urls = []
        #     for match in matches:
        #         if primebot.utils.parsers.is_yt(match):
        #             urls.append(primebot.utils.parsers.yt_to_invidious(match))
        #     if urls:
        #         embed = discord.Embed(title="Invidious Links")
        #         for url in urls:
        #             embed.add_field(name="\u200b", value=url, inline=False)
        #         await message.channel.send(embed=embed)
        #         await log_on_message(self, message)
        if 'happy birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        if 'i want to die' in message.content.lower():
            await message.channel.send("Are you considering suicide? You are not alone. If you feel suicidal, please call the suicide prevention hotline at 800-273-8255.")

        if message.content == '<@!788810436535386112>' or message.content == '<@788810436535386112>':
            await message.channel.send("Prefix is {}".format(primebot.db.prefixes.find_one({"guild_id": message.guild.id})['prefix']))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(description=f"Joined guild {guild.name} [{guild.id}]")
        embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
        embed.add_field(
            name="**Members**",  # Basic stats about the guild
            value=f"**Total:** {len(guild.members)}\n" + f"**Admins:** {len([m for m in guild.members if m.guild_permissions.administrator])}\n" + f"**Owner: ** {guild.owner}\n", inline=False)
        guildChannel = self.bot.get_channel(primebot.conf['log']['guild_notifs'])
        await guildChannel.send(embed=embed)
        guild_id = guild.id
        primebot.db.prefixes.delete_one({'guild_id': guild_id})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(description=f"Removed from guild {guild.name} [{guild.id}]")
        embed.set_thumbnail(url=guild.icon_url_as(static_format="png"))
        guildChannel = self.bot.get_channel(primebot.conf['log']['guild_notifs'])
        await guildChannel.send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
