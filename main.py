#!/usr/bin/env python
#
import youtube_dl
import os
import music_tag
from banners import *
import configparser

def configure(HOME):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'MusicDir': os.path.join(HOME, 'Music/')}
    os.mkdir(HOME+'/.config/mustube')
    with open(os.path.join(HOME, '.config/mustube/config.ini'), 'w') as configfile:
        config.write(configfile)

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

def pathbyid(videoid, path):
    fileslist = os.listdir(path)
    return path+fileslist[list(map(str.endswith, fileslist, [videoid+'.mp3']*len(fileslist))).index(True)]

def main(config):
    os.system('clear')
    print(INDEX_BANNER)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': config.get('DEFAULT', 'MusicDir')+'%(title)s-%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    url = input('URL: ').replace("'", "")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    tagging(pathbyid(videoid(url), config.get('DEFAULT', 'MusicDir')))



if __name__=='__main__':
    HOMEDIR = os.environ['HOME']
    if 'mustube' not in os.listdir(HOMEDIR+'/.config/'):
        configure(HOMEDIR)
    config = configparser.ConfigParser()
    config.read(os.path.join(HOMEDIR, '.config/mustube/config.ini'))
    while True:
        try:
            main(config)
            if input('Continue? [Y/n] ').lower()=='n':
                break
        except KeyboardInterrupt:
            break
