from random import randint
from random import choice
from discord.ext import commands

from utils import send_embed, get_server_prefix


class Gen_Pw(commands.Cog):
    '''
    Generate a random password.
    Usage:
    `<prefix> gen_pw [length] [characters]`
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['generate_pass', 'generate_password', 'genpw', 'genpass'])
    async def gen_pw(self, ctx, length=None, chars=None, *, content=None):
        if not length:
            length = randint(6,12)
        if chars:
            possible = chars
        else:
            possible = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        pw = ''
        for _ in range(int(length)):
            pw += choice(possible)

        await send_embed(ctx, 'Generated password', pw)

    @gen_pw.error
    async def gen_pw_error(self, ctx, error):
        if isinstance(error, ValueError):
            await send_embed(ctx, 'Invalid usage', f'Use `{get_server_prefix(self.bot, ctx)}genpw '
                                                   f'[length] [possible characters]`')
        else:
            raise error

def setup(bot):
    bot.add_cog(Gen_Pw(bot))