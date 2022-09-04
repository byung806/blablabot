from random import choice

import discord
from discord.ext import commands

from utils import send_embed


class Coinflip(commands.Cog):
    '''
    Flip a coin.
    Usage:
    `<prefix> coinflip [call]`
    '''

    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['coin','flip','cf'])
    async def coinflip(self, ctx, call=None, *, content=None):
        if not call:
            await send_embed(ctx, ctx.author.display_name, f'The coin came up **{choice(["heads", "tails"])}**.')
        else:
            result = choice(["heads", "tails"])
            if call.lower() in result:
                await send_embed(ctx, 'You win!', f'The coin came up **{result}**.')
            else:
                await send_embed(ctx, 'You lose!', f'The coin came up **{result}**.')

def setup(bot):
    bot.add_cog(Coinflip(bot))