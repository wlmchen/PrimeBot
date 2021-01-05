import discord
import datetime
from discord.ext import commands

class Whois(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.message.author

        if '@' in ctx.message.content:
            await ctx.send("You may not ping in this command! {}".format(ctx.message.author.mention))
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
            embed.add_field(name='Discord beigetreten am', value='{}\n(Tage seitdem: {})'.format(member.created_at.strftime('%d.%m.%Y'), (datetime.now()-member.created_at).days), inline=True)
            embed.add_field(name='Server beigetreten am', value='{}\n(Tage seitdem: {})'.format(member.joined_at.strftime('%d.%m.%Y'), (datetime.now()-member.joined_at).days), inline=True)
            embed.add_field(name='Avatar Link', value=member.avatar_url, inline=False)
            embed.add_field(name='Roles', value=self._getRoles(member.roles), inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            await ctx.send(embed=embed)
        else:
            msg = 'You have not specified a user!'
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(Whois(bot))
