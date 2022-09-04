import discord
from random import choice
from discord.ext import commands

from utils import get_server_prefix, send_embed


class Choose(commands.Cog):
    '''
    Choose from some choices.
    Usage:
    `<prefix> choose <choices>`
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['select'])
    async def choose(self, ctx, *, message):
        choices = message.split(' ')
        await ctx.message.channel.send(f"{ctx.message.author.mention}, I choose `{choice(choices)}`.")

    @choose.error
    async def choose_error(self, ctx, error):
        await send_embed(ctx, 'Invalid usage', f'Use `{await get_server_prefix(self.bot, ctx)}choose <options>`')

def setup(bot):
    bot.add_cog(Choose(bot))