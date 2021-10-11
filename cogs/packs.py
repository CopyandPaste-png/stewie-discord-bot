from discord.ext import commands
import discord
from discord.ext.commands.core import command
import requests
import os
import asyncio
import math
from discord.utils import get

created = {

}

class Packs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["all"])
    async def _helppacks(self, ctx:commands.Context):
        embed =discord.Embed(title="Packs", colour=0xa714ba)
        embed.add_field(name=".dpack",value="download packs.txt",inline=True)
        embed.add_field(name=".dbackup",value="downloads backup.txt",inline=True)
        embed.add_field(name=".drestore",value="downloads restore.txt",inline=True)
        embed.add_field(name=".epack",value="edits packs.txt file. Upload file which overrides current packs.txt",inline=True)
        embed.add_field(name=".cbackup",value="creates backup.txt and backs up to it",inline=True)
        embed.add_field(name=".crestore",value="creates restore.txt and backs up to it",inline=True)
        embed.add_field(name=".restore",value="overrides packs.txt content with restore.txt content",inline=True)
        embed.add_field(name=".backup",value="overrides packs.txt content with backup.txt content",inline=True)
        embed.add_field(name=".dall",value="Downloads all files",inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["add"])
    async def _addPack(self, ctx:commands.Context,name:str,code:str, author=""):
        
        if len(name)<1:
            await ctx.send("Name too short")
            return
        elif len(code)!=19 or code.count("-")!=3:
            await ctx.send("Invalid code")
            return
        

        with open("packs.txt","a") as f:
            f.write(name.replace("_"," ")+":"+ code+":"+author.replace("_"," ")+"\n")
            await ctx.send("Pack inserted!")

    @commands.command()
    async def pages(self,ctx):
        
        contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
        pages = 4
        cur_page = 1
        message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
        # getting the message object for editing and reacting

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        if ctx.author.id in created.keys():
            msg = ctx.fetch_message(created[ctx.author.id])
            del created[ctx.author.id]
            await msg.delete()

        created[ctx.author.id]=message.id
        
        print(created)
            
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds

    async def createEmbed(self,ctx, names,fields):
        pass

    @commands.command(aliases=["getpackname","search"])
    async def _getPackName(self, ctx:commands.Context,*args):
        name = " ".join(args)
        
        with open("packs.txt","r") as f:
            data = f.readlines()
        
        names=[]
        fields=[]

        for i in data:
            end = i[i.rfind(":")+1:-1]

            start=i.find(":")
            if name.lower() in i[0:start].lower():
  
                if end !="":
                    names.append(i[0:start]+":"+end)
                    fields.append(i[start+1:i.find(":",start+1)])
                else:
                    names.append(i[0:start])
                    fields.append(i.find(":",start+1))

        
        
        
        customEmbeds=[]
        numberOfEmbeds = math.ceil(len(names)/15)
        if numberOfEmbeds>4:
            numberOfEmbeds=4
        
        currentData=0
        for i in range(numberOfEmbeds):
            customEmbeds.append(discord.Embed(title="Packs",color=0xff0000))
            for j in range(15):
                try:
                    customEmbeds[i].add_field(name=names[(currentData*15)+j],value=fields[(currentData*15)+j])
                except IndexError as e:
                    break
            currentData+=1

        current_page=1

        message = await ctx.send(embed=customEmbeds[0])
        # getting the message object for editing and reacting
        
        # ctx.author.id = [ctx.channel.name,ctx.message.id,message.id]
        if ctx.author.id in created.keys():
            guild= self.bot.get_guild(ctx.guild.id)

            channel = get(guild.channels,name=created[ctx.author.id][0])

            try:
                msg0 = await channel.fetch_message(created[ctx.author.id][1])
                await msg0.delete()
            except discord.errors.NotFound as e:
                pass
            
            try:
                msg1 = await channel.fetch_message(created[ctx.author.id][2])
                await msg1.delete()
            except discord.errors.NotFound as e:
                pass

            del created[ctx.author.id]

        created[ctx.author.id]=[ctx.channel.name,ctx.message.id,message.id]

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and current_page != numberOfEmbeds:
                    current_page += 1
                    
                    await message.edit(embed=customEmbeds[current_page-1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    await message.edit(embed=customEmbeds[current_page-1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                try:
                    channel = get(guild.channels,name=created[ctx.author.id][0])
                    msg3= channel.fetch_message(ctx.message.id)
                    await msg3.delete()
                except discord.errors.NotFound as e:
                    pass
                if ctx.author.id in created.keys():
                    del created[ctx.author.id]
                
                # ending the loop if user doesn't react after x seconds
        """
        name = " ".join(args)
        
        with open("packs.txt","r") as f:
            data = f.readlines()

        
        packs = discord.Embed(title="Packs",color=0xff0000)
        

        for i in data:
            
            end = i[i.rfind(":")+1:-1]

            start=i.find(":")
            if name.lower() in i[0:start].lower():
  
                if end !="":
                    packs.add_field(name=i[0:start]+":"+end,value=i[start+1:i.find(":",start+1)],inline=False)
                else:
                    packs.add_field(name=i[0:start],value=i[start+1:i.find(":",start+1)],inline=False)

        await ctx.author.send(embed=packs)"""

    
    @commands.command(aliases=["getpackauthor"])
    async def _getPackAuthor(self, ctx:commands.Context,*args):
        author = " ".join(args)
        print(author)
        with open("packs.txt","r") as f:
            data = f.readlines()

        packs = discord.Embed(title=f"Packs by {author}",color=0xff0000)
        
        for i in data:
            start = i.find(":")
            end=i.rfind(":")
            if author.lower() in i[end:-1].lower():
                packs.add_field(name=i[0:start],value=i[start+1:i.find(":",start+1)], inline=False)

        await ctx.author.send(embed=packs)

    @commands.is_owner()
    @commands.command(aliases=["dpack","dp"])
    async def _downloadPack(self, ctx:commands.Context):
        await ctx.send(file=discord.File("packs.txt"))

    @commands.is_owner()
    @commands.command(aliases=["dbackup"])
    async def _downloadBackup(self, ctx:commands.Context):
        await ctx.send(file=discord.File("backup.txt"))    

    @commands.is_owner()
    @commands.command(aliases=["drestore"])
    async def _downloadRestore(self, ctx:commands.Context):
        await ctx.send(file=discord.File("restore.txt"))    

    @commands.is_owner()
    @commands.command(aliases=["epack","ep"])
    async def _editpack(self, ctx:commands.Context):
        # Does a backup of the packs first
        with open("packs.txt","r") as f:
            data = f.read()
        
        with open("backup.txt","w+") as f:
            f.write(data)
        
        attachment = ctx.message.attachments[0].url
        file = requests.get(attachment)

        #Removes the \r at the end of the lines
        final = [line for line in file.text.split("\r")]

        with open("packs.txt","w") as f:
            for i in final:
                f.write(i)

        await ctx.send("Edited succesfully")
    
    @commands.is_owner()
    @commands.command(aliases=["cbackup"])
    async def _createbackup(self, ctx:commands.Context):
        with open("packs.txt","r") as f:
            data = f.read()
        
        with open("backup.txt","w+") as f:
            f.write(data)

        await ctx.send("Backup created")
    
    @commands.is_owner()
    @commands.command(aliases=["crestore"])
    async def _createrestore(self, ctx:commands.Context):
        with open("packs.txt","r") as f:
            data = f.read()
        
        with open("restore.txt","w+") as f:
            f.write(data)

        await ctx.send("restore created")
    
    @commands.is_owner()
    @commands.command(aliases=["restore"])
    async def _restore(self, ctx:commands.Context):
        # Does a backup of the packs first
        with open(" restore.txt","r") as f:
            data = f.read()
        
        with open("packs.txt","w+") as f:
            f.write(data)

        await ctx.send("Backup restored to packs.txt")
    
    @commands.is_owner()
    @commands.command(aliases=["backup"])
    async def _restore(self, ctx:commands.Context):
        # Does a backup of the packs first
        with open(" restore.txt","r") as f:
            data = f.read()
        
        with open("packs.txt","w+") as f:
            f.write(data)

        await ctx.send("Backup restored to packs.txt")
    
    @commands.is_owner()
    @commands.command(aliases=["dall"])
    async def _restore(self, ctx:commands.Context):
        if os.path.exists("packs.txt"):
            await ctx.send(file=discord.File("packs.txt"))
        
        if os.path.exists("backup.txt"):
            await ctx.send(file=discord.File("backup.txt"))

        if os.path.exists("restore.txt"):
            await ctx.send(file=discord.File("restore.txt"))

def setup(bot):
    bot.add_cog(Packs(bot))
