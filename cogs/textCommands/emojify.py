import discord
from discord.ext import commands


class Emojify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['emoji'])
    async def emojify(self, ctx, *, message=None):
        if message==None:
            description = 'What are you trying to emojify?'
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
            return
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        numbers = {
            '1': ':one:',
            '2': ':two:',
            '3': ':three:',
            '4': ':four:',
            '5': ':five:',
            '6': ':six:',
            '7': ':seven:',
            '8': ':eight:',
            '9': ':nine:',
            '0': ':zero:',
            '#': ':hash:',
            '*': ':asterisk:'
        }
        new_message = ''
        for letter in message:
            if letter.lower() in alphabet:
                new_message+=':regional_indicator_'+letter.lower()+': '
            elif letter == ' ':
                new_message+= '    '
            elif letter in numbers:
                new_message+=numbers[letter]
                new_message+=' '
            else:
                new_message+=letter
                new_message+=' '
        await ctx.message.channel.send(new_message)

def setup(bot):
    bot.add_cog(Emojify(bot))