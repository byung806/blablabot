import discord
import datetime
from discord.ext import commands

class JoinDate(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases = ['joindate'])
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        dateJoined = member.joined_at.strftime("%b-%d-%Y (%H:%M:%S)")
        embed = discord.Embed(title='Joined:', description=dateJoined, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.set_footer(text = "{} (ID: {})".format(ctx.guild.name, ctx.guild.id))
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(JoinDate(bot))