from random import randint

import discord
from discord.ext import commands


class Simprate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['simp', 'ratesimp', 'howsimp'])
    async def simprate(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        simprate = randint(0,100)
        description = """You are {}% simp.""".format(simprate)
        if simprate < 10:
            description += '\n'
        title = '{}\'s simp calculator'.format(member.name)
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour.from_rgb(randint(0,255), randint(0,255), randint(0,255))
        )
        await ctx.message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Simprate(bot))