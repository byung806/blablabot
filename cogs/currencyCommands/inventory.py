import discord
from discord.ext import commands
import mysql.connector
connection = mysql.connector.connect(
    host = "localhost",
    user = "discord_dev",
    password = "81117556",
    database = "discord"
)

class Inventory(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['inv', 'items'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def inventory(self, ctx, *, member: discord.Member = None):
        connection.commit()
        itemnames = ['Bread', 'Diamond', 'Emerald', 'Ruby', 'Sapphire', 'Stone']
        itemicons = [':bread:', '<:diamond:763841763571925042>', '<:emerald:763840788508835900>', '<:ruby:763841098140614737>', '<:sapphire:763841773066780702>', '<:stone:763843326230659073>']
        itemids = ['bread', 'diamond', 'emerald', 'ruby', 'sapphire', 'stone']
        # CAUTION WHEN CHANGING ORDER CHANGE MINE.PY AND BEG.PY
        if not member:
            member = ctx.message.author
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM discord_inventory WHERE user_id={}".format(int(member.id)))
        items = cursor.fetchone()
        cursor.close()
        description = """**Owned Items**"""
        embed = discord.Embed(
            #title='{}\'s inventory'.format(member.name),
            colour=discord.Colour.dark_blue(),
            description=description
        )
        embed.set_author(name='{}\'s inventory'.format(member.name))
        #for item_amount in items:
        #    embed.add_field(name='**item**', value=item_amount, inline=False)
        make_embed = False
        for i in range(len(items)-1):
            item_name = itemnames[i]
            item_icon = itemicons[i]
            item_amount = items[i+1]
            item_id = itemids[i]
            if item_amount > 0:
                embed.add_field(name=f'{item_icon}  **{item_name}** — {item_amount}', value=f'*ID* `{item_id}`', inline=False)
                make_embed = True
        if make_embed == False:
            embed.add_field(name='Nothing here, imagine being so poor you don\'t have any items', value='hahaha')
            embed.colour = discord.Colour.red()
        await ctx.message.channel.send(embed=embed)

    @inventory.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            description = """Why are you checking your inventory so much? Are you really that forgetful?
            You can check your inventory again in **{:.0f} seconds**
            \nDefault cooldown: `2 seconds`""".format(error.retry_after)
            embed = discord.Embed(
                title='Your eyes are getting tired looking through your inventory',
                colour=discord.Colour.blue(),
                description=description
            )
            await ctx.send(embed=embed)
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            description = """The user was not found."""
            embed = discord.Embed(
                title='Who are you trying to check the inventory of?',
                colour=discord.Colour.red(),
                description=description
            )
            await ctx.send(embed=embed)
        else:
            raise error

def setup(bot):
    bot.add_cog(Inventory(bot))