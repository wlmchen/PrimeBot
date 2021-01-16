import discord
import requests
import os
from dotenv import load_dotenv
from googlesearch import search 
from bs4 import BeautifulSoup
from discord.ext import commands
import random
import requests_cache


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    requests_cache.install_cache('distro_cache')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        pingEmbed = discord.Embed(title="Ping!", description='🏓 Pong! {0}s'.format(self.bot.latency))
        await ctx.send(embed=pingEmbed)

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

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author

        if '@everyone' in ctx.message.content:
            await ctx.send("You may not ping everyone in this command! {}".format(ctx.message.author.mention))
            return

        if member is not None:
            embed = discord.Embed()
            embed.set_footer(text=f'UserID: {member.id}')
            embed.set_thumbnail(url=member.avatar_url)
            if member.name != member.display_name:
                fullName = f'{member} ({member.display_name})'
            else:
                fullName = member
            embed.add_field(name=member.name, value=fullName, inline=False)
            embed.add_field(name='Joined Discord on:', value='{}\n'.format(member.created_at.strftime('%m/%d/%Y %H:%M:%S')), inline=True)
            embed.add_field(name='Joined Server on', value='{}\n'.format(member.joined_at.strftime('%m/%d/%Y %H:%M:%S')), inline=True)
            embed.add_field(name='Avatar Link', value=member.avatar_url, inline=False)
            embed.add_field(name='Roles', value=self._getRoles(member.roles), inline=True)
            await ctx.send(embed=embed)
        else:
            msg = 'You have not specified a user!'
            await ctx.send(msg)
#
#    @commands.command()
#    @commands.cooldown(1, 10, commands.BucketType.user)
#    async def githead(self, ctx):
#        head = subprocess.run(['git', '--no-pager', 'show', 'HEAD'], stdout=subprocess.PIPE)
#        if len(head.stdout.decode('utf-8')) > 2000:
#            mystr = head.stdout.decode('utf-8')
#            mystr = mystr[0:2030]
#        else:
#            mystr = head.stdout.decode('utf-8')
#        mystr = "```diff\n" + mystr + "```"
#        embedHead = discord.Embed(title="Git Head", description=mystr)
#        embedHead.add_field(name=".", value="[Git Repository](https://gitlab.com/pryme-svg/primebot)")
#        await ctx.send(embed=embedHead)
#
#    @commands.command()
#    @commands.cooldown(1, 10, commands.BucketType.user)
#    async def gitlog(self, ctx):
#        log = subprocess.run(['git', '--no-pager', 'log'], stdout=subprocess.PIPE)
#        if len(log.stdout.decode('utf-8')) > 2000:
#            mystr = log.stdout.decode('utf-8')
#            mystr = mystr[0:2030]
#            mystr = "```\n" + mystr + "```"
#        else:
#            mystr = log.stdout.decode('utf-8')
#            mystr = "```\n" + mystr + "```"
#        embedLog = discord.Embed(title="Git Log(truncated)", description=mystr)
#        embedLog.add_field(name=".", value="[Git Repository](https://gitlab.com/pryme-svg/primebot)")
#        await ctx.send(embed=embedLog)

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        options = [(word.lower()) for word in options]
        if "@" in ctx.message.content:
            await ctx.send("You may not tag everyone in this command {}".format(ctx.message.author.mention))
            return
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await self.bot.edit_message(react_message, embed=embed)

    @commands.command(aliases=['aw'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def archwiki(self, ctx, *, query):
        query1 = query + " site:https://wiki.archlinux.org"
        
        for j in search(query1): 
            url = j
            break

        html_string = requests.get(url).content
        html_string = html_string.decode('utf-8')
        try:
            test1 = html_string[html_string.index("</ul></div>"):html_string.index("Contents")]
        except ValueError:
            await ctx.send(":x: Page not Found!")
            return
        soup = BeautifulSoup(test1, "html.parser")
        description = "".join(soup.strings)

        embedAw = discord.Embed(title="Arch Wiki: " + query, description=description, color=0x1793d1)
        embedAw.set_footer(text=url)
        await ctx.send(embed=embedAw)

    @commands.command()
    async def avatar(self, ctx, *, avamember=None):
        if avamember is None:
            avamember = ctx.message.author
        else:
            converter = discord.ext.commands.MemberConverter()
            avamember = await converter.convert(ctx, avamember)
        userAvatarUrl = avamember.avatar_url
        embedAvatar = discord.Embed(title=str(avamember), description='')
        embedAvatar.set_image(url=userAvatarUrl)
        await ctx.send(embed=embedAvatar)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def apod(self, ctx, date=None):
        load_dotenv()
        API_KEY = os.getenv('API_KEY')

        if date is None:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY
            s = requests_cache.CachedSession()
            with s.cache_disabled():
                r = s.get(url)
        else:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + API_KEY + "&date=" + date
            r = requests.get(url)

        json_file = r.json()
        if 'code' in json_file:
            await ctx.send(json_file['msg'])
            return

        embedApod = discord.Embed(title=json_file['title'], description=json_file['explanation'])
        embedApod.set_footer(text=json_file['date'])
        embedApod.set_image(url=json_file['url'])
        await ctx.send(embed=embedApod)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def distro(self, ctx, *, arg):
        if arg == "random":
            arg = (random.choice(list(open('linux.list'))))

        url = "http://www.distrowatch.com/table.php?distribution=" + arg
        html_string = requests.get(url).content
        pattern = "<b><a href=\"dwres.php?resource=popularity\">"

        html_string = html_string.decode('utf-8')

#        for line in html_string.splitlines():
#            if len(line) > 100 and '<' not in line and 'is a' in line:
#                description = line
#                break

        for (num, line) in enumerate(html_string.splitlines()):
            if pattern in line:
                linenum = num

        try:
            linenum
        except NameError:
            description = ":x: That distro doesn't exist!"
            embed = discord.Embed(title='Distro not Found', description=description)
            await ctx.send(embed=embed)
            return

        description = html_string.splitlines()[linenum - 2]
        soup = BeautifulSoup(html_string)
        title = soup.title.string
        embed = discord.Embed(title=title, description=description)


def setup(bot):
    bot.add_cog(Utility(bot))
