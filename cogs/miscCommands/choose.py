import discord
from random import choice
from discord.ext import commands


class Choose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['select'])
    async def choose(self, ctx, *, message):
        choices = message.split(' ')
        await ctx.message.channel.send(f"{ctx.message.author.mention}, I choose `{choice(choices)}`.")

def setup(bot):
    bot.add_cog(Choose(bot))