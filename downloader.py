#!/usr/bin/env python


import os, pytube, sys, traceback

parentDirectory = "/root/projects/youtubedownloader/"

def downloadChannel(cLink):
  c = pytube.Channel(cLink)
  newFolder = True
  path = os.path.join(parentDirectory, c.channel_name)
  try:
    os.mkdir(path)
  except FileExistsError as e:
    fileList = os.listdir(path)
    if len(fileList)>0:
      newFolder = False
      prefixCount = 0
      for i in fileList[0]:
        if not i.isdigit():
          prefixCount += 3
          break
        prefixCount += 1
      videoSet=set()
      for file in fileList:
        file = file.removesuffix(".3gpp")
        videoSet.add(file[prefixCount:])

  l = len(c.videos)
  print(str(l)+" videos found")
  i = 0
  for video in c.videos:
    try:
      name = video.title
      strippedName = stripNonAscii(name)
      print("Progress: "+str(i)+" "+strippedName)
      if not newFolder:
        fileFound = str(strippedName in videoSet)
        if strippedName in videoSet:
          print("Video "+ strippedName + " exists, so not downloading")
          i = i+1
          continue
      video.streams.first().download(output_path = path, filename_prefix = digitpadded(l-i, l), filename = strippedName+".3gpp")
      i = i+1
    except Exception as e:
      print(e)
      traceback.print_exc()
      print(name + "failed to download")
      i=i+1

def digitpadded(num, total):
  l = len(str(total))
  d = len(str(num))
  return "0"*(l-d)+str(num)+" - "

def stripNonAscii(string):
    stripped = (c for c in string if (ord(c) == 32 or 48 <= ord(c) <= 57 or 65 <= ord(c) <= 90 or 97 <= ord(c) <= 122))
    name = ''.join(stripped)
    return name

if __name__ == "__main__":
  if len(sys.argv) == 1:
    f = open('channels.txt', 'r')
    lines = f.readlines()
    f.close()
    channels = (line.strip() for line in lines)
    for channel in channels:
      downloadChannel(channel)
  else:
    link = sys.argv[1]
    downloadChannel(link)
