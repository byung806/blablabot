import discord
from discord.ext import commands
import mysql.connector
connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Give(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def give(self, ctx, member: discord.Member, amount):
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(ctx.message.author.id)))
        result1 = cursor.fetchone()
        mywallet = result1[1]
        if amount == 'all' or amount == 'max':
            amount = int(mywallet)
        amount=int(amount)
        if amount > mywallet or amount <= 0:
            raise ValueError
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(member.id)))
        result2 = cursor.fetchone()
        theirwallet = result2[1]
        mynewwallet = mywallet-amount
        theirnewwallet = theirwallet+amount
        cursor.execute(
            "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(mynewwallet, int(ctx.message.author.id))
        )
        cursor.execute(
            "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(theirnewwallet, int(member.id))
        )
        connection.commit()
        description = """You gave {} **{}** coins.""".format(member.name, amount)
        embed = discord.Embed(
            #description=description,
            colour=discord.Colour.green()
        ).set_author(name="""You gave {} {} coins.""".format(member.name, f"{int(amount):,d}"))
        await ctx.message.channel.send(embed=embed)

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, ValueError) or isinstance(error, commands.BadArgument):
            description = """That doesn't work.
            \nGive people coins with `bla give [user] [amount]`."""
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
    bot.add_cog(Give(bot))