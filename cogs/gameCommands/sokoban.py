from random import randint

import discord
from discord.ext import commands
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="discord_dev",
    password="81117556",
    database="discord"
)


class Sokoban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_coords(self, first, second, third):
        while True:
            if first == second or second == third or third == first:
                first = [randint(1, 6), randint(1, 6)]
                second = [randint(1, 6), randint(1, 6)]
                third = [randint(1, 6), randint(1, 6)]
            else:
                return first, second, third

    async def send_sokoban(self, user, result, amountwon=None):
        global embed
        description = """Play by reacting to the message.
                    You control the face.
                    Your objective is to push the box onto the green X and to go onto the green X.
                    \n"""
        for rows in SokobanGames.user_sokoban_megalist[user.id]:
            for emoji in rows:
                description += emoji
            description += '\n'
        if result == 'normal':
            embed = discord.Embed(
                #title='{}\'s sokoban game'.format(user.name),
                colour=discord.Colour.blue(),
                description=description
            )
            embed.set_author(name='{}\'s sokoban game'.format(user.name))
        if result == 'winner':
            embed = discord.Embed(
                #title='{}\'s sokoban game'.format(user),
                colour=discord.Colour.green(),
                description="""You won! Great job!
                You got **{}** coins.
                \nYou can play again with `bla sokoban start`.""".format(f"{int(amountwon):,d}")
            )
            embed.set_author(name='{}\'s sokoban game'.format(user.name))
        return embed
        # self.sokoban_msg = await ctx.message.channel.send(embed=embed)

    @commands.command()
    async def sokoban(self, ctx, *, command):
        if command == None:
            raise commands.BadArgument
        if command == 'start':
            if ctx.message.author.id not in SokobanGames.user_games:
                white = ':white_large_square:'
                brown = ':brown_square:'
                green = ':negative_squared_cross_mark:'
                row1 = [white, white, white, white, white, white]
                row2 = [white, white, white, white, white, white]
                row3 = [white, white, white, white, white, white]
                row4 = [white, white, white, white, white, white]
                row5 = [white, white, white, white, white, white]
                row6 = [white, white, white, white, white, white]
                megalist = [row1, row2, row3, row4, row5, row6]
                playercoords = [randint(1, 6), randint(1, 6)]
                boxcoords = [randint(1, 6), randint(1, 6)]
                wincoords = [randint(1, 6), randint(1, 6)]
                playercoords, boxcoords, wincoords = self.check_coords(playercoords, boxcoords,
                                                                                      wincoords)
                megalist[playercoords[0] - 1][playercoords[1] - 1] = ':flushed:'
                megalist[boxcoords[0] - 1][boxcoords[1] - 1] = brown
                megalist[wincoords[0] - 1][wincoords[1] - 1] = green

                # send initial game message
                if ctx.message.author.id not in SokobanGames.user_sokoban_megalist:
                    SokobanGames.user_sokoban_megalist[ctx.message.author.id] = megalist
                if ctx.message.author.id not in SokobanGames.user_playercoords:
                    SokobanGames.user_playercoords[ctx.message.author.id] = playercoords
                if ctx.message.author.id not in SokobanGames.user_boxcoords:
                    SokobanGames.user_boxcoords[ctx.message.author.id] = boxcoords
                if ctx.message.author.id not in SokobanGames.user_wincoords:
                    SokobanGames.user_wincoords[ctx.message.author.id] = wincoords
                #await SokobanGames().new_game(ctx.message.author.id, sokoban_msg, megalist, playercoords, boxcoords, wincoords)
                sokoban_msg = await ctx.message.channel.send(
                    embed=await self.send_sokoban(ctx.message.author, 'normal'))
                await sokoban_msg.add_reaction("⬆")
                await sokoban_msg.add_reaction("⬇")
                await sokoban_msg.add_reaction("⬅")
                await sokoban_msg.add_reaction("➡")
                if ctx.message.author.id not in SokobanGames.user_games:
                    SokobanGames.user_games[ctx.message.author.id] = sokoban_msg
            else:
                description = """You already have a sokoban game.
\nYou can finish the game or use `bla sokoban stop` to stop your game."""
                title = 'What are you thinking??'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    colour=discord.Colour.red()
                )
                await ctx.message.channel.send(embed=embed)
        elif command == 'stop':
            try:
                await SokobanGames.user_games[ctx.message.author.id].clear_reactions()
                SokobanGames.user_games[ctx.message.author.id] = await SokobanGames.user_games[
                    ctx.message.author.id].edit(embed=discord.Embed(
                    #title='{}\'s sokoban game'.format(ctx.message.author.name),
                    colour=discord.Colour.light_gray(),
                    description="""Sokoban game stopped."""
                ).set_author(name='{}\'s sokoban game'.format(ctx.message.author.name))
                )
                SokobanGames.user_games.pop(ctx.message.author.id)
                SokobanGames.user_playercoords.pop(ctx.message.author.id)
                SokobanGames.user_boxcoords.pop(ctx.message.author.id)
                SokobanGames.user_wincoords.pop(ctx.message.author.id)
                SokobanGames.user_sokoban_megalist.pop(ctx.message.author.id)
            except:
                description = """That doesn't work. You can't stop a game that doesn't exist.
                            \nYou can use `bla sokoban start` to start a game."""
                title = 'What are you thinking??'
                embed = discord.Embed(
                    title=title,
                    description=description,
                    colour=discord.Colour.red()
                )
                await ctx.message.channel.send(embed=embed)
        elif command == 'info' or command == 'information' or command == 'help':
            embed = discord.Embed(
                title='Sokoban',
                description = 'Sokoban is a popular box-pushing puzzle game.',
                colour = discord.Colour.blue()
            )
            embed.add_field(name='How to play', value="""You are a **sokoban :flushed:**.
            Your goal is to push **boxes :brown_square:** onto their **destinations :negative_squared_cross_mark:** and then go into the **destinations :negative_squared_cross_mark:**.""",
                            inline=False)
            embed.add_field(name='Features', value=""":white_small_square: **Randomly generated levels**
            Sokoban never gets boring because of the randomly generated levels.
            :white_small_square: **Easy-to-use controls**
            It's easy to play with reaction controls! Just hit the reaction and you will start playing.
            :white_small_square: **Simultaneous games**
            Multiple users can use the bot at the same time without interfering with each other!""")
            embed.add_field(name='Commands', value="""`bla sokoban start` can be used to start a game.
            `bla sokoban stop` can be used to stop your active game. (You can only have 1 at a time)
            `bla sokoban info` or `bla sokoban help` brings up this message.""")
            await ctx.message.channel.send(embed=embed)
        else:
            raise commands.BadArgument

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            if SokobanGames.user_games[user.id].id == reaction.message.id and user.id != 745010432464650408:
                # print("went here with user {}".format(user.name))
                megalist = SokobanGames.user_sokoban_megalist[user.id]
                playercoords = SokobanGames.user_playercoords[user.id]
                boxcoords = SokobanGames.user_boxcoords[user.id]
                wincoords = SokobanGames.user_wincoords[user.id]
                sokoban_msg = SokobanGames.user_games[user.id]
                if reaction.emoji == "⬆":
                    megalist[(playercoords[0] - 1) % 6][playercoords[1] - 1] = ':white_large_square:'
                    if megalist[(playercoords[0] - 2) % 6][playercoords[1] - 1] == ':brown_square:':
                        megalist[(playercoords[0] - 3) % 6][playercoords[1] - 1] = ':brown_square:'
                        SokobanGames.user_boxcoords[user.id] = [(playercoords[0] - 2) % 6, playercoords[1]]
                    megalist[(playercoords[0] - 2) % 6][playercoords[1] - 1] = ':flushed:'
                    SokobanGames.user_playercoords[user.id] = [(playercoords[0] - 1) % 6, playercoords[1]]
                    if playercoords != wincoords:
                        megalist[wincoords[0] - 1][wincoords[1] - 1] = ':negative_squared_cross_mark:'
                if reaction.emoji == "⬇":
                    megalist[(playercoords[0] - 1) % 6][playercoords[1] - 1] = ':white_large_square:'
                    if megalist[playercoords[0] % 6][playercoords[1] - 1] == ':brown_square:':
                        megalist[(playercoords[0] + 1) % 6][playercoords[1] - 1] = ':brown_square:'
                        SokobanGames.user_boxcoords[user.id] = [playercoords[0] + 2, playercoords[1]]
                    megalist[playercoords[0] % 6][playercoords[1] - 1] = ':flushed:'
                    SokobanGames.user_playercoords[user.id] = [(playercoords[0] + 1) % 6, playercoords[1]]
                    if playercoords != wincoords:
                        megalist[wincoords[0] - 1][wincoords[1] - 1] = ':negative_squared_cross_mark:'
                if reaction.emoji == "⬅":
                    megalist[playercoords[0] - 1][(playercoords[1] - 1) % 6] = ':white_large_square:'
                    if megalist[playercoords[0] - 1][(playercoords[1] - 2) % 6] == ':brown_square:':
                        megalist[playercoords[0] - 1][(playercoords[1] - 3) % 6] = ':brown_square:'
                        SokobanGames.user_boxcoords[user.id] = [playercoords[0], (playercoords[1] - 2) % 6]
                    megalist[playercoords[0] - 1][(playercoords[1] - 2) % 6] = ':flushed:'
                    SokobanGames.user_playercoords[user.id] = [playercoords[0], (playercoords[1] - 1) % 6]
                    if playercoords != wincoords:
                        megalist[wincoords[0] - 1][wincoords[1] - 1] = ':negative_squared_cross_mark:'
                if reaction.emoji == "➡":
                    megalist[playercoords[0] - 1][(playercoords[1] - 1) % 6] = ':white_large_square:'
                    if megalist[playercoords[0] - 1][(playercoords[1]) % 6] == ':brown_square:':
                        megalist[playercoords[0] - 1][(playercoords[1] + 1) % 6] = ':brown_square:'
                        SokobanGames.user_boxcoords[user.id] = [playercoords[0], playercoords[1] + 2]
                    megalist[playercoords[0] - 1][playercoords[1] % 6] = ':flushed:'
                    SokobanGames.user_playercoords[user.id] = [playercoords[0], (playercoords[1] + 1) % 6]
                    if playercoords != wincoords:
                        megalist[wincoords[0] - 1][wincoords[1] - 1] = ':negative_squared_cross_mark:'
                await sokoban_msg.remove_reaction(reaction, user)
                if boxcoords[0] % 6 == wincoords[0] % 6 and boxcoords[1] % 6 == wincoords[1] % 6:
                    await sokoban_msg.clear_reactions()
                    cursor = connection.cursor(buffered=True)
                    cursor.execute("SELECT * FROM discord_currency WHERE user_id={}".format(int(user.id)))
                    result1 = cursor.fetchone()
                    wallet = result1[1]
                    # total = result1[1]+result1[2]
                    if randint(1, 50) != 50:
                        newwallet = wallet + randint(5000, 10000)
                    else:
                        newwallet = wallet + randint(40000, 69420)
                    cursor.execute(
                        "UPDATE discord_currency SET wallet = {} WHERE user_id={}".format(newwallet,
                                                                                          int(user.id))
                    )
                    connection.commit()
                    cursor.close()
                    await sokoban_msg.edit(
                        embed=await self.send_sokoban(user, 'winner', newwallet - wallet))
                    SokobanGames.user_games.pop(user.id)
                    SokobanGames.user_playercoords.pop(user.id)
                    SokobanGames.user_boxcoords.pop(user.id)
                    SokobanGames.user_wincoords.pop(user.id)
                    SokobanGames.user_sokoban_megalist.pop(user.id)
                else:
                    await sokoban_msg.edit(embed=await self.send_sokoban(user, 'normal'))
        except KeyError:
            pass
            #if user.id != 745010432464650408:
                #if user.id in SokobanGames.user_games:
                    #description = """Imagine trying to hijack someone else's game.
                    #\nStart a game with `bla sokoban start`."""
                    #title = 'What are you thinking??'
                    #embed = discord.Embed(
                        #title=title,
                        #description=description,
                        #colour=discord.Colour.red()
                    #)
                    #await user.send(embed=embed)

    @sokoban.error
    async def sokoban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument) or isinstance(
                error, commands.CommandInvokeError):
            description = """That doesn't work. You need to provide a command.
            \nYou can use `bla sokoban start`, `bla sokoban stop`, or `bla sokoban info`."""
            title = 'What are you thinking??'
            embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.red()
            )
            await ctx.message.channel.send(embed=embed)
        else:
            raise error


class SokobanGames:
    user_games = {}
    user_sokoban_megalist = {}
    user_playercoords = {}
    user_boxcoords = {}
    user_wincoords = {}

    async def new_game(self, userid, sokoban_msg, megalist, playercoords, boxcoords, wincoords):
        if userid not in self.user_games:
            self.user_games[userid] = sokoban_msg
        if userid not in self.user_sokoban_megalist:
            self.user_sokoban_megalist[userid] = megalist
        if userid not in self.user_playercoords:
            self.user_playercoords[userid] = playercoords
        if userid not in self.user_boxcoords:
            self.user_boxcoords[userid] = boxcoords
        if userid not in self.user_wincoords:
            self.user_wincoords[userid] = wincoords


def setup(bot):
    bot.add_cog(Sokoban(bot))
