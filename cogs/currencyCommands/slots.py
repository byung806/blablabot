from random import choice, randint
from datetime import datetime
import discord
import mysql.connector
from discord.ext import commands

connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Slots(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def get_winnings_and_percent(self, amountbet, winemoji, howmany):
        global winnings, percent
        global multi
        if winemoji == ':fire:' or winemoji == ':jack_o_lantern:' or winemoji == ':gift:':
            if howmany == 2:
                multi = 4.4
            if howmany == 3:
                multi = 5.6
        elif winemoji == ':star:' or winemoji == ':trophy:':
            if howmany == 2:
                multi = 3.4
            if howmany == 3:
                multi = 4.0
        elif winemoji == ':flushed:' or winemoji == ':poop:' or winemoji == ':scream:':
            if howmany == 2:
                multi = 2.8
            if howmany == 3:
                multi = 3.1
        else:
            if howmany == 2:
                multi = 2.3
            if howmany == 3:
                multi = 2.8
        winnings = randint(round(int(amountbet) * (multi-0.2)), round(int(amountbet) * (multi+0.2)))
        percent = winnings/amountbet*100
        return winnings, percent

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slots(self, ctx, amount=None):
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
                global embed, description, winnings, percentwon
                emojis = [':flushed:', ':scream:', ':clown:', ':poop:', ':fire:', ':star:', ':trophy:']
                halloween_emojis = [':jack_o_lantern:', ':ghost:', ':pie:', ':coffin:', ':skull:']
                christmas_emojis = [':christmas_tree:', ':santa:', ':gift:', ':snowflake:', ':snowman:', ':deer:']
                month = datetime.now().month
                if month == 10:
                    emojis.extend(halloween_emojis)
                if month == 12:
                    emojis.extend(christmas_emojis)
                spin1 = choice(emojis)
                spin2 = choice(emojis)
                spin3 = choice(emojis)
                if spin1 == spin2 or spin2 == spin3 or spin3 == spin1:
                    #win
                    if spin1 == spin2 == spin3:
                        winnings, percentwon = await self.get_winnings_and_percent(amount, spin1, 3)
                    elif spin1 == spin2:
                        winnings, percentwon = await self.get_winnings_and_percent(amount, spin1, 2)
                    elif spin2 == spin3:
                        winnings, percentwon = await self.get_winnings_and_percent(amount, spin2, 2)
                    elif spin3 == spin1:
                        winnings, percentwon = await self.get_winnings_and_percent(amount, spin3, 2)
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
                                        \nYou now have **{}** coins.
                                        \n**Outcome**
                                        **\> {} {} {} <**""".format(f"{round(winnings):,d}", round(percentwon),
                                                                               f"{int(result2):,d}", spin1, spin2, spin3)
                    embed = discord.Embed(
                        #title='{}\'s slot machine'.format(ctx.message.author.name),
                        colour=discord.Colour.green(),
                        description=description
                    )
                    embed.set_author(name='{}\'s slot machine'.format(ctx.message.author.name))
                else:
                    # lose
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
                                        \nYou now have **{}** coins.
                                        \n**Outcome**
                                        **\> {} {} {} <**""".format(f"{int(amount):,d}",
                                                                               f"{int(result2):,d}", spin1, spin2, spin3)
                    embed = discord.Embed(
                        #title='{}\'s slots machine'.format(ctx.message.author.name),
                        colour=discord.Colour.red(),
                        description=description
                    )
                    embed.set_author(name='{}\'s slot machine'.format(ctx.message.author.name))
                connection.commit()
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

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """The slot machine will break if you keep losing money this fast.
            You can bet again in **{:.0f} seconds**
            (trust me, this is for your own good)
            \nDefault cooldown: `2 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='You\'re getting dangerously addicted',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Slots(bot))