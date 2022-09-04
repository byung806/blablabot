import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    '''
    Print someone's user info.
    Usage:
    `<prefix> userinfo [member]`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['ui', 'user_info', 'whois'])
    async def userinfo(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        join_date = member.joined_at.strftime("%b %d %Y (%H:%M:%S)")
        creation_date = member.created_at.strftime("%b %d %Y (%H:%M:%S)")
        top_role = member.top_role.name
        avatar_url = member.avatar_url
        display_name = member.display_name
        embed = discord.Embed()
        embed.set_thumbnail(url=avatar_url)
        embed.set_author(name=str(member), icon_url=avatar_url)
        embed.add_field(name='Created at:', value=creation_date, inline=True)
        embed.add_field(name='Joined at:', value=join_date, inline=True)
        embed.add_field(name='Top role:', value=top_role, inline=True)
        embed.add_field(name='Display name:', value=display_name, inline=True)
        embed.add_field(name='Avatar URL:', value=f'[Click Here]({avatar_url})', inline=True)
        await ctx.message.channel.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        raise error

def setup(bot):
    bot.add_cog(UserInfo(bot))