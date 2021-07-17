import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None, reason = None):
        try:
            if reason:
                ban_reason = reason
                if ban_reason == '':
                    await member.send(
                        'You were banned from **%s** by **%s**. **Reason:** %s.' % (member.guild, ctx.message.author, 'None'))
                    await member.message.channel.send(
                        '%s has been banned by **%s**. **Reason:** %s.' % (member.name, ctx.message.author, 'None'))
                else:
                    await member.send(
                        'You were banned from **%s** by **%s**. **Reason:** %s.' % (member.guild, ctx.message.author, ban_reason))
                    await member.message.channel.send(
                        '**%s** has been banned by **%s**. **Reason:** %s.' % (member.name, ctx.message.author, ban_reason))
                await member.ban()
        except:
            await ctx.message.channel.send('**An error occurred** when trying to ban **{}**.'.format(member.name))

def setup(bot):
    bot.add_cog(Ban(bot))