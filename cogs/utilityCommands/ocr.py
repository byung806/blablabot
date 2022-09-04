import discord
import os
import pytesseract
import cv2
import numpy as np
from discord.ext import commands
from PIL import Image
from io import BytesIO

from utils import send_embed


class Ocr(commands.Cog):
    '''
    Get text from an image!
    Usage:
    `<prefix> ocr <image>`
    '''
    def __init__(self, bot):
        self.bot = bot

    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @commands.command()
    @commands.guild_only()
    async def ocr(self, ctx, *, content=None):
        async with ctx.typing():
            pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
            if ctx.message.attachments:
                img = Image.open(BytesIO(await ctx.message.attachments[0].read())).convert('RGBA')
                img = np.array(img)[:, :, ::-1].copy()
            gray = self.get_grayscale(img)
            try:
                text = pytesseract.image_to_string(gray, lang='eng')
            except Exception:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
                text = pytesseract.image_to_string(gray, lang='eng')
            embed = discord.Embed(
                description=text,
                color=discord.Color.blurple()
            )
            for char in 'abcdefghijklmnopqrstuvwxyz':
                if char in text.lower():
                    embed.set_author(name='Detected text', icon_url=ctx.author.avatar_url)
                    break
            else:
                embed.set_author(name='No text detected', icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)

    @ocr.error
    async def ocr_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await send_embed(ctx, 'No image', 'You need to attach an image.')
        else:
            raise error

def setup(bot):
    bot.add_cog(Ocr(bot))