from random import randint

import discord
import mysql.connector
from discord.ext import commands

connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Gamble(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['gamble'])
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def bet(self, ctx, amount=None):
        connection.commit()
        if amount == None:
            return
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
        myresult = cursor.fetchone()
        wallet = int(myresult[1])
        if amount == 'all' or amount == 'max':
            amount = int(wallet)
        try:
            amount = int(amount)
            cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
            result = cursor.fetchone()
            cursor.close()
            wallet = int(result[1])
            if amount and int(amount) <= wallet and int(amount) > 0:
                global embed, description
                mydice = randint(1, 12)
                botdice = randint(1, 12)
                if mydice == botdice:
                    amountlost = round(int(amount) / 4)
                    resultcursor = connection.cursor()
                    resultcursor.execute(
                        "SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
                    myres = resultcursor.fetchone()
                    result1 = myres
                    result2 = int(result1[1]) - round(amountlost)
                    resultcursor.execute(
                        "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(result2,
                                                                                          int(ctx.message.author.id))
                    )
                    resultcursor.close()
                    description = """Tie! You lost **{}** coins.
                    \nYou now have **{}** coins.""".format(f"{amountlost:,d}", f"{result2:,d}")
                    embed = discord.Embed(
                        #title='{}\'s gambling game'.format(ctx.message.author.name),
                        color=discord.Colour.gold(),
                        description=description
                    )
                    embed.set_author(name='{}\'s gambling game'.format(ctx.message.author.name))
                if mydice >= botdice:
                    winnings = randint(round(int(amount)*0.4), round(int(amount)*1.7))
                    percentwon = round(winnings/int(amount)*100)
                    resultcursor = connection.cursor()
                    resultcursor.execute(
                        "SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
                    myres = resultcursor.fetchone()
                    result1 = myres
                    result2 = int(result1[1]) + round(winnings)
                    resultcursor.execute(
                        "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(result2,
                                                                                          int(ctx.message.author.id))
                    )
                    resultcursor.close()
                    description = """You won **{}** coins.
                    **Percent of bet won** {}%
                    \nYou now have **{}** coins.""".format(f"{round(winnings):,d}", percentwon, f"{int(result2):,d}")
                    embed = discord.Embed(
                        #title='{}\'s gambling game'.format(ctx.message.author.name),
                        colour=discord.Colour.green(),
                        description=description
                    )
                    embed.set_author(name='{}\'s gambling game'.format(ctx.message.author.name))
                if mydice <= botdice:
                    resultcursor = connection.cursor()
                    resultcursor.execute(
                        "SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
                    myres = resultcursor.fetchone()
                    result1 = myres
                    result2 = int(result1[1]) - round(int(amount))
                    resultcursor.execute(
                        "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(result2,
                                                                                          int(ctx.message.author.id))
                    )
                    resultcursor.close()
                    description = """You lost **{}** coins.
                    \nYou now have **{}** coins.""".format(f"{int(amount):,d}", f"{int(result2):,d}")
                    embed = discord.Embed(
                        #title='{}\'s gambling game'.format(ctx.message.author.name),
                        colour=discord.Colour.red(),
                        description=description
                    )
                    embed.set_author(name='{}\'s gambling game'.format(ctx.message.author.name))
                connection.commit()
                embed.add_field(name=ctx.message.author.name, value=f"Rolled `{mydice}`")
                embed.add_field(name="blablabot", value=f"Rolled `{botdice}`")
                await ctx.message.channel.send(embed=embed)
                return
            elif amount > wallet:
                description = 'You can\'t bet more than what\'s in your wallet.'
            elif amount < 0:
                description = 'Don\'t try to bet a negative number.'
            elif amount == 0:
                description = 'What\'s the point of betting nothing?'
            else:
                description = 'Something went wrong. Please try again.'
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
        except ValueError:
            description = 'You have to bet a whole number of coins greater than 0.'
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """You'll lose a lot more coins if you keep betting this fast.
            You can bet again in **{:.0f} seconds**
            (trust me, this is for your own good)
            \nDefault cooldown: `8 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='You\'re getting dangerously addicted',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Gamble(bot))