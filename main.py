from discord.ext import commands
from discord.ext import tasks
import discord
import os
from dotenv import load_dotenv
import asyncio
import pafy
from ytsearch import searchr
from ytdl import downloader
from ytdl import deleter
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import random


#make it so @tasks.loop(seconds=1) it checks to see if a global list has any items and if its currently playing, and plays it from the list. -play deletes all then adds one, -queue adds to the end.



load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='-')
@bot.event
async def on_ready():
  for guild in bot.guilds:
    print(
    f'{bot.user} is connected to the following guild(s):\n'
    f'{guild.name}(id: {guild.id})'
    )
  await change_status()

@tasks.loop(seconds=20)
async def change_status():
  await bot.change_presence(activity=discord.Game(random.choice(["Music is here!","More music features soon!"])))
  print("t.loop notif")

async def playa(ctx,url):
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
  FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

  voice = get(bot.voice_clients, guild=ctx.guild)
  with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()




@bot.command(name="play",help="Plays the first Youtube result from the input you give. Usage:   -play [search here]   Example:   -play Never Gonna Give You Up",aliases=["p"])
async def play(cxt,*args):
  plyinp = ""
  inpvalid = True
  result = []
  voice_client = get(cxt.bot.voice_clients, guild=cxt.guild)
  
  if len(args) != 0:
    for i in args:
      plyinp += i
  else:
    await cxt.send("Invalid input.")
    inpvalid = False
  
  if inpvalid == True:

    result = searchr(plyinp,1)
    vidurl = result[0][1]


    if voice_client.is_playing() == True:
      await cxt.send("Video already playing. Replace? y/n")
      
      def check(msg):
        return msg.author == cxt.author and msg.channel == cxt.channel and ("y" in msg.content.lower() or "n" in msg.content.lower())

      try:
        replacemessage = await bot.wait_for("message", check=check, timeout=20)
      except asyncio.TimeoutError:
        await cxt.send("Timed out.")
      else:
        if replacemessage.contents.lower() == "y":
          await stop()
          await playa(cxt,vidurl)
    else:
      await playa(cxt,vidurl)
      
      
  

@bot.command(name="search",help="Gets the top ten results for your search. Usage: -search [search here]  Example: -search Crab Rave",aliases=["s"])
async def search(cxt,*args):
  plyinp = ""
  inpvalid = True
  sresult = []
  sendstr = ""
  sendstrint = 0
  voice_client = get(cxt.bot.voice_clients, guild=cxt.guild)

  if len(args) != 0:
    for i in args:
      plyinp += i
  else:
    await cxt.send("Invalid input.")
    inpvalid = False
  if inpvalid == True:
    sendstr = f"Top results for {plyinp}:\n"
    sresult = searchr(plyinp,10)
    for i in sresult:
      sendstrint += 1
      sendstr += f"{sendstrint}.  {i[0]}\n"
    sendstr += "\nChoose one to continue:"
    message = cxt.send(sendstr)

    def check(msg):
      return msg.author == cxt.author and msg.channel == cxt.channel and ("1" in msg.content or "2" in msg.content or "3" in msg.content or "4" in msg.content or "5" in msg.content or "6" in msg.content or "7" in msg.content or "8" in msg.content or "9" in msg.content or "10" in msg.content)

    try:
      nmessage = await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
      await cxt.send("Timed out.")
    else:

      vidurl = (sresult[int(nmessage.content)-1])[1]


    if voice_client.is_playing() == True:
      await cxt.send("Video already playing. Replace? y/n")
      
      def check(msg):
        return msg.author == cxt.author and msg.channel == cxt.channel and ("y" in msg.content.lower() or "n" in msg.content.lower())

      try:
        replacemessage = await bot.wait_for("message", check=check, timeout=20)
      except asyncio.TimeoutError:
        await cxt.send("Timed out.")
      else:
        if replacemessage.contents.lower() == "y":
          await stop()
          await playa(cxt,vidurl)
    else:
      await playa(cxt,vidurl)
      



@bot.command(name="join",help="Joins a vc. Usage: -join  Example: -join (use while in vc)")
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command(name="leave",help="Leaves a vc. Usage: -leave  Example: -leave (use while in vc)")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(name="resume",help="Resumes playig whatever it was before.")
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()  

  

@bot.command(name="url")
async def pburl(ctx,url):
  playa(ctx,url)


@bot.command(name="queue",help="usage: -queue (play, reset, url, name) input")
async def queue(cxt,*args):

  plyinp = ""
  inpvalid = True
  result = []
  voice_client = get(cxt.bot.voice_clients, guild=cxt.guild)
  
  if len(args) != 0:
    for i in args:
      plyinp += i
  else:
    await cxt.send("Invalid input.")
    inpvalid = False

  if inpvalid == True:

    if args[0] == "url":
      f = open("queue.txt","a")
      f.write(args[1])
      f.close()
    elif args[0] == "reset":
      open('file.txt', 'w').close()
    elif args[0] == "name":
      result = searchr(plyinp,1)
      vidurl = result[0][1]
      f = open("queue.txt","a")
      f.write(vidurl)
      f.close()
    elif args[0] == "play":
      f = open("queue.txt","r")
      qtxt = f.read().strip().split()
      f.close()
      for i in qtxt:
        playa(cxt,i)
        n = 0
        while n == 0:
          if voice_client.is_playing() == False:
            n = 1
            with open("queue.txt", "w") as f:
              for line in qtxt:
                  if line.strip("\n") != qtxt[i]:
                      f.write(line)




#portions of this bot were made using code from here: https://github.com/eric-yeung/Discord-Bot/blob/master/main.py
#with help from https://stackoverflow.com
#and https://realpython.org,
#https://discordpy.readthedocs.io,
#and https://google.com
  
bot.run(TOKEN) 
