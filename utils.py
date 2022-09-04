import datetime
import json
from random import choice

import discord

PREFIX = 'bla '


async def get_millis_time():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


async def choose_random_member(ctx, bots=False):
    guild_members = ctx.channel.guild.members
    member = choice(guild_members)
    if not bots:
        while member.bot:
            member = choice(guild_members)
    return member


async def get_embed_color(user_id, hex_code=False):
    data = json.load(open('cogs\\_data\\colors.json', 'r'))
    if str(user_id) in data:
        if not hex_code:
            sixteenIntegerHex = int(data[str(user_id)].replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            return readableHex
        else:
            return data[str(user_id)]
    else:
        if not hex_code:
            return 0xffffff  # white color
        else:
            return '#FFFFFF'


async def mixed_case(*args):
    total = []
    import itertools
    for string in args:
        a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
        for x in list(a): total.append(x)
    return list(total)


async def get_server_prefix(bot, message) -> str:
    data = json.load(open('cogs\\_data\\prefixes.json', 'r'))
    if str(message.guild.id) in data:
        return data[str(message.guild.id)]
    else:
        return PREFIX


async def get_server_prefix_list(bot, message) -> list[str]:
    if isinstance(message.channel, discord.DMChannel):
        return await mixed_case(PREFIX)
    data = json.load(open('cogs\\_data\\prefixes.json', 'r'))
    if str(message.guild.id) in data:
        return await mixed_case(data[str(message.guild.id)])
    else:
        return await mixed_case(PREFIX)


async def send_embed(ctx, title, description, avatar_url=None, send=True):
    if not avatar_url:
        avatar_url = ctx.author.avatar_url
    embed = discord.Embed(
        description=description,
        color=await get_embed_color(ctx.author.id)
    ).set_author(name=title, icon_url=avatar_url)
    if send:
        return await ctx.send(embed=embed)
    else:
        return embed