import discord
from random import randint
from random import choice
from discord.ext import commands

class PassMaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['generate_pass', 'generate_password', 'genpw', 'genpass'])
    async def gen_pw(self, ctx, length=None, chars=None):
        if not length:
            length = randint(6,12)
        if chars:
            possible = chars
        else:
            possible = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        pw = ''
        for _ in range(int(length)):
            pw += choice(possible)

        embed = discord.Embed(
            description=pw,
            colour=discord.Colour.blurple()
        ).set_author(name='Generated password', icon_url=ctx.author.avatar_url)
        await ctx.message.channel.send(embed=embed)

    @gen_pw.error
    async def gen_pw_error(self, ctx, error):
        if isinstance(error, ValueError):
            embed = discord.Embed(
                description='You need to provide a valid number.'
            ).set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(PassMaker(bot))