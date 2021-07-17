import discord
import bot
from random import randint
from random import choice
from discord.ext import commands
import mysql.connector

connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)


class Mine(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def mine(self, ctx):
        global result
        message = ''
        stoneamount = randint(1,4)
        diamondamount = 0
        emeraldamount = 0
        rubyamount = 0
        sapphireamount = 0
        starting_messages = [
            '{} almost tripped and died but got **{} stone** <:stone:763843326230659073>',
            '{} almost got crushed by a stalactite but got out of there with **{} stone** <:stone:763843326230659073>',
            '{} found **{} stone** <:stone:763843326230659073>',
            '{} dug to the center of the Earth and found **{} stone** <:stone:763843326230659073>'
        ]
        death_messages = [
            '{} fell onto a stalagmite and died.',
            '{} dropped into lava and dissolved.',
            '{} was eaten.',
            '{} almost got out, but fell into a crevice and died.'
        ]
        if randint(1,69) != 1:
            mine_num = randint(1, 69)
            message = choice(starting_messages).format(ctx.message.author.mention, stoneamount)
            if mine_num == 42:
                diamondamount = 1
                message += ' and a **diamond**! <:diamond:763841763571925042>'
            elif mine_num == 69 or mine_num == 68 or mine_num == 67:
                emeraldamount = 1
                message += ' and an **emerald**! <:emerald:763840788508835900>'
            elif mine_num in range(60, 67):
                rubyamount = 1
                message += ' and a **ruby**! <:ruby:763841098140614737>'
            elif mine_num in range(50, 60):
                sapphireamount = 1
                message += ' and a **sapphire**! <:sapphire:763841773066780702>'
            else:
                message += '.'
        else:
            minedeath = bot.Death()
            await minedeath.death(ctx.message.author)
            message += choice(death_messages).format(ctx.message.author.mention)
            await ctx.message.channel.send(message)
            return
        await ctx.message.channel.send(message)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM discord_inventory WHERE user_id={}".format(int(ctx.message.author.id)))
        inventory_amounts = cursor.fetchone()
        currentdiamond = inventory_amounts[2]
        currentemerald = inventory_amounts[3]
        currentruby = inventory_amounts[4]
        currentsapphire = inventory_amounts[5]
        currentstone = inventory_amounts[6]

        currentdiamond += diamondamount
        currentemerald += emeraldamount
        currentruby += rubyamount
        currentsapphire += sapphireamount
        currentstone += stoneamount
        cursor.execute(
            "UPDATE discord_inventory SET diamond = {} WHERE user_id={}".format(currentdiamond,
                                                                              int(ctx.message.author.id))
        )
        cursor.execute(
            "UPDATE discord_inventory SET emerald = {} WHERE user_id={}".format(currentemerald,
                                                                                int(ctx.message.author.id))
        )
        cursor.execute(
            "UPDATE discord_inventory SET ruby = {} WHERE user_id={}".format(currentruby,
                                                                                int(ctx.message.author.id))
        )
        cursor.execute(
            "UPDATE discord_inventory SET sapphire = {} WHERE user_id={}".format(currentsapphire,
                                                                                int(ctx.message.author.id))
        )
        cursor.execute(
            "UPDATE discord_inventory SET stone = {} WHERE user_id={}".format(currentstone,
                                                                                int(ctx.message.author.id))
        )
        connection.commit()
        cursor.close()

    @mine.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """Stop mining so much.
                You can mine in **{:.0f} seconds**
                \nDefault cooldown: `15 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='What are you thinking??',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.channel.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Mine(bot))