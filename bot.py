import os
import time

import discord
from discord.ext import commands

from utils import PREFIX
from utils import get_server_prefix_list

intents = discord.Intents.all()
TOKEN = "NzQ1MDEwNDMyNDY0NjUwNDA4.XzrjCA.vl44UbFBfvq5uFQbi9rVpiFiIMk" #blablabot
bot = commands.Bot(command_prefix=get_server_prefix_list, case_insensitive=True, intents=intents)
bot.remove_command('help')


for category in os.listdir('cogs'):
    if 'Commands' in category:
        for extension in os.listdir(f'cogs\\{category}'):
            if extension.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.{category}.{extension[:-3]}')
                except Exception as e:
                    print(f'Failed to load cogs\\{category}\\{extension}: {e}')

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            prefix = PREFIX
            embed = discord.Embed(
                description=f'Hey! I\'m **blablabot**.\n\n'
                            f'To see what I can do, send `{prefix}help`. All my commands are run like this,'
                            f'with a `{prefix}` before the command (for example `{prefix}help`).\n\n',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='**Links**',
                            value='[Invite]('
                                  'https://discord.com/api/oauth2/authorize?'
                                  'client_id=745010432464650408&permissions=8&scope=bot%20applications.commands'
                                  ') - Add this bot to your servers and have fun!',inline=False)
            await channel.send(embed=embed)
        break

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following servers:\n')
    for guild in bot.guilds:
        print(
            f'{guild.name} (id: {guild.id})'
        )

bot.run(TOKEN)