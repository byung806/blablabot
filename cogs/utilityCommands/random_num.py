import discord
import random
from discord.ext import commands

from utils import send_embed, get_server_prefix


class RandomNum(commands.Cog):
    '''
    Generate a random number.
    Usage:
    `<prefix> randomnumber [lower bound-upper bound]`
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['randomnum', 'rn', 'randonum', 'randonumber', 'random_num', 'random_number'])
    async def randomnumber(self, ctx, *, range=None):
        if range:
            desc = random.randint(*[int(x.rstrip()) for x in range.split('-')])
        else:
            desc = random.randint(1,100)
        await send_embed(ctx, 'Generated random number', desc)

    @randomnumber.error
    async def randomnumber_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await send_embed(ctx, 'Invalid usage', 'You need a valid range. Use'
                                                   f'`{await get_server_prefix(self.bot, ctx)}randomnumber'
                                                   f'[lowerbound-upperbound]`')
        else:
            raise error

def setup(bot):
    bot.add_cog(RandomNum(bot))