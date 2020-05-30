import discord
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
import requests
import youtube_dl
import os

def read_token() :
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def badwords():
    with open("blacklist.txt", "r") as s:
        badwords = s.read().strip().split("\n")
        return badwords


swear_log = {}

serverlist = {}


token = read_token()

bl_words = badwords()

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")

    


#Work on Swear Filter
@bot.event
async def on_message(message):
    if any(bl_word in message.content.lower() for bl_word in bl_words):
        server = message.guild.id
        user = message.author.name
        iden = message.author.id
        
        val = serverlist[server]

        if val == True:
            await message.delete()
            await message.channel.send(f"{user} has sweared, you bad boy")
            user_sweared = True
            
            if user_sweared == True:
                swear_log[iden] = 1

            for iden, swearcount in swear_log.items():
                if swearcount == 1:
                    swear_log[iden] = 2
                elif swearcount == 2:
                    swear_log[iden] = 3
                    print(swear_log.get(iden))
                    await message.channel.send("You have sweared 3 times too many, notifying an admin.")
                    swear_log.pop(iden)

            
            
            
            """elif iden in swear_log:
                swear_log.pop(iden)
                swear_log[iden] = 2
            elif iden in swear_log:
                swear_log.pop(iden)
                swear_log[iden] = 3
                await message.channel.send("You have sweared 3 times too many, notifying an admin")"""


                
                
            """if iden in swear_log:
                swear_count += 1
                swear_log[iden] = swear_count
                if iden in swear_log:
                    swear_log.pop(iden)
                    await message.channel.send("You have sweared 3 times too many, notifying an Admin.")"""    
                        
            print(swear_log)
        elif val == False:
            pass
        

    await bot.process_commands(message)

#Swear Filter ends here

@bot.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=int(amount))
        
@bot.command(pass_context = True, aliases = ["j", "joi"])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f"Joined {channel}")



@bot.command(pass_context = True, aliases = ["l", "lea"])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Wow, you really think that I'm in a voice channel do you?")


@bot.command(pass_context=True, aliases=["p", "pla"])
async def play(ctx, url: str):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if not voice and voice.is_connected():
        channel = ctx.message.author.voice.channel
        await channel.connect()

    song_there = os.path.isfile("song.mp3")
    
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")

    except PermissionError:
        print("Trying to remove song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return
    
    await ctx.send("Getting everything ready")

    

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'C:/Users/banan/code/renai/song.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': "192",
        }],
        
    }

    

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])



    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    await ctx.send("Playing")
    print("Playing")

@bot.command(pass_context = True, aliases = ["pa", "pau"])
async def pause(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Paused Music")
    else:
        print("User tried to stop the music but nothing was playing")
        await ctx.send("Nothing is playing")

@bot.command(pass_context = True, aliases = ["s", "sto"])
async def stop(ctx):

    voice = get(bot.voice_clients, guild = ctx.guild)

    channel = ctx.message.author.voice.channel

    if voice and voice.is_playing():
        print("Music stopped")
        voice.pause()
        await voice.disconnect()
        await ctx.send("Stopping the music")
    elif voice and voice.is_connected():
        print(f"Bot left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was asked to stop, wasn't connected")
        await ctx.send("Bot wasn't connected to a channel")

@bot.command(pass_context = True, aliases = ["r", "res"])
async def resume(ctx):
    
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_paused():
        print("resumed music")
        voice.resume()
        await ctx.send("Resumed the music")
    else:
        print("user tried to resume music although its already playing")
        await ctx.send("Music is already playing")


@bot.command(pass_context=True)
async def ohno(ctx):
    username = ctx.message.author.name

    voice.play(discord.FFmpegPCMAudio("sc.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    await ctx.send("SCOTLAND FOREVER")
    print(f"{username} has probably made a big mistake")

@bot.command(pass_context=True)
async def china(ctx):
    voice.play(discord.FFmpegPCMAudio("alex.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1
    
    username = ctx.message.author.name
    
    await ctx.send(f"{username} is now Chinese")

    print(f"{username} is now gonna become a doctor")


@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.send(f"my ping is {ping} ms")

@bot.command()
async def swearfilter(ctx, answer):
    server_iden = ctx.guild.id
    if answer == "yes":
        actual_answer = True
        await ctx.send("Enabling Swear Filter")
    elif answer == "no":
        actual_answer = False
        await ctx.send("Disabling Swear Filter")
    else:
        await ctx.send("You have to answer either yes or no.")
    serverlist[server_iden] = actual_answer
    print(serverlist)

'''@bot.command()
async def osu(ctx, username):
    url = f"https://osustats.click/{username}"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

    page = requests.get(url, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    pname = soup.find(class_ = "PlayerCard__name").get_text(' ', strip=True)
    pplace = soup.find(class_ = "PlayerCard__value").get_text(' ', strip=True)
    ppcount = soup.find(class_ = "PlayerCard__value").get_text(' ', strip=True)

    await ctx.send(f"{pname} \n {pplace} \n {ppcount}")
'''
@bot.command()
async def invite(ctx):
    await ctx.send("Invite me to anther server through this link! https://discord.com/oauth2/authorize?client_id=692930408907800637&scope=bot&permissions=8")

bot.remove_command("help")

@bot.command()
async def help(ctx):
    await ctx.author.send("""Here is the list of commands for Renaissance Man:
.clear (number of messages to delete): deletes a certain amount of messages, standard amount is 2. 
.join: joins channel that you are in. .leave: leaves channel it is in. 
.play (youtube link): plays the youtube link that you have provided. 
.stop: stops the music bot and leaves the channel. 
.resume: resumes the music bot. .pause: pauses the music bot. 
.ping: returns the latency of the bot. 
.swearfilter (yes or no): enables or disables the swearfilter, this is server specific. 
.invite: gives you an invite link to invite the bot to another server. 
.help DM's you this command. 
If you have more questions or suggestions for new features, ask on the support server : https://discord.gg/2Rt3EY8""")

bot.run(token)
