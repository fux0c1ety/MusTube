#!/usr/bin/env python
#
import youtube_dl
import os
import music_tag
from banners import *

def tagging(path):
    MusFile = music_tag.load_file(path)
    MusFile['title'] = input('Song Title: ')
    MusFile['artist'] = input('Artist: ')
    MusFile.save()

def videoid(url):
    if 'youtube.com' in url:
        return url.split('=')[1]
    elif 'youtu.be' in url:
        return url.split('/')[-1]

def pathbyid(videoid):
    path = os.environ['HOME']+'/Music/'
    fileslist = os.listdir(path)
    return path+fileslist[list(map(str.endswith, fileslist, [videoid+'.mp3']*len(fileslist))).index(True)]

def main():
    os.system('clear')
    print(INDEX_BANNER)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl':'~/Music/%(title)s-%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    url = input('URL: ').replace("'", "")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    tagging(pathbyid(videoid(url)))



if __name__=='__main__':
    while True:
        try:
            main()
            if input('Continue? [Y/n] ').lower()=='n':
                break
        except KeyboardInterrupt:
            break
