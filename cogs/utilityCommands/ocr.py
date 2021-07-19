import discord
import os
import pytesseract
import cv2
import numpy as np
from discord.ext import commands
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

class Ocr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image, 5)

    # dilation
    def dilate(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    @commands.command()
    async def ocr(self, ctx):
        async with ctx.typing():
            if ctx.message.attachments:
                img = Image.open(BytesIO(await ctx.message.attachments[0].read())).convert('RGBA')
                img = np.array(img)[:, :, ::-1].copy()
            gray = self.get_grayscale(img)
            text = pytesseract.image_to_string(gray, lang='eng')
            embed = discord.Embed(
                description=text,
                color=discord.Color.blurple()
            )
            is_text = False
            for char in 'abcdefghijklmnopqrstuvwxyz':
                if char in text.lower():
                    is_text = True
            if is_text:
                embed.set_author(name='Detected text', icon_url=ctx.message.author.avatar_url)
            else:
                embed.set_author(name='No text detected', icon_url=ctx.message.author.avatar_url)
            await ctx.message.channel.send(embed=embed)

    @ocr.error
    async def ocr_error(self, ctx, error):
        raise error
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            embed = discord.Embed(
                description='You need to attach an image.'
            ).set_author(name=ctx.message.author.name, icon_url=ctx.author.avatar_url)
            await ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Ocr(bot))