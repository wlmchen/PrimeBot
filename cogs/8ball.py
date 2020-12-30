import discord 
import random
from discord.ext import commands 

class ball(commands.Cog): 
    def __init__(self, bot): 
        self.bot = bot 
    @commands.cooldown(20, 30, commands.BucketType.user)

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        if ctx.message.mention_everyone:
            await ctx.send("You may not tag everyone in this command {}".format(ctx.message.author.mention))
            return
        responses = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

def setup(bot):
    bot.add_cog(ball(bot))
