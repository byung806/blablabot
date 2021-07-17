import discord
from math import *
from random import choice
from discord.ext import commands


class Calculate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['calc'])
    async def calculate(self, ctx, *, message=None):
        if message == None:
            description = 'What are you trying to calculate? You need to put an expression so I can calculate it.'
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            result = eval(message)
            description = f'**Your input:** `{message}`'
            if isinstance(result, int):
                description += f'\n**blablabot calculated:** `{result:,d}`'
            else:
                description += '\n**blablabot calculated:** `{:,}`'.format(result)
            description += f'\n**Raw:** `{result}`'
            embed = discord.Embed(
                description=description,
                colour=discord.Colour.green()
            ).set_author(name=f'{ctx.message.author.name}\'s calculator')
            await ctx.message.channel.send(embed=embed)
        except NameError or SyntaxError or commands.CommandInvokeError:
            description = f'**Your input:** `{message}`'
            description += f'\n**blablabot calculated:** `Could not calculate an answer`'
            embed = discord.Embed(
                description=description,
                colour=discord.Colour.red()
            ).set_author(name=f'{ctx.message.author.name}\'s calculator')
            await ctx.message.channel.send(embed=embed)

    """"@calculate.error
    async def calc_error(self, ctx, error):
        if isinstance(error, SyntaxError) or isinstance(error, commands.CommandInvokeError):
            description = 'What are you trying to calculate? You need to put a valid expression so I can calculate it.'
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
        else:
            raise error"""

def setup(bot):
    bot.add_cog(Calculate(bot))