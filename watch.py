import discord
from discord.ext import commands

TOKEN = ""

client = commands.Bot(command_prefix = ".")
pot = []
neg = []
channel_list=[566851123982630930,568856151844978738,568856167326023680]
size_watch=["5.5","6","6.5","7","7.5","8","8.5","9","9.5","10","10.5","11","11.5","12","12.5","13","13.5","14","14.5","15"]
size_black=[]

with open('pot.txt', 'r') as f:
    pot = f.read().split('\n')

with open('neg.txt', 'r') as f:
    neg = f.read().split('\n')

with open('size_black.txt', 'r') as f:
    size_black = f.read().split('\n')
size_watch= list(set(size_watch)-set(size_black))

def num_there(s):
    return any(i.isdigit() for i in s)

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    POST = True
    channel=message.channel
    channel_id=message.channel.id
    
    ## Add Watch Keyword and Blacklist
    if message.content.lower().startswith("!add"):
        newKW= message.content[5:]
        if newKW[0]=="+":
            if newKW[1:] in pot:
                await channel.send("ERROR:The keyword "+ newKW[1:]+"already exists in the watch list!")
            else:
                pot.append(newKW[1:])
                try:
                    neg.remove(newKW[1:])
                except:
                    pass
                await channel.send("Success: "+ newKW[1:]+" added to pot list")
        elif newKW[0]=="-":
            if newKW[1:] in neg:
                await channel.send("ERROR:The keyword "+ newKW[1:]+"already exists in the blacklist!")
            else:
                neg.append(newKW[1:])
                try:
                    pot.remove(newKW[1:])
                except:
                    pass
                await channel.send("Success: "+ newKW[1:]+" added to pot list")
        else:
            await channel.send("Error in format: !ADD +123 for adding 123 into watch list  !ADD -123 for adding 123 into black list")
        return 0
    ## Remove Watch Keyword and Blacklist
    if message.content.lower().startswith("!remove"):
        newKW= message.content[8:]
        if newKW[0]=="+":
            if newKW[1:] not in pot:
                await channel.send("ERROR:The keyword "+ newKW[1:]+" does not exist in the watch list!")
            else:
                pot.remove(newKW[1:])
                await channel.send("Success: "+ newKW[1:]+" removed from watch list")
        elif newKW[0]=="-":
            if newKW[1:] not in neg:
                await channel.send("ERROR:The keyword "+ newKW[1:]+" does not exist in the blacklist!")
            else:
                neg.remove(newKW[1:])
                await channel.send("Success: "+ newKW[1:]+" removed from black list")
        else:
            await channel.send("Error in format: !remove +123 for removing 123 from watch list  !remove -123 for removing 123 from black list")
        return 0

    
    ##### Size section
    if message.content.lower().startswith("!sizeadd"):
        newKW= message.content[9:]
        if newKW[0]=="+":
            if newKW[1:] in size_watch:
                await channel.send("ERROR:The size "+ newKW[1:]+"already exists in the watch list!")
            else:
                size_watch.append(newKW[1:])
                try:
                    size_black.remove(newKW[1:])
                except:
                    pass
                await channel.send("Success: "+ newKW[1:]+" added to pot list")
        elif newKW[0]=="-":
            if newKW[1:] in size_black:
                await channel.send("ERROR:The size "+ newKW[1:]+" already exists in the size ignore list!")
            else:
                size_black.append(newKW[1:])
                try:
                    size_watch.remove(newKW[1:])
                except:
                    pass
                await channel.send("Success: "+ newKW[1:]+" added to size ignore list")
        else:
            await channel.send("Error in format: !sizeadd +123 for adding 123 into size watch list  !add -123 for adding 123 into size ignore list")
        return 0

    if message.content.lower().startswith("!sizeremove"):
        newKW= message.content[12:]
        if newKW[0]=="+":
            if newKW[1:] not in size_watch:
                await channel.send("ERROR:The size "+ newKW[1:]+" does not exist in the size watch list!")
            else:
                size_watch.remove(newKW[1:])
                size_black.append(newKW[1:])
                await channel.send("Success: "+ newKW[1:]+" removed from watch list")
        elif newKW[0]=="-":
            if newKW[1:] not in size_black:
                await channel.send("ERROR:The keyword "+ newKW[1:]+" does not exist in the size ignore list!")
            else:
                size_black.remove(newKW[1:])
                size_watch.append(newKW[1:])
                await channel.send("Success: "+ newKW[1:]+" removed from the size ignore list")
        else:
            await channel.send("Error in format: !sizeremove +123 for removing 123 from size watch list  !sizeremove -123 for removing 123 from size ignore list")
        return 0
    ## Show both lists
    if message.content.lower().startswith("!show"):
        temp=""
        await channel.send("Watch list Keywords:")
        if len(pot)!=0:
            for i in pot:
                temp+=i+" \n"
        else:
            temp="None"
        await channel.send("```"+temp+"```")
        temp=""
        await channel.send("\nBlack list Keywords:")
        if len(neg)!=0:
            for i in neg:
                temp+=i+" \n"
        else:
            temp="None"
        await channel.send("```"+temp+"```")
        temp=""
        await channel.send("\nWatching Size:")
        if len(size_watch)!=0:
            for i in size_watch:
                temp+=i+" \n"
        else:
            temp="None"
        await channel.send("```"+temp+"```")
        temp=""
        await channel.send("\nIgnoring Size:")
        if len(size_black)!=0:
            for i in size_black:
                temp+=i+" \n"
        else:
            temp="None"
        await channel.send("```"+temp+"```")
        return 0
    try:
        POST= True
        embed= message.embeds
        title = embed[0].title
        des = embed[0].description
        fields = embed[0].fields
        # select field 1-7 into filtering selection
        if num_there(fields[4].name) and any(substring in fields[4].name for substring in size_black):
            #debug Mode:
            print ("Ignored size caught in field[4] name")
            print ("Debug Uses... Field[4] Name is: "+fields[4].name)
            POST = False
        else:
            if num_there(fields[4].value.split(']')[0]) and any(substring in fields[4].value.split(']')[0] for substring in size_black):
                #debug Mode:
                print ("Ignored size caught in field[4] value")
                print ("Debug Uses... Field[4] value is: "+fields[4].value.split(']')[0])
                POST = False
            
        if (POST and any(substring in title for substring in pot)and
            not(any(substring in title for substring in neg))and
            channel_id in channel_list):
            print("Keyword caught!")
            await channel.send("Keyword FOUND: "+title+" @everyone")
        else:
            if (POST and not(any(substring in title for substring in neg)) and
                any(substring in des for substring in pot) and
             not(any(substring in des for substring in neg))and
            channel_id in channel_list):
                print("Keyword caught!")
                await channel.send("Keyword FOUND: "+des+" @everyone")

    except:
        print ("Ignored")
        pass
    finally:
        print ("Monitoring...")
client.run(TOKEN)
