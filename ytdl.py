from __future__ import unicode_literals

import pafy
import youtube_dl
import os

def downloader(url):

  def my_hook(d):
      if d['status'] == 'finished':
          print('Done downloading, now converting ...')

  ydl_opts = {
      'format': 'bestaudio/best',       
      'outtmpl': '/home/runner/discb2/audio/%(title)s',        
      'noplaylist' : True,        
      'progress_hooks': [my_hook],  
  }
  vid = pafy.new(url)
  vidt = vid.title

  if f"{vidt}.mp3" not in os.listdir("/home/runner/discb2/audio/"):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

  os.rename(os.path.join("/home/runner/discb2/audio/",vidt),str(os.path.join("/home/runner/discb2/audio/",vidt + ".mp3")))
  return (os.path.join("/home/runner/discb2/audio/",vidt + ".mp3"))

def deleter():
  for filename in os.listdir("/home/runner/discb2/audio/"):
    if filename != "textnew.txt":
      os.remove(os.path.join("/home/runner/discb2/audio/",filename))
