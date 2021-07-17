import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not member:
            await ctx.channel.send('Please specify a member to unmute.')
            return
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.channel.send('**%s** has been successfully unmuted by **%s**.' % (member, ctx.message.author))
            channel = await member.create_dm()
            await channel.send(
                f'**{member.name}**, you were unmuted in **{ctx.guild}** by **{ctx.message.author}**.'
            )
        else:
            await ctx.channel.send('**%s** was never muted in the first place.' % (member))

def setup(bot):
    bot.add_cog(Unmute(bot))