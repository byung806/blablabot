import discord
from discord.ext import commands
import mysql.connector
connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Deposit(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='deposit',aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        cursor = connection.cursor(buffered = True)
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
        myresult = cursor.fetchone()
        print(myresult)
        cursor.close()
        wallet = int(myresult[1])
        bank = int(myresult[2])
        if amount:
            if amount.lower() == 'all' or amount.lower() == 'max':
                amount = wallet
            depamount = int(amount)
            if depamount > wallet or depamount < 0:
                raise ValueError
            else:
                depcursor = connection.cursor()
                newwallet = int(wallet) - depamount
                newbank = int(bank) + depamount
                depcursor.execute(
                    "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(newwallet,
                                                                                      int(
                                                                                          ctx.message.author.id))
                )
                depcursor.execute(
                    "UPDATE discord_currency SET bank = {} WHERE user_id={}".format(newbank,
                                                                                    int(ctx.message.author.id))
                )
                depcursor.close()
                connection.commit()
                await ctx.message.channel.send('**{}** coins deposited.'.format(f"{int(depamount):,d}"))
        else:
            raise commands.BadArgument

    @deposit.error
    async def dep_error(self, ctx, error):
        if isinstance(error, ValueError) or isinstance(error, commands.BadArgument) or isinstance(error, commands.CommandInvokeError):
            description = """That doesn't work. You need to deposit an amount within your wallet.
            \nDeposit coins with `bla dep [amount]`."""
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
    bot.add_cog(Deposit(bot))