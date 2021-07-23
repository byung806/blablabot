import io

import numpy as np
from PIL import Image
from io import BytesIO
import requests
import discord
from discord.ext import commands


from cogs.utilityCommands.solid_blocks.aa_mc_mapping import SOLID_BLOCKS_MC_MAPPING, ALL_BLOCKS_MC_MAPPING

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_closest_block(self, rgba, colors, type):
        distances = np.sqrt(np.sum((colors - rgba) ** 2, axis=1))
        if type == 'all':
            return ALL_BLOCKS_MC_MAPPING[tuple(colors[np.where(distances == min(distances))][0])]
        else:
            return SOLID_BLOCKS_MC_MAPPING[tuple(colors[np.where(distances == min(distances))][0])]

    @commands.command(aliases=['mc'])
    async def minecraft(self, ctx, *, user: discord.Member = None):
        type = 'solid'  # all or solid
        async with ctx.typing():
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
            colors = np.array(list(eval(f'{type.upper()}_BLOCKS_MC_MAPPING.keys()')))

            with Image.new('RGBA', (img.width*16, img.height*16)) as result:
                for y in range(img.height):
                    for x in range(img.width):
                        color = np.array(img.getpixel((x, y)))
                        block_name = self.get_closest_block(color, colors, type)
                        result = result.convert('RGBA')
                        result.paste(Image.open('cogs\\utilityCommands\\solid_blocks\\{}'.format(block_name)), (x*16,y*16))

            with io.BytesIO() as image_binary:
                result.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.message.channel.send(file=discord.File(fp=image_binary, filename='minecraft.png'))

    @minecraft.error
    async def mc_error(self, ctx, error):
        print(__file__)
        raise error
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(
                description = 'Please attach an image or mention a user.'
            ).set_author(name = ctx.message.author.name, icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Minecraft(bot))
