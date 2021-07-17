import discord
from discord.ext import commands

class CommandName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['alias'])
    async def command_name(self, ctx):
        pass

    @command_name.error
    async def command_name_error(self, ctx, error):
        raise error

def setup(bot):
    bot.add_cog(CommandName(bot))