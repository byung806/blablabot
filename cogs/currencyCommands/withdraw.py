import discord
from discord.ext import commands
import mysql.connector
connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Withdraw(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='withdraw', aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
        myresult = cursor.fetchone()
        cursor.close()
        wallet = int(myresult[1])
        bank = int(myresult[2])
        if amount:
            if amount.lower() == 'all' or amount.lower() == 'max':
                amount = bank
            withamount = int(amount)
            if withamount > bank:
                raise ValueError
            else:
                withcursor = connection.cursor()
                newwallet = int(wallet) + withamount
                newbank = int(bank) - withamount
                withcursor.execute(
                    "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(newwallet,
                                                                                      int(
                                                                                          ctx.message.author.id))
                )
                withcursor.execute(
                    "UPDATE discord_currency SET bank = {} WHERE user_id={}".format(newbank,
                                                                                    int(ctx.message.author.id))
                )
                withcursor.close()
                connection.commit()
                await ctx.message.channel.send('**{}** coins withdrawn.'.format(f"{int(withamount):,d}"))
        else:
            raise commands.BadArgument

    @withdraw.error
    async def with_error(self, ctx, error):
        if isinstance(error, ValueError) or isinstance(error, commands.BadArgument) or isinstance(error,
                                                                                                  commands.CommandInvokeError):
            description = """That doesn't work. You need to withdraw an amount within your bank.
                \nDeposit coins with `bla with [amount]`."""
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Withdraw(bot))