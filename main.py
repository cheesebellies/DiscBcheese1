from discord.ext import commands
from discord.ext import tasks
import discord
from itertools import cycle
import os
from dotenv import load_dotenv
import asyncio
from ytsearch import searchr
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

list_to_play = []


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
  change_status.start()
  play_the_list.start()
  
status = cycle(['Music is here!','More features soon!'])

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

async def playa(url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':   'True'}
    FFMPEG_OPTIONS = {
          'before_options': '-reconnect 1   -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}

    voice = get(bot.voice_clients, guild=bot.get_guild(782024223311790100))
    with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          URL = info['url']
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()


@tasks.loop(seconds=3)
async def play_the_list():
  global list_to_play
  
  voice = get(bot.voice_clients, guild=bot.get_guild(782024223311790100))
  if voice.is_playing() == False:

    await playa(list_to_play[0])

    if len(list_to_play) != 0:
      playa(list_to_play[0])
      del list_to_play[0]


@bot.command(name="play",help="Plays the first Youtube result from the input you give. Usage:   -play [search here]   Example:   -play Never Gonna Give You Up",aliases=["p"])
async def play(cxt,*args):
  global list_to_play
  plyinp = ""
  inpvalid = True
  result = []
  
  voice_client = get(bot.voice_clients, guild=bot.get_guild(782024223311790100))  
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
          list_to_play = [vidurl]
    else:
      list_to_play = [vidurl]
      
      
  

# @bot.command(name="search",help="Gets the top ten results for your search. Usage: -search [search here]  Example: -search Crab Rave",aliases=["s"])
# async def search(cxt,*args):
#   global list_to_play
#   plyinp = ""
#   inpvalid = True
#   sresult = []
#   sendstr = ""
#   sendstrint = 0
  
#   voice_client = get(bot.voice_clients, guild=bot.get_guild(782024223311790100))
#   if len(args) != 0:
#     for i in args:
#       plyinp += i
#   else:
#     await cxt.send("Invalid input.")
#     inpvalid = False
#   if inpvalid == True:
#     sendstr = f"Top results for {plyinp}:\n"
#     sresult = searchr(plyinp,10)
#     for i in sresult:
#       sendstrint += 1
#       sendstr += f"{sendstrint}.  {i[0]}\n"
#     sendstr += "\nChoose one to continue:"

#     def check(msg):
#       return msg.author == cxt.author and msg.channel == cxt.channel and ("1" in msg.content or "2" in msg.content or "3" in msg.content or "4" in msg.content or "5" in msg.content or "6" in msg.content or "7" in msg.content or "8" in msg.content or "9" in msg.content or "10" in msg.content)

#     try:
#       nmessage = await bot.wait_for("message", check=check, timeout=20)
#     except asyncio.TimeoutError:
#       await cxt.send("Timed out.")
#     else:

#       vidurl = (sresult[int(nmessage.content)-1])[1]


#     if voice_client.is_playing() == True:
#       await cxt.send("Video already playing. Replace? y/n")
      
#       def check(msg):
#         return msg.author == cxt.author and msg.channel == cxt.channel and ("y" in msg.content.lower() or "n" in msg.content.lower())

#       try:
#         replacemessage = await bot.wait_for("message", check=check, timeout=20)
#       except asyncio.TimeoutError:
#         await cxt.send("Timed out.")
#       else:
#         if replacemessage.contents.lower() == "y":
#           await stop()
#           list_to_play = [vidurl]
#     else:
#       list_to_play = [vidurl]
      



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
  global list_to_play
  list_to_play = [url]


@bot.command(name="queue",help="usage: -queue")
async def queue(cxt,*args):
  global list_to_play
  plyinp = ""
  inpvalid = True
  result = []

  if len(args) != 0:
    for i in args:
      plyinp += i
  else:
    await cxt.send("Invalid input.")
    inpvalid = False

  if inpvalid == True:

    if len(args) != 0:

      if args[0] == "name":
        result = searchr(plyinp,1)
        vidurl = result[0][1]
        list_to_play.append(vidurl)
      elif args[0] == "url":
        vidurl = args[1]
        list_to_play.append(vidurl)
      elif args[0] == "clear":
        list_to_play = list_to_play[1:]



#portions of this bot were made using code from here: https://github.com/eric-yeung/Discord-Bot/blob/master/main.py
#with help from https://stackoverflow.com
#and https://realpython.org,
#https://discordpy.readthedocs.io,
#and https://google.com
  
bot.run(TOKEN) 
