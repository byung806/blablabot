import discord
from discord.ext import commands

class TopRole(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='toprole', aliases=['top_role'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        global top_role
        if member is None:
            member = ctx.author
        await ctx.send(f'The top role for {member.display_name} is `{member.top_role.name}`.')

def setup(bot):
    bot.add_cog(TopRole(bot))