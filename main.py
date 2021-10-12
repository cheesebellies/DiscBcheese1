from discord.ext import commands
from discord.ext import tasks
import discord
import discord.py
import os
from dotenv import load_dotenv
import itertools


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=';')

status = itertools.cycle(['Music coming soon!','Status cycling!','online 24/7!'])

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
  await bot.change_presence(activity=discord.Game(next(status)))
                              

bot.run(TOKEN)
