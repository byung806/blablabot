import discord
from datetime import datetime
from random import randint
from random import choice
from discord.ext import commands

class Halloween(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def halloween(self, ctx):
        global description
        month = datetime.now().month
        if month != 10:
            description = """It\'s not spooky enough yet!
            \n`bla halloween` only works in October."""
            embed = discord.Embed(
                title='In your dreams...',
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
            return
        num = randint(1,5)
        if num == 1 or num == 2:
            if randint(1,3) == 1:
                description = 'Here\'s a pumpkin.'
            else:
                description = 'PUMPKIN!!'
            description += """​\n```
          ___
       ___)__|_
  .-*'          '*-,
 /      /|   |\     \\
;      /_|   |_\     ;
;   |\           /|  ;
;   | ''--...--'' |  ;
 \  ''---.....--''  /
  ''*-.,_______,.-*'  ```"""
        elif num == 3 or num == 4:
            if randint(1,3) == 1:
                description = 'Ghosts are very scaryyyy...'
            else:
                description = 'AHH A GHOST!'
            description += """​\n```
      .'``'.      ...
     :o  o `....'`  ;
     `. O         :'
       `':          `.
         `:.          `.
          : `.         `.
         `..'`...       `.
                 `...     `.
                     ``...  `.
                          ` ` `.
```"""
        elif num == 5:
            if randint(1,3) == 1:
                description = 'Stay away from the witch...'
            else:
                description = 'Look up!'
            description += """​\n```
                  /\\
                _/__\_
                /( o\\
           /|  // \-'
      __  ( o,    /\\
        ) / |    / _\\
 >>>>==(_(__u---(___ )-----
                   //
                  /__)```"""
        title = "Spookyyyy!"
        colors = [discord.Colour.orange(), discord.Colour.dark_grey(), discord.Colour.dark_green()]
        embed = discord.Embed(
            title=title,
            description=description,
            colour=choice(colors)
        )
        await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Halloween(bot))