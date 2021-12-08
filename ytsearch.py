from youtubesearchpython import VideosSearch

def searchr(inpt,amnt):
  vs = VideosSearch(inpt, limit = amnt)

  vsr = vs.result()

  returnr = []

  for i in vsr.get("result"):
    returnr.append([i.get("title"),i.get("link"),i.get("duration")])
  return returnr
