import discord
from primebot.utils.formatters import list_to_bullets

from discord.ext import commands
import primebot


class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def command_tag(self, ctx, tag=None):
        if tag is None:
            await ctx.send_help('tag')
            return
        if primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': tag}) is None:
            return await ctx.send("Tag not found")
        description = primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': tag})['content']
        embed = discord.Embed(title=tag, description=description, color=0x32CD32)
        await ctx.send(embed=embed)

    @command_tag.command(name='new')
    async def command_tag_new(self, ctx, name, *, content):
        if primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': name}) is not None:
            return await ctx.send("Tag already exists")
        if len(content) >= 2048:
            return await ctx.send("Tag is too long")
        if len(list(primebot.db.tags.find({'guild_id': ctx.guild.id}))) >= 100:
            return await ctx.send("Your server has too many tags")
        tag = {
            "guild_id": ctx.guild.id,
            "name": str(name),
            "content": str(content)
        }
        primebot.db.tags.insert(tag)
        await ctx.send("Tag Created")

    @commands.has_permissions(administrator=True)
    @command_tag.command(name='delete', aliases=['remove', 'del'])
    async def command_tag_delete(self, ctx, name):
        if primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': name}) is None:
            return await ctx.send("Tag not found")
        primebot.db.tags.delete_one({'guild_id': ctx.guild.id, 'name': name})
        await ctx.send("tag deleted")

    @command_tag.command(name='list', aliases=['l'])
    async def command_tag_list(self, ctx):
        listt = []
        lst = primebot.db.tags.find({'guild_id': ctx.guild.id})
        for doc in lst:
            listt.append(doc['name'])
        embed = discord.Embed(title="Tags", description=list_to_bullets(listt), color=0x32CD32)
        await ctx.send(embed=embed)

    @command_tag.command(name='raw')
    async def command_tag_raw(self, ctx, name):
        if primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': name}) is None:
            return await ctx.send("Tag not found")
        tag = primebot.db.tags.find_one({'guild_id': ctx.guild.id, 'name': name})
        await ctx.send("```\n" + tag['content'] + "```")

    @command_tag.command(name='edit')
    @commands.has_permissions(administrator=True)
    async def command_tag_edit(self, ctx, name, *, content):
        query = {"name": str(name), "guild_id": ctx.guild.id}
        new = {"$set": {"content": content}}

        primebot.db.tags.update_one(query, new)

        await ctx.send("Updated Tag")


def setup(bot):
    bot.add_cog(Tags(bot))
