import discord
from discord.ext import commands
import mysql.connector
connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Balance(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['bal', 'coins'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def balance(self, ctx, *, member: discord.Member = None):
        connection.commit()
        if not member:
            member = ctx.message.author
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(member.id)))
        result = cursor.fetchone()
        #print(result)
        #await ctx.message.channel.send(result)
        cursor.close()
        wallet = int(result[1])
        bank = int(result[2])
        embed = discord.Embed(
            #title='{}\'s balance'.format(member.name),
            colour=discord.Colour.dark_blue(),
            description="""**Wallet:** {}
            **Bank:** {}
            **Total:** {}""".format(f"{wallet:,d}", f"{bank:,d}", f"{wallet+bank:,d}")
        )
        embed.set_author(name='{}\'s balance'.format(member.name))
        await ctx.message.channel.send(embed=embed)

    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """Why are you checking your balance so much? Are you really that forgetful?
            You can check your balance again in **{:.0f} seconds**
            \nDefault cooldown: `2 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='Your tiny arms are getting tired from checking your wallet and bank',
                colour=discord.Colour.blue(),
                description=description
            )
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            description = """The user was not found."""
            embed = discord.Embed(
                title='Who are you trying to check the balance of?',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Balance(bot))