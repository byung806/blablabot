import discord
from discord.ext import commands

class Perms(commands.Cog):
    '''
    Check the permissions of someone.
    Usage:
    `<prefix> check_permissions [member]`
    '''

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='perms', aliases=['checkperms', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)
        embed = discord.Embed(title='Permissions:', description=perms, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_footer(text="{} (ID: {})".format(ctx.guild.name, ctx.guild.id))
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Perms(bot))