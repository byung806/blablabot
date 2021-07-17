import sys
from io import StringIO
from time import perf_counter

import discord
from discord.ext import commands

class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['eval'])
    async def evaluate(self, ctx, *, code):
        if ctx.message.author.id != 461345173314732052:
            raise PermissionError
        else:
            old_stdout = sys.stdout
            sys.stdout = result = StringIO()
            start = perf_counter()
            try:
                eval(code[3:-3].rstrip())
            except Exception as e:
                print(e)
            end = perf_counter()
            sys.stdout = old_stdout
            await ctx.message.channel.send(f'Time taken: {end-start:.8f} seconds\n```{result.getvalue()}```')

    @evaluate.error
    async def evaluate_error(self, ctx, error):
        if isinstance(error, PermissionError):
            embed = discord.Embed(
                description='You need to be blabla to run this command. Sorry!',
                colour=discord.Colour.blurple()
            ).set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Eval(bot))