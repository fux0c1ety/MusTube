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

def main(config):
    os.system('clear')
    print(INDEX_BANNER)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(config.get('DEFAULT', 'MusicDir'), '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    url = input('URL: ').replace("'", "")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        title = ydl.extract_info(url)['title']
        tagging(os.path.join(config.get('DEFAULT', 'MusicDir'), '{}.mp3'.format(title)))



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
