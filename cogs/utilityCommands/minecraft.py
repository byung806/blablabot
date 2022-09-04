import io

import numpy as np
from PIL import Image
from io import BytesIO
import requests
import discord
from discord.ext import commands
from time import perf_counter

from cogs._data.minecraft.solid_blocks.aa_mc_mapping import SOLID_BLOCKS_MC_MAPPING
from utils import send_embed


class Minecraft(commands.Cog):
    '''
    Convert an image to minecraft blocks!
    Usage:
    `<prefix> minecraft [member | image]`
    '''
    def __init__(self, bot):
        self.bot = bot

    async def get_closest_block(self, rgba, colors):
        distances = np.sqrt(np.sum((colors - rgba) ** 2, axis=1))
        return SOLID_BLOCKS_MC_MAPPING[tuple(colors[np.where(distances == min(distances))][0])]

    @commands.command(aliases=['mc'])
    @commands.guild_only()
    async def minecraft(self, ctx, *, user: discord.Member = None):
        async with ctx.typing():
            start = perf_counter()
            size = 64
            if ctx.message.attachments:
                img = Image.open(BytesIO(await ctx.message.attachments[0].read())).convert('RGBA')
            else:
                if user == None:
                    img = Image.open(requests.get(
                        'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024'.format(ctx.message.author), stream=True).raw)
                else:
                    img = Image.open(requests.get(
                        'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024'.format(user), stream=True).raw)


            if img.width > size:
                height = img.height // (img.width / size)
                img = img.resize((size, int(height)))
            elif img.height > size:
                width = img.width // (img.height / size)
                img = img.resize((int(width), size))

            colors = np.array(list(SOLID_BLOCKS_MC_MAPPING.keys()))

            cached_color_blocks = dict()
            with Image.new('RGBA', (img.width*16, img.height*16)) as result:
                for y in range(img.height):
                    for x in range(img.width):
                        color = np.array(img.getpixel((x, y)))
                        if tuple(color) in cached_color_blocks:
                            block_name = cached_color_blocks[tuple(color)]
                        else:
                            block_name = await self.get_closest_block(color, colors)
                            cached_color_blocks[tuple(color)] = block_name
                        result = result.convert('RGBA')
                        try:
                            result.paste(Image.open(r'cogs\_data\minecraft\solid_blocks\{}'.format(block_name)), (x*16,y*16))
                        except:
                            result.paste(Image.open('/app/cogs/_data/minecraft/solid_blocks/{}'.format(block_name)), (x*16,y*16))

            with io.BytesIO() as image_binary:
                result.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.message.channel.send(f'Time taken: {round(perf_counter()-start, 2)} seconds',
                                               file=discord.File(fp=image_binary, filename='minecraft.png'))

    @minecraft.error
    async def mc_error(self, ctx, error):
        await send_embed(ctx, 'Provide a valid image', 'Attach an image or mention a user to see minecraft magic.')

def setup(bot):
    bot.add_cog(Minecraft(bot))
