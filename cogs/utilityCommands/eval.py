import sys
from io import StringIO
from time import perf_counter

from discord.ext import commands

from utils import send_embed


class Eval(commands.Cog):
    '''
    Evaluate python code.
    Usage:
    `<prefix> evaluate <code block>`
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['eval'])
    async def evaluate(self, ctx, *, code):
        if ctx.message.author.id != 461345173314732052:
            raise PermissionError
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
        await send_embed(ctx, 'Something went wrong.', 'How did you even get here??')

def setup(bot):
    bot.add_cog(Eval(bot))