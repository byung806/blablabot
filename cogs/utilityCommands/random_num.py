import discord
import random
from discord.ext import commands

class RandomNum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['randomnum', 'rn', 'randonum', 'randonumber', 'random_num', 'random_number'])
    async def randomnumber(self, ctx, *, range=None):
        if range:
            desc = random.randint(*list(map(lambda x: int(x.rstrip()), range.split('-'))))
        else:
            desc = random.randint(1,100)
        embed = discord.Embed(
            description=desc,
            color=discord.Color.blurple()
        ).set_author(name='Generated random number', icon_url=ctx.author.avatar_url)
        await ctx.message.channel.send(embed=embed)

    @randomnumber.error
    async def randomnumber_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(
                description='You need a valid range. `bla x-y`',
            ).set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(RandomNum(bot))