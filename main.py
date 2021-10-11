import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
#import database

load_dotenv('config.env')
botintents = discord.Intents()
botintents.guilds=True
botintents.reactions=True

"""
def get_prefix(bot, message): ##first we define get_prefix
    results= database.getprefix()
    for i in results:
        if message.guild.id in i:
            return i[1]
    return '.'
"""

bot = commands.Bot(command_prefix='.', help_command=None)

extentions = ["cogs.reactions","cogs.packs","cogs.help"]

class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.creator = 249901932548849664

    @commands.Cog.listener()
    async def on_connect(self):
        print("Connected")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online,activity=discord.Game(name=".help"))
        for i in extentions:
            self.bot.load_extension(i)
            print(i + " loaded")
        print("Ready")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        #database.insertIntoDatabase(guild.id,'.')
        print(f"Joined {guild.name}")
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        #database.deleteFromDatabase(guild.id)
        print(f"Left {guild.name}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")


bot.add_cog(Startup(bot=bot))

TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
