import discord 
from discord.ext import commands 
from discord.ext.commands import MemberConverter
class Moderation(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason=None):
        converter = discord.ext.commands.MemberConverter()
        member = await converter.convert(ctx, member)
        await member.kick(reason= 'Kicked by: {}, Reason: {}'.format(ctx.message.author,reason))
        await ctx.send(f'User {member.mention} has been kicked')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason=None):
        converter = discord.ext.commands.MemberConverter()
        member = await converter.convert(ctx, member)
        await member.ban(reason= 'Banned by: {}, Reason: {}'.format(ctx.message.author,reason))
        await ctx.send(f'User {member.mention} has been banned')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban (ctx, *, member):
        if '@' in member:
            member = member[1:]
        if '#' not in member:
            user = await bot.fetch_user(member)
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

def setup(bot): 
    bot.add_cog(Moderation(bot))
