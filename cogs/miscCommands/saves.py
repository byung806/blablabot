import discord
from random import choice
from discord.ext import commands


class Save(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def saves(self, ctx, command, *, message=None):
        #if ctx.message.author.id in self.users_saves:
            #print(self.users_saves[ctx.message.author.id])


        if message != None:
            if ctx.message.author.id in UserSaves.users_saves:
                # UserSaves.users_saves[ctx.message.author.id] = []
                if command == 'add':
                    UserSaves.users_saves[ctx.message.author.id].append(message)
                elif command == 'remove' or command == 'delete':
                    if message in UserSaves.users_saves[ctx.message.author.id]:
                        UserSaves.users_saves[ctx.message.author.id].remove(message)
                        await ctx.message.channel.send(f'Successfully removed "{message}".')
                    else:
                        await ctx.message.channel.send('You must specify the exact message saved.')
            else:
                if command == 'add':
                    UserSaves.users_saves[ctx.message.author.id] = [message]
        else:
            if ctx.message.author.id in UserSaves.users_saves:
                if command == 'clear':
                    UserSaves.users_saves.pop(ctx.message.author.id)
                    await ctx.message.channel.send('cleared')
                elif command == 'view':
                    print('view')
                    description = """"""
                    print(UserSaves.users_saves[ctx.message.author.id])
                    for save in UserSaves.users_saves[ctx.message.author.id]:
                        description += save
                        description += '\n'
                    embed = discord.Embed(
                        description=description,
                        colour=discord.Colour.green()
                    ).set_author(name=f'{ctx.message.author.name}\'s saves')
                    await ctx.message.channel.send(embed=embed)
            else:
                if command == 'help' or command == 'info':
                    await ctx.message.channel.send('help/info command')

class UserSaves:
    users_saves = {}

def setup(bot):
    bot.add_cog(Save(bot))