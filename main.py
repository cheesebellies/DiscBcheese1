from discord.ext import commands
from discord.ext import tasks
import discord
import os
from dotenv import load_dotenv
import itertools
import asyncio
import pafy
from ytsearch import searchr
from ytdl import downloader
from ytdl import deleter
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL



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

status = itertools.cycle(['Music coming soon!','Status cycling!','online 24/7!'])
#hello
@tasks.loop(seconds=20)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))
@tasks.loop(seconds=10800)
async def dchekr():
  fszs = 0
  for filename in os.listdir("/home/runner/discb2/audio/"):
    fszs += os.path.getsize(filename)
  if fszs > 1073741824:
    deleter()


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
      


  
# @bot.command(name="queue",help="Adds, removes, and plays songs in a queue. P stands for play, which plays the queue from the start, A stands for add, L stands for list.  Usage: -queue (p, a, r) (song name if applicable)  Example: -queue a NCS Candyland")
# async def queue(cxt,*args):
#   inpvalid = True
#   inp = ""
#   sresult = []
#   name1 = ""
#   url1 = ""
#   num1 = 0
#   qlen = 0
#   tru1 = True
#   sendstr = ""
#   qnum = 0

#   if len(args) != 0:
#     typ = args[0]
#     if len(args) >1:
#       for i in args[0:]:
#         inp += i
#     elif typ.lower() != "l":
#       await cxt.send("Invalid input.")
#       inpvalid = False
#   elif typ.lower() != "l":
#     await cxt.send("Invalid input.")
#     inpvalid = False
#   if inpvalid == True:
#     if typ.lower() == "a":

#       sresult = searchr(inp,1)

#       f = open("queue.txt","a")
#       f.write(f"{sresult[0][0]}\n")
#       f.close

#     elif typ.lower() == "r":
#       with open("queue.txt", "r") as f:
#         lines = f.readlines()
#       with open("queue.txt", "w") as f:
#         for line in lines:
#           if line.strip("\n") != inp:
#             f.write(line)
#     elif typ.lower() == "p":
#       f = open("queue.txt","r")
#       qlen = len(f.readlines())
#       if qlen != 0:
#         while tru1:
#           num1 += 1
#           name1 = (f.readlines())[num1].strip("\n")
#           if qlen == num1:
#             tru1 =  False
#           url1 = (searchr(name1,1))[1]
#           path = downloader(url1)
#           playa(cxt,path)
#           asyncio.sleep((((int(searchr[2])[0])*60)+((int(searchr[2])[2:])))+1)



#       else:
#         await cxt.send("Queue is empty.")

#     elif typ.lower() == "l":
#       f=open("queue.txt")
#       sendstr = "Current Queue:\n"
#       for i in f.readlines().strip("\n"):
#         qnum += 1
#         sendstr += f"{qnum}. {i}\n"
#       cxt.send(sendstr)

#     else:
#       await cxt.send("Invalid input.")



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




    
  



#portions of this bot were made using code from here: https://github.com/eric-yeung/Discord-Bot/blob/master/main.py
  
bot.run(TOKEN) 
