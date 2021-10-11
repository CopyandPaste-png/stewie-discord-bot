import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx:commands.Context):
        """A custom help command

        Parameters
        _________
        None

        NB:
        a @commands.group() decorator is required to make this custom help command work.
        Basically it allows for subcommands(@helpfor.command()) to be called and invoked through
        $helpfor <command_name>, similar to how the default help command works.
        """

        # guild_prefix queries the database (main.GUILDS) to get the prefix for the guild
        pf = "."
        em = discord.Embed(title="COMMANDS")

        
        em.add_field(name=f"{pf}search <term>", value="Finds a pack", inline=False)
        em.add_field(name=f"{pf}add <name> <code>", value="Adds pack", inline=False)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(HelpCommand(bot))
