import discord
from discord.ext import commands
from utils import get_embed_color, send_embed

from utils import get_server_prefix


class Help(commands.Cog):
    '''
    The bot's help command.
    Usage:
    `<prefix> help`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *, command=None):
        prefix = await get_server_prefix(self.bot, ctx)
        version = '1.0'
        if not command:
            emb = discord.Embed(
                title='Blablabot Command List', color=discord.Color.blue(),
                description=f'**Prefix: {await get_server_prefix(self.bot, ctx)}**\n'
                            f'Use `{prefix}help <command>` to see specific information about a command.',
                colour=await get_embed_color(ctx.author.id)
            )
            for cog in self.bot.cogs:
                if self.bot.cogs[cog].__doc__:
                    emb.add_field(name=cog, value=self.bot.cogs[cog].__doc__.split('\n')[1].strip())
                else:
                    emb.add_field(name=cog, value='No description')
        else:
            for cog in self.bot.cogs:
                if command.lower() == cog.lower() or command in self.bot.get_command(cog.lower()).aliases:
                    full_desc = '\n'.join(
                        [x.strip() for x in (self.bot.cogs[cog].__doc__.split('Usage:')[0].strip().split('\n'))])
                    usage = '\n'.join([x.strip() for x in
                                       (self.bot.cogs[cog].__doc__.strip().split('Usage:')[1].strip().split('\n'))])
                    aliases = ', '.join([f'`{x}`' for x in self.bot.get_command(cog.lower()).aliases])
                    emb = discord.Embed(
                        title=f'{cog} - Command',
                        description=full_desc,
                        colour=await get_embed_color(ctx.author.id)
                    )
                    emb.add_field(name='Usage', value=usage, inline=False)
                    emb.add_field(name='Aliases', value=aliases if aliases else 'None', inline=False)
                    break
            else:
                emb = await send_embed(ctx, 'Command not found', f'No command named `{command}`.', send=False)
        emb.set_footer(text=f'{len(self.bot.cogs)} commands • blablabot is running version {version}')
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))
