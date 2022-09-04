from random import randint

import discord
from discord.ext import commands

from utils import send_embed


class Simprate(commands.Cog):
    '''
    Find out how much of a simp you are!
    Usage:
    `<prefix> simprate [member]`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['simp', 'ratesimp', 'howsimp'])
    async def simprate(self, ctx, member: discord.Member = None, *, content=None):
        if not member:
            member = ctx.message.author
        simprate = randint(0,100)
        description = """You are {}% simp.""".format(simprate)
        if simprate < 10:
            description += '\n'

        await send_embed(ctx, '{}\'s simp calculator'.format(member.name), description)

def setup(bot):
    bot.add_cog(Simprate(bot))