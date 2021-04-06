import discord
import primebot
from discord.ext import commands
from typing import Union


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['changeprefix'])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str):
        guild_id = ctx.guild.id
        result = primebot.db.prefixes.update_one({'guild_id': guild_id}, {"$set": {"prefix": prefix}})
        if result.matched_count > 0:
            await ctx.send("prefix changed to {}".format(prefix))
        else:
            await ctx.send("failed")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban_message(self, ctx, *, msg: str = None):
        """
        Set the ban message of the server
        Use {reason} as a placeholder
        """
        guild_id = ctx.guild.id
        if msg is None and primebot.db.ban_messages.find_one({'guild_id': guild_id})['message'] is None:
            return await ctx.send("No message set")
        elif msg is None:
            await ctx.send(primebot.db.ban_messages.find_one({'guild_id': guild_id})['message'])
            return
        if primebot.db.ban_messages.find_one({'guild_id': guild_id}) is None:
            new = {
                "guild_id": guild_id,
                "message": msg
            }
            primebot.db.ban_messages.insert_one(new)
            await ctx.send("ban message changed to {}".format(msg))
        else:
            result = primebot.db.ban_messages.update_one({'guild_id': guild_id}, {'$set': {'message': msg}})
            if result.matched_count > 0:
                await ctx.send("ban message changed to {}".format(msg))
            else:
                await ctx.send("failed")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def log_channel(self, ctx, channel: int):
        guild_id = ctx.guild.id
        if self.bot.get_channel(channel) is None:
            raise commands.CommandError("Invalid Channel! ☹️")
        if primebot.db.log_channels.find_one({'guild_id': guild_id}) is None:
            new = {
                "guild_id": guild_id,
                "channel_id": channel
            }
            primebot.db.log_channels.insert_one(new)
        else:
            result = primebot.db.log_channels.update_one({'guild_id': guild_id}, {"$set": {'channel_id': channel}})
            if result.matched_count > 0:
                await ctx.send("log channel changed to to {}".format(channel))
            else:
                await ctx.send("failed")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason=None):
        converter = discord.ext.commands.MemberConverter()
        member = await converter.convert(ctx, member)
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot kick yourself {}".format(ctx.message.author.mention))
            return
        if primebot.db.log_channels.find_one({'guild_id': ctx.guild.id}) is not None:
            embed = discord.Embed(description="Event: kick\nModerator: {}\nReason: {}\nUser: {}".format(ctx.author.mention, reason, member.mention))
            await self.bot.get_channel(int(primebot.db.log_channels.find_one({'guild_id': ctx.guild.id})['channel_id'])).send(embed=embed)

        await member.kick(reason='Kicked by: {}, Reason: {}'.format(ctx.message.author, reason))
        await ctx.send(f'User {member.mention} has been kicked')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Union[discord.Member, int], *, reason=None):
        user_obj = (
            await self.bot.fetch_user(member) if isinstance(member, int) else member
        )
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself {}".format(ctx.message.author.mention))
            return
        if primebot.db.ban_messages.find_one({'guild_id': ctx.guild.id}) is not None:
            await user_obj.send(primebot.db.ban_messages.find_one({'guild_id': ctx.guild.id})['message'].format(reason=reason))
        if primebot.db.log_channels.find_one({'guild_id': ctx.guild.id}) is not None:
            embed = discord.Embed(description="Event: ban\nModerator: {}\nReason: {}\nUser: {}".format(ctx.author.mention, reason, user_obj.mention))
            await self.bot.get_channel(int(primebot.db.log_channels.find_one({'guild_id': ctx.guild.id})['channel_id'])).send(embed=embed)
        await ctx.guild.ban(user_obj, reason=f"{ctx.author} ({ctx.author.id}) - {reason}", delete_message_days=0)
        await ctx.send(f'User {user_obj.mention} has been banned')
        # user = await discord.ext.commands.MemberConverter().convert(ctx, member)
        # await user.send(reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if '@' in member:
            member = member[1:]
        if '#' not in member:
            user = await self.bot.fetch_user(member)
            if primebot.db.log_channels.find_one({'guild_id': ctx.guild.id}) is not None:
                embed = discord.Embed(description="Event: unban\nModerator: {}\nUser: {}".format(ctx.author.mention, user.mention))
                await self.bot.get_channel(int(primebot.db.log_channels.find_one({'guild_id': ctx.guild.id})['channel_id'])).send(embed=embed)
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                if primebot.db.log_channels.find_one({'guild_id': ctx.guild.id}) is not None:
                    embed = discord.Embed(description="Event: unban\nModerator: {}\nUser: {}".format(ctx.author.mention, user.mention))
                    await self.bot.get_channel(int(primebot.db.log_channels.find_one({'guild_id': ctx.guild.id})['channel_id'])).send(embed=embed)

                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['clean', 'purge'])
    async def clear(self, ctx, amount):
        amount = int(amount)
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Moderation(bot))
