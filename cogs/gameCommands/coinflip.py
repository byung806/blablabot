from random import random

import discord
from discord.ext import commands

class Coinflip(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def print_coin_result(self, result, author, call=None):
        global embedcolor, embed
        if call:
            if call == result:
                embedcolor = discord.Colour.green()
            else:
                embedcolor = discord.Colour.red()
            embed = discord.Embed(
                #title='{}\'s coinflip'.format(author),
                colour=embedcolor,
                description="""You chose **{}**.
                The coin was **{}**.""".format(call, result)
            )
            embed.set_author(name='{}\'s coinflip'.format(author))
        else:
            embedcolor = discord.Colour.gold()
            embed = discord.Embed(
                #title='{}\'s coinflip'.format(author),
                colour=embedcolor,
                description="""The coin was {}.""".format(result)
            )
            embed.set_author(name='{}\'s coinflip'.format(author))
        return embed

    @commands.command(aliases=['coin','flip','cf'])
    async def coinflip(self, ctx, call=None):
        if call:
            if call.lower() == 'heads':
                if random() <= 0.5:
                    await ctx.message.channel.send(embed=await self.print_coin_result('heads', ctx.message.author.name, 'heads'))
                else:
                    await ctx.message.channel.send(embed=await self.print_coin_result('tails', ctx.message.author.name, 'heads'))
            elif call.lower() == 'tails':
                a = random()
                if a >= 0.5:
                    await ctx.message.channel.send(embed=await self.print_coin_result('tails', ctx.message.author.name, 'tails'))
                else:
                    await ctx.message.channel.send(embed=await self.print_coin_result('heads', ctx.message.author.name, 'tails'))
            else:
                await ctx.channel.send('That\'s not a valid option. Try again.')
        else:
            if random() <= 0.5:
                randomcall = 'heads'
            else:
                randomcall = 'tails'
            await ctx.message.channel.send(embed=await self.print_coin_result(randomcall, ctx.message.author.name))


def setup(bot):
    bot.add_cog(Coinflip(bot))