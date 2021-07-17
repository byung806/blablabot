from random import randint
from datetime import datetime
import discord
from discord.ext import commands
import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Beg(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        names = ['Mr. Beast', 'blablabot', 'blabla', 'Donald Trump', 'Michael Jordan', 'Justin Bieber', 'Some random person you met 2 days ago', 'Jason Citron', 'Elon Musk', 'Jeff Bezos', 'Bill Gates', 'Steve Jobs', 'Thanos', 'Shrek', 'Rick Astley']
        no_coins = [
            'I\'m saving money for the all new Third Generation iPhone 14 XS R V A J R e T Max Pro 2 Plus Plus Air Lite Series 7 with 128 cameras - you get nothing!',
            'Too bad, you get NOTHING.',
            'Imagine not even finding a place to beg',
            'Sorry, I don\'t have any spare coins :(',
            'Maybe ask me later, I\'m busy right now.',
            'ewwwww get away from me!'
        ]
        halloween_no_coins = [
            'I\'m saving money for candy!',
            'I spent all my money on a Halloween party, sorry.'
        ]
        month = datetime.now().month
        if month == 10:
            no_coins.extend(halloween_no_coins)
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
        result1 = cursor.fetchone()
        myres = result1
        #totalbal = result1[2] + result1[3]
        a = randint(50, 500)
        """if round(totalbal / 100) > 69420:
            a = randint(69000, 69840)
        else:
            if round(totalbal / 100 - 250) <= 0:
                a = randint(500, 1000)
            else:
                a = randint(round(totalbal / 100 - 250), round(totalbal / 100 + 250))"""
        if randint(1, 5) <= 2:
            await ctx.channel.send("**{}:** {}".format(names[randint(0,len(names)-1)], no_coins[randint(0,len(no_coins)-1)]) )
        else:
            money = a
            message = "**{}** has donated {} coins to {}".format(names[randint(0,len(names)-1)], f"{int(money):,d}", ctx.message.author.mention)
            item_chance = randint(1, 100)
            if item_chance <= 10:
                message += " and a piece of bread! :bread:"
                cursor.execute("SELECT * FROM discord_inventory WHERE user_id={}".format(int(ctx.message.author.id)))
                invresult = cursor.fetchone()
                bread = invresult[1]
                bread += 1
                cursor.execute(
                    "UPDATE discord_inventory SET bread = {} WHERE user_id={}".format(bread,
                                                                                      int(ctx.message.author.id))
                )
                connection.commit()
            else:
                message += "!"
            await ctx.message.channel.send(message)
            #cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
            result1 = myres
            result2 = int(result1[1]) + money
            cursor.execute(
                "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(result2, int(ctx.message.author.id))
            )
            connection.commit()
            cursor.close()

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """Stop begging so much.
            You can beg again in **{:.0f} seconds**
            \nDefault cooldown: `20 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='What are you thinking??',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Beg(bot))