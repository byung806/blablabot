import asyncio

import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        if member == ctx.message.author:
            await ctx.channel.send('You can\'t mute yourself.')
        elif member is None:
            await ctx.channel.send('You can\'t mute nobody.')
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not member:
                await ctx.channel.send('Please specify a member to mute.')
                return
            await member.add_roles(role)
            await ctx.channel.send('**%s** has been successfully muted by **%s**.' % (member, ctx.message.author))
            channel = await member.create_dm()
            await channel.send(
                f'**{member.name}**, you were muted in the server by **{ctx.message.author}**.'
                f' | **Reason:** %s. You may contact them to appeal the mute.' % reason
            )

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            description = """You are missing the following permissions:"""
            for perm in error.missing_perms:
                description += '\n`{}`'.format(perm)
            embed = discord.Embed(
                title='You are missing something...',
                colour=discord.Colour.red(),
                description=description
            )
            ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Mute(bot))