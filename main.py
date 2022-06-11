#!/usr/bin/env python
#
import youtube_dl
import os
import music_tag

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
    fileslist = os.listdir('./')
    return fileslist[list(map(str.endswith, fileslist, [videoid+'.mp3']*len(fileslist))).index(True)]

def main():
    ydl_opts = {
        'format': 'bestaudio/best',
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
    main()
