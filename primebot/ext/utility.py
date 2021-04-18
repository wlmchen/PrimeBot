import discord
import asyncio
import math # noqa
import time
import datetime
from pyparsing import ParseException

from primebot.utils.math import convert_size

from primebot.utils.paginator import Menu

from primebot.utils.formatters import list_to_bullets

from typing import Union
from bs4 import BeautifulSoup
from discord.ext import commands
import random
import primebot
import subprocess


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def scrape_pypi(self, query):  # i know this is messy but who cares
        url = "https://pypi.org/pypi/{}/json".format(query)
        page = await self.bot.session.get(url)
        if page.status == 404:
            raise commands.CommandError("Package not found")
        json = await page.json()
        author = json['info']['author']
        homepage = json['info']['home_page']
        license = json['info']['license']
        description = json['info']['summary']
        url = json['info']['package_url']
        name = json['info']['name'] + ' ' + json['info']['version']

        return homepage, author, license, description, url, name

    async def scrape_crates(self, crate):
        url = "https://crates.io/api/v1/crates/{}".format(crate)
        raw = await self.bot.cached_session.get(url)
        if raw.status == 404:
            raise commands.CommandError("Crate not found")
        json = await raw.json()
        crate = json['crate']
        name = crate['name']
        description = crate['description']
        version = crate['max_version']
        repo = crate['repository']
        docs = crate['documentation']
        downloads = crate['downloads']
        created_at = crate['created_at']
        owners = []
        owner_json = await self.bot.cached_session.get("https://crates.io{}".format(crate['links']['owners']))
        owner_json = await owner_json.json()
        owner_json = owner_json['users']
        for owner in owner_json:
            owners.append('[{}]({})'.format(owner['name'], owner['url']))
        return name, description, version, repo, docs, downloads, created_at, owners

    async def scrape_arch(self, package):
        url = "https://archlinux.org/packages/search/json/?name={}".format(package)
        raw = await self.bot.cached_session.get(url)
        json = await raw.json()
        pkg = json['results'][0]

        name = pkg['pkgname']
        description = pkg['pkgdesc']
        url = pkg['url']
        repo = pkg['repo']
        version = pkg['pkgver']
        pkgrel = pkg['pkgrel']
        arch = pkg['arch']
        pkg_size = convert_size(pkg['compressed_size'])
        installed_size = convert_size(pkg['installed_size'])
        licenses = pkg['licenses']
        build_date = pkg['build_date']
        maintainer = pkg['maintainers'][0]
        packager = pkg['packager']

        provides = pkg['provides']
        conflicts = pkg['conflicts']
        replaces = pkg['replaces']
        depends = pkg['depends']
        optdepends = pkg['optdepends']
        return name, description, url, repo, version, pkgrel, arch, pkg_size, installed_size, licenses, build_date, maintainer, packager, provides, conflicts, replaces, depends, optdepends

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string == '':
            return 'None'
        else:
            return string[:-2]

    @commands.command()
    async def whois(self, ctx, member=None):
        """Get information about a member"""
        if member is None:
            member = str(ctx.message.author.id)

        if '@everyone' in ctx.message.content:
            await ctx.send("You may not ping everyone in this command! {}".format(ctx.message.author.mention))
            return

        converter = discord.ext.commands.MemberConverter()
        member = await converter.convert(ctx, member)
        if member is not None:
            embed = discord.Embed()
            embed.set_footer(text=f'UserID: {member.id}')
            embed.set_thumbnail(url=member.avatar_url)
            # if member.name != member.display_name:
            #    fullName = f'{member} ({member.display_name})'
            # else:
            #    fullName = member
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            # embed.add_field(name=member.name, value=fullName, inline=False)
            embed.add_field(name='whois', value=member.mention, inline=False)
            embed.add_field(name='Joined Discord on:', value='{}\n'.format(member.created_at.strftime('%m/%d/%Y %H:%M:%S')), inline=True)
            embed.add_field(name='Joined Server on', value='{}\n'.format(member.joined_at.strftime('%m/%d/%Y %H:%M:%S')), inline=True)
            embed.add_field(name='Avatar Link', value=member.avatar_url, inline=False)
            embed.add_field(name='Roles', value=self._getRoles(member.roles), inline=True)
            await ctx.send(embed=embed)
        else:
            msg = 'You have not specified a user!'
            await ctx.send(msg)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def githead(self, ctx):
        """Get info about the latest commit"""
        head = subprocess.run(['git', '--no-pager', 'show', 'HEAD'], stdout=subprocess.PIPE)
        if len(head.stdout.decode('utf-8')) > 2000:
            mystr = head.stdout.decode('utf-8')
            mystr = mystr[0:2030]
        else:
            mystr = head.stdout.decode('utf-8')
        mystr = "```diff\n" + mystr + "```"
        embedHead = discord.Embed(title="Git Head", description=mystr, url="https://github.com/pryme-svg/PrimeBot/commit/HEAD")
        embedHead.add_field(name="\u200b", value="[Git Repository](https://github.com/pryme-svg/primebot)")
        await ctx.send(embed=embedHead)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gitlog(self, ctx):
        """Get a log of git commits"""
        log = subprocess.run(['git', '--no-pager', 'log'], stdout=subprocess.PIPE)
        if len(log.stdout.decode('utf-8')) > 2000:
            mystr = log.stdout.decode('utf-8')
            mystr = mystr[0:2030]
            mystr = "```\n" + mystr + "```"
        else:
            mystr = log.stdout.decode('utf-8')
            mystr = "```\n" + mystr + "```"
        embedLog = discord.Embed(title="Git Log(truncated)", description=mystr)
        embedLog.add_field(name="\u200b", value="[Git Repository](https://github.com/pryme-svg/primebot)")
        await ctx.send(embed=embedLog)

    @commands.command(aliases=['pip'])
    async def pypi(self, ctx, *, query):
        """
        Search PyPI for a python package
        """
        homepage, author, license, description, url, name = await self.scrape_pypi(query)
        embed = discord.Embed(title=name, url=url, description=description)
        embed.add_field(name="Author", value=author)
        embed.add_field(name="License", value=license)
        embed.add_field(name="Homepage", value=homepage)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_thumbnail(url="https://raw.githubusercontent.com/github/explore/666de02829613e0244e9441b114edb85781e972c/topics/pip/pip.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def crate(self, ctx, *, query):
        """Search crates.io for a crate"""
        name, desc, version, repo, docs, downloads, created_at, owners = await self.scrape_crates(query)
        url = "https://crates.io/crates/{}".format(name)
        title = name + ' ' + version
        embed = discord.Embed(title=title, url=url, description=desc)
        embed.add_field(name="Author{}".format('' if len(owners) == 1 else's'), value=list_to_bullets(owners))
        embed.add_field(name="Repository", value=repo)
        embed.add_field(name="Documentation", value=docs, inline=False)
        embed.add_field(name="Downloads", value=downloads)
        embed.set_footer(text="Created at: {}".format(created_at))
        embed.set_thumbnail(url="https://doc.rust-lang.org/cargo/images/Cargo-Logo-Small.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['archpkg'])
    async def arch(self, ctx, *, query):
        """Search the Arch Linux Repository"""
        try:
            name, description, url, repo, version, pkgrel, arch, pkg_size, installed_size, licenses, build_date, maintainer, packager, provides, conflicts, replaces, depends, optdepends = await self.scrape_arch(query)
        except IndexError:
            raise commands.CommandError("Package not Found")
        name1 = "{} {}-{} ({})".format(name, version, pkgrel, arch)
        embed = discord.Embed(title=name1, url=url, color=0x1793d1)
        embed.add_field(name="Description", value=description)
        embed.add_field(name="License{}".format('' if len(licenses) == 1 else 's'), value=list_to_bullets(licenses))
        embed.add_field(name="Repository", value=repo)
        embed.add_field(name="Sizes", value="**Package Size:** {}\n**Installed Size:** {}".format(pkg_size, installed_size))
        embed.add_field(name="Build Date", value=build_date)
        embed.add_field(name="Maintainer", value=maintainer)
        embed.add_field(name="Packager", value=packager)
        embed.add_field(name="\u200b", value="**Provides:** {}\n**Conflicts:** {}\n**Replaces:** {}\n**Depends:** {}\n**Optdepends:** {}".format(list_to_bullets(provides), list_to_bullets(conflicts), list_to_bullets(replaces), list_to_bullets(depends), list_to_bullets(optdepends)))
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Archlinux-icon-crystal-64.svg/1024px-Archlinux-icon-crystal-64.svg.png")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        """Create a poll"""
        # options = [(word.lower()) for word in options]
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def country(self, ctx, *, country):
        """Get information about a country"""
        json = await self.bot.cached_session.get("https://restcountries.eu/rest/v2/name/{}".format(country)).json()
        try:
            if json['status'] == 404:
                raise commands.CommandError(json['message'])
        except TypeError:
            pass
        embeds = []
        for country in json:
            embed = discord.Embed(title=country['name'], color=discord.Color.blurple())
            embed.set_thumbnail(url="https://www.countryflags.io/{}/flat/64.png".format(country['alpha2Code']))
            embed.add_field(name="Population", value=country['population'])
            embed.add_field(name="Capital", value=country['capital'])
            embed.add_field(name="Currency", value=f"{country['currencies'][0]['name']} ({country['currencies'][0]['symbol']})")
            embed.add_field(name="Located in", value=country['subregion'])
            embed.add_field(name="Demonym", value=country['demonym'])
            embed.add_field(name="Native Name", value=country['nativeName'])
            if country['area'] is not None:
                embed.add_field(name="Area", value="{:,} km\u00b2 ({:,} mi\u00b2)".format(country['area'], country['area'] * 0.62137))
            embed.set_author(name="Country Information - {}".format(country['name']))
            embed.timestamp = ctx.message.created_at

            embeds.append(embed)

        pages = primebot.utils.paginator.EmbedsSource(embeds)
        menu = Menu(pages)
        await menu.start(ctx)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def big(self, ctx, emoji: discord.PartialEmoji):
        """Enlarge an emoji"""
        url = emoji.url
        embed = discord.Embed(title=emoji.name)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text="Emoji ID: {}".format(emoji.id))
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['aw'])
    async def archwiki(self, ctx, *, query):
        """Search the ArchWiki"""

        url = "https://wiki.archlinux.org/index.php?search={}".format(query)

        html = await self.bot.cached_session.get(url)
        redirected = False
        for e in html.history:
            if e.status == 302:
                redirected = True
        html_string = await html.text()
        if redirected is not True:
            links = []
            titles = []
            description = ''
            reactions = []
            i = 1
            a = 0
            e = BeautifulSoup(html_string, 'html.parser')

            def check(reaction, user):
                return user == ctx.message.author

            for result in e.find_all('li', class_="mw-search-result"):
                links.append('https://wiki.archlinux.org' + result.find('a')['href'])
                titles.append(result.find('a')['title'])
            # max of 9 results
            links = links[:9]
            if len(links) == 0:
                raise commands.CommandError("Query not Found")

            for link, title in zip(links, titles):
                description += str(i) + '. ' + '[{}]({})'.format(title, link) + '\n'
                i += 1
            embed = discord.Embed(title="Results: " + query, description=description, color=0x1793d1)
            message = await ctx.send(embed=embed)
            emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(len(links)+1)][1:]
            for reaction in emojis:
                await message.add_reaction(reaction)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                return
            reaction = str(reaction)
            reaction = reaction.replace('1⃣', '1')
            reaction = reaction.replace('2⃣', '2')
            reaction = reaction.replace('3⃣', '3')
            reaction = reaction.replace('4⃣', '4')
            reaction = reaction.replace('5⃣', '5')
            reaction = reaction.replace('6⃣', '6')
            reaction = reaction.replace('7⃣', '7')
            reaction = reaction.replace('8⃣', '8')
            reaction = reaction.replace('9⃣', '9')
            reaction = int(reaction)
            urlo = links[reaction-1]
            title = titles[reaction-1]
        if 'urlo' in locals():
            html_string = await self.bot.session.get(urlo)
            html_string = await html_string.text()
        try:
            test1 = html_string[html_string.index("</ul></div>"):html_string.index("Contents")]
        except ValueError:
            raise commands.CommandError("Page not found!")
            return
        soup = BeautifulSoup(test1, "html.parser")
        description = "".join(soup.strings)
        if 'urlo' in locals():
            embedAw = discord.Embed(title="Arch Wiki: " + title, description=description, url=url, color=0x1793d1)
            await message.clear_reactions()
            await message.edit(embed=embedAw)
            return

        url = "https://wiki.archlinux.org/index.php?search={}".format(query)
        embedAw = discord.Embed(title="Arch Wiki: " + query, description=description, url=url, color=0x1793d1)
        await ctx.send(embed=embedAw)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, member: Union[discord.Member, int] = None):
        """Get a user avatar"""
        if member is None:
            member = ctx.message.author
        else:
            member = (await self.bot.fetch_user(member) if isinstance(member, int) else member)
            # converter = discord.ext.commands.MemberConverter()
            # avamember = await converter.convert(ctx, avamember)
        userAvatarUrl = member.avatar_url
        embedAvatar = discord.Embed(title=str(member), description='', url=str(userAvatarUrl))
        embedAvatar.set_image(url=userAvatarUrl)
        embedAvatar.set_author(name=member.name, icon_url=member.avatar_url)
        await ctx.send(embed=embedAvatar)

    @commands.command()
    async def apod(self, ctx, date=None):
        """Get the astronomy picture of the day"""
        API_KEY = primebot.conf['api']['nasa_api_key']

        if date is None:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY
            r = await self.bot.session.get(url)
        else:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY + "&date=" + date
            r = await self.bot.cached_session.get(url)

        json_file = await r.json()
        if 'code' in json_file:
            await ctx.send(json_file['msg'])
            return

        embedApod = discord.Embed(title=json_file['title'], description=json_file['explanation'])
        embedApod.set_footer(text=json_file['date'])
        embedApod.set_image(url=json_file['url'])
        await ctx.send(embed=embedApod)

    @commands.command()
    async def translate(self, ctx, sourcelanguage, targetlanguage, *, content):
        """
        Translate text

        Usage:

        <prefix>translate (source_language) (target_language) content

        Available Languages: English(en), Spanish(es), Arabic(ar), Chinese(zh), French(fr), German(de), Hindi(hi), Irish(ga), Italian(it), Japanese(ja), Korean(ko), Portugese(pt), Russian(ru)
        """
        langs = ['en', 'es', 'ar', 'zh', 'fr', 'de', 'hi', 'ga', 'it', 'ja', 'ko', 'pt', 'ru']
        if sourcelanguage not in langs or targetlanguage not in langs:
            return await ctx.send("Invalid Language")
        url = "https://libretranslate.com/translate?q={}&source={}&target={}".format(content, sourcelanguage, targetlanguage)
        json = await self.session.post(url)
        json = await json.json()
        translated = json['translatedText']
        embed = discord.Embed(title="Translation", description=translated)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text="{} => {}".format(sourcelanguage, targetlanguage))
        await ctx.send(embed=embed)

    @commands.command(name="math")
    async def _math(self, ctx, *, m):
        """
        Do math
        """
        start = time.time()
        try:
            result = str(primebot.utils.parsers.NumericStringParser().eval(m))
        except ParseException:
            raise commands.CommandError("Invalid Expression")
        end = time.time()
        embed = discord.Embed(title="Math result", description=result)
        embed.set_footer(text="Done in {}".format(end - start))
        await ctx.send(embed=embed)

    @commands.command(aliases=['gh'])
    async def github(self, ctx, *, repo):
        """
        Get Information about a GitHub repository

        ex.

        <prefix>gh pryme-svg/primebot
        """
        json = await self.bot.session.get('https://api.github.com/repos/{}'.format(repo))
        json = await json.json()
        try:
            if json['message'] == "Not Found":
                raise commands.CommandError("Repo not found")
        except KeyError:
            pass
        if json['description'] is None:
            description = "No Description Provided"
        else:
            description = json['description']
        if json['license'] is None:
            license = "copyright"
        else:
            license = json['license']['name']
        embed = discord.Embed(title=json['name'], description=description, url=json['html_url'])
        embed.set_thumbnail(url=json['owner']['avatar_url'])
        embed.add_field(name='Author', value=json['owner']['login'])
        if license == "Other":
            license_url = 'other'
        else:
            license_url = "https://choosealicense.com/licenses/{}".format(json['license']['spdx_id'])
        embed.add_field(name="License", value="[{}]({})".format(license, license_url))
        embed.set_footer(text="Repo created at: {}".format(json['created_at']))
        if json['language'] is not None:
            try:
                emoji = primebot.conf['emojis'][json['language'].lower()]
            except KeyError:
                emoji = ''
            embed.add_field(name="Language", value="{} {}".format(emoji, json['language']))

        await ctx.send(embed=embed)

    @commands.command()
    async def distro(self, ctx, *, arg):
        """Get information about a GNU/Linux distribution"""
        if arg == "random":
            arg = (random.choice(list(open('primebot/assets/linux.list'))))

        url = "http://www.distrowatch.com/table.php?distribution=" + arg
        html_string = await self.bot.cached_session.get(url).text
        pattern = "<br /><br />"

        if "The distribution you requested" in html_string:
            description = ":x: That distro doesn't exist!"
            embed = discord.Embed(title='Distro not Found', description=description)
            await ctx.send(embed=embed)
            return

#        for line in html_string.splitlines():
#            if len(line) > 100 and '<' not in line and 'is a' in line:
#                description = line
#                break

        for (num, line) in enumerate(html_string.splitlines()):
            if pattern in line:
                linenum = num
                break
#
#        try:
#            linenum
#        except NameError:
#            description = ":x: That distro doesn't exist!"
#            embed = discord.Embed(title='Distro not Found', description=description)
#            await ctx.send(embed=embed)
#            return
#
        description = html_string.splitlines()[linenum - 1]

        soup = BeautifulSoup(html_string, 'html.parser')
        title = soup.title.string
        embed = discord.Embed(title=title, description=description)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
