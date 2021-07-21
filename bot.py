import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions
TOKEN = "NzQ1MDEwNDMyNDY0NjUwNDA4.XzrjCA.vl44UbFBfvq5uFQbi9rVpiFiIMk" #blablabot
bot = commands.Bot(command_prefix='bla ', case_insensitive=True)
bot.remove_command('help')

initial_extensions = [
    'cogs.funCommands.simprate',
    'cogs.gameCommands.coinflip',
    'cogs.memberCommands.perms',
    'cogs.memberCommands.userinfo',
    #'cogs.miscCommands.calculate',
    'cogs.miscCommands.choose',
    'cogs.miscCommands.halloween',
    #'cogs.miscCommands.saves',
    #'cogs.modCommands.ban',
    #'cogs.modCommands.kick',
    #'cogs.modCommands.mute',
    #'cogs.modCommands.unban',
    #'cogs.modCommands.unmute',
    #'cogs.modCommands.warn',
    'cogs.textCommands.emojify',
    #'cogs.utilityCommands.eval',
    'cogs.utilityCommands.minecraft',
    'cogs.utilityCommands.ocr',
    'cogs.utilityCommands.pass_maker',
    'cogs.utilityCommands.random_num',
]

for extension in initial_extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following servers:\n')
    for guild in bot.guilds:
        print(
            f'{guild.name} (id: {guild.id})'
        )

bot.run(TOKEN)