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
import youtube_dl
from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
import pafys

list_to_play = []
paused = False

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

async def playa(ctx,url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':   'True'}
    FFMPEG_OPTIONS = {
          'before_options': '-reconnect 1   -reconnect_streamed 1 -reconnect_delay_max 5',  'options': '-vn'}

    voice = get(bot.voice_clients, guild=ctx.guild)
    with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          URL = info['url']
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()


@tasks.loop(seconds=3)
async def play_the_list():
  global list_to_play
  
  if paused == False:
    
      if len(list_to_play) != 0:
        ctx = list_to_play[0][1]

        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing() == False:

          if len(list_to_play) != 0:
            await playa(list_to_play[0][1],list_to_play[0][0])
            del list_to_play[0]


async def getitle(url):    
  video = pafys.new(url)
  return video.title


async def video_id(value):
    query = urllib.parse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


@bot.command(name="play",help="Plays the first Youtube result from the input you give. Usage:   -play [search here]   Example:   -play Never Gonna Give You Up",aliases=["p"])
async def play(ctx,*args):
  global list_to_play
  plyinp = ""
  inpvalid = True
  result = []
  
  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if len(args) != 0:
    for i in args:
      plyinp += f'{i} '
  else:
    await ctx.send("Invalid input.")
    inpvalid = False
  
  if inpvalid == True:

    result = searchr(plyinp,1)
    vidurl = result[0][1]

    list_to_play = [[vidurl, ctx]]
      
      
  

@bot.command(name="search",help="Gets the top ten results for your search. Usage: -search [search here]  Example: -search Crab Rave",aliases=["s"])
async def search(ctx,*args):
  global list_to_play
  plyinp = ""
  inpvalid = True
  sresult = []
  sendstr = ""
  sendstrint = 0
  
  voice_client = get(bot.voice_clients, guild=ctx.guild)
  if len(args) != 0:
    for i in args:
      plyinp += f'{i} '
  else:
    await ctx.send("Invalid input.")
    inpvalid = False
  if inpvalid == True:
    sendstr = f"Top results for {plyinp}:\n"
    sresult = searchr(plyinp,10)
    for i in sresult:
      sendstrint += 1
      sendstr += f"{sendstrint}.  {i[0]}\n"
    sendstr += "\nChoose one to continue:"

    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and ("1" in msg.content or "2" in msg.content or "3" in msg.content or "4" in msg.content or "5" in msg.content or "6" in msg.content or "7" in msg.content or "8" in msg.content or "9" in msg.content or "10" in msg.content)

    await ctx.send(sendstr)

    try:
      nmessage = await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
      await ctx.send("Timed out.")
    else:

      vidurl = (sresult[int(nmessage.content)-1])[1]
      
    list_to_play = [[vidurl,ctx]]
      
      
      



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
    global list_to_play
    await ctx.voice_client.disconnect()
    list_to_play = []

@bot.command(name="resume",help="Resumes playig whatever it was before.")
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global paused

    if not voice.is_playing():
        voice.resume()
        paused = False


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global paused

    if voice.is_playing():
        voice.pause()
        paused = True
        


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    global list_to_play
    
    if voice.is_playing():
        voice.stop()  
        list_to_play = []

  

@bot.command(name="url")
async def pburl(ctx,url):
  global list_to_play
  list_to_play = [[url,ctx]]


@bot.command(name="queue",help="usage: -queue")
async def queue(ctx,*args):
  global list_to_play
  plyinp = ""
  inpvalid = True
  result = []
  sresult = []
  sendstr = ""
  sendstrint = 0

  if len(args) != 0:
    for i in args:
      plyinp += f'{i} '
  else:
    await ctx.send("Invalid input.")
    inpvalid = False

  if inpvalid == True:

    if len(args) != 0:

      if args[0] == "name":
        result = searchr(plyinp,1)
        vidurl = result[0][1]
        list_to_play.append([vidurl, ctx])
      elif args[0] == "url":
        vidurl = args[1]
        list_to_play.append([vidurl, ctx])
      elif args[0] == "clear":
        list_to_play = []
      elif args[0] == "search":
        sendstr = f"Top results for {plyinp}:\n"
        sresult = searchr(plyinp,10)
        for i in sresult:
          sendstrint += 1
          sendstr += f"{sendstrint}.  {i[0]}\n"
        sendstr += "\nChoose one to continue:"

        def check(msg):
          return msg.author == ctx.author and msg.channel == ctx.channel and ("1" in msg.content or "2" in msg.content or "3" in msg.content or "4" in msg.content or "5" in msg.content or "6" in msg.content or "7" in msg.content or "8" in msg.content or "9" in msg.content or "10" in msg.content)

        await ctx.send(sendstr)

        try:
          nmessage = await bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
          await ctx.send("Timed out.")
        else:

          vidurl = (sresult[int(nmessage.content)-1])[1]

        list_to_play.append([vidurl,ctx])
        

@bot.command(name="next",help="-next outputs videos in queue")
async def qnxt(ctx):
  global list_to_play
  otp = ""

  if len(list_to_play) != 0:
    for i in list_to_play:
      otp += f"1)  {await getitle(i[0])}\n"
  else:
    otp = "Nothing in queue."
  await ctx.send(otp)



# @bot.command(name="playlist",help="-playlist (add, search, view, remove, delete, play")
# async def playlistopts(ctx,*args):
#   global list_to_play
#   plyinp = ""
#   inpvalid = True
#   result = []
#   sresult = []
#   sendstr = ""
#   sendstrint = 0

#   if len(args) != 0:
#     for i in args:
#       plyinp += f'{i} '
#   else:
#     await ctx.send("Invalid input.")
#     inpvalid = False

#   if inpvalid == True:

#     if 


'''
embeds:
first two tabs of the group
'''


@bot.command(name="embed",help="dev tool")
async def embedr(ctx,url):
  ttl = await getitle(url)
  vgid = await video_id(url)
  embed=discord.Embed(title="**Now playing:**", color=0xFF000,url=url)
  embed.add_field(name=ttl, inline=False)
  embed.set_thumbnail(f"https://img.youtube.com/vi/{vgid}/default.jpg")

  await ctx.send(embed)


       


#Create playlists (maybe from yt playlist, somehow search in playlists?) probably just from -playlist add (name, url).

#play live vidoes... may be too hard... more research needed (into ffmpeg, youtube-dl ; read the docs)

#make the gui look better/give more responses for what its doing


bot.run(TOKEN) 
