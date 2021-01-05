import discord
from datetime import datetime, timedelta
from discord.ext import commands

class Whois(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
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
    async def whois(self, ctx, member: discord.Member=None):
        if member == None:
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
            embed.add_field(name='Joined Discord on:', value='{}\n)'.format(member.created_at.strftime('%d.%m.%Y')), inline=True)
            embed.add_field(name='Joined Server on', value='{}\n)'.format(member.joined_at.strftime('%d.%m.%Y')), inline=True)
            embed.add_field(name='Avatar Link', value=member.avatar_url, inline=False)
            embed.add_field(name='Roles', value=self._getRoles(member.roles), inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            await ctx.send(embed=embed)
        else:
            msg = 'You have not specified a user!'
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(Whois(bot))
