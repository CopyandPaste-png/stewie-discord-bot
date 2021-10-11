from discord.ext import commands
import discord
from discord.utils import get
from file import readFromFileLines,writeToFile

class Reaction(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.filename="reactions.txt"
        self.rolesToEmoji = {
            "🎯":"NA",
            "⚽":"EU",
            "🏑":"RSA",
            "🌊":"OCE",
            "<:GC:892931611681783858>":"grand champ",
            "<:champ3:893065042059231264>":'champion',
            "<:diamond3:893065041266495488>":"diamond",
            "<:plat3:893065078528700416>":"plat",
            "<:gold3:893065539080056852>":"gold",
            "<:bronze3:893065041530740756>":"bronze",
            "<:silver3:893065078394474506>":"silver"
        }
    

    @commands.is_owner()
    @commands.command(aliases=["rolesReset"])
    async def _reset(self,ctx:commands.Context, rankID,regionID):
        writeToFile(self.filename,f"{ctx.channel.id}\n{rankID}:{regionID}")

    @commands.command(aliases=["setup"])
    async def _setup(self, ctx:commands.Context):
        """
        Okay
        """
        regionString = """
        🎯-NA
        ⚽-EU
        🏑-RSA 
        🌊-OCE"""
        embed= discord.Embed(title="Region", color=0x4CFE21)
        embed.add_field(name="React to this message to set your region", value=regionString)
        
        region = await ctx.send(embed=embed)

        message =await ctx.fetch_message(region.id)
        
        await message.add_reaction("🎯")
        await message.add_reaction("⚽")
        await message.add_reaction("🏑")
        await message.add_reaction("🌊")

        rankString = f"""
        If you are Supersonic legend- use /ranks in #bot-commands and a mod will assign your role.
        {get(ctx.guild.emojis, name="GC")}-Grand champ
        {get(ctx.guild.emojis, name="champ3")}-Champion
        {get(ctx.guild.emojis, name="diamond3")}-Diamond
        {get(ctx.guild.emojis, name="plat3")}-Platinum
        {get(ctx.guild.emojis, name="gold3")}-Gold
        {get(ctx.guild.emojis, name="silver3")}-Silver
        {get(ctx.guild.emojis, name="bronze3")}-Bronze
        """
        embed= discord.Embed(title="Rank", color=0x4CFE21)
        embed.add_field(name="React to this message to set your rank", value=rankString)
    
        rank = await ctx.send(embed=embed)

        message =await ctx.fetch_message(rank.id)
        
        await message.add_reaction(get(ctx.guild.emojis, name="GC"))
        await message.add_reaction(get(ctx.guild.emojis, name="champ3"))
        await message.add_reaction(get(ctx.guild.emojis, name="diamond3"))
        await message.add_reaction(get(ctx.guild.emojis, name="plat3"))
        await message.add_reaction(get(ctx.guild.emojis, name="gold3"))
        await message.add_reaction(get(ctx.guild.emojis, name="silver3"))
        await message.add_reaction(get(ctx.guild.emojis, name="bronze3"))
        writeToFile(self.filename,f"{ctx.channel.id}\n{rank.id}:{region.id}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        data = readFromFileLines(self.filename)
        try:
            channel = int(data[0])
        except IndexError as e:
            return
            
        messageIDs=[int(i) for i in data[1].split(":")]

        if payload.channel_id == channel and payload.message_id in messageIDs:
            if str(payload.emoji) in self.rolesToEmoji.keys():
                guild= self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.rolesToEmoji[str(payload.emoji)])
                await payload.member.add_roles(role) 
                
                channel = get(guild.channels,name="bot-logs")
                await channel.send(f"{payload.member.display_name} added the role of {self.rolesToEmoji[str(payload.emoji)]}")
            
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):

        data = readFromFileLines(self.filename)
        try:
            channel = int(data[0])
        except IndexError as e:
            return
        messageIDs=[int(i) for i in data[1].split(":")]

        if payload.channel_id == channel and payload.message_id in messageIDs:
            if str(payload.emoji) in self.rolesToEmoji.keys():
                guild= self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.rolesToEmoji[str(payload.emoji)])
                member= await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

                channel = get(guild.channels,name="bot-logs")
                await channel.send(f"{member.display_name} removed the role of {self.rolesToEmoji[str(payload.emoji)]}")


def setup(bot):
    bot.add_cog(Reaction(bot))
