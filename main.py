from pytube import YouTube, Playlist
from colorama import Fore, init
from os.path import isfile, join
from os import listdir
import sys
import os


class Args:
    def __init__(self, url, path, audio, jump, to):
        self.url    = url
        self.path   = path
        self.audio  = audio
        self.jump   = jump
        self.to     = to

class Tubes:
    def __init__(self, ytb:YouTube, path):
        self.ytb        = ytb
        self.title      = ytb.title + '.mp4'
        self.path       = path
    
    def download(self, audio):
        try:
            if audio:
                self.ytb.streams.get_audio_only().download(output_path=tube.path, max_retries=3)
            else:
                self.ytb.streams.get_highest_resolution().download(output_path=tube.path, max_retries=3)
            print(Fore.GREEN + 'Done')
        except:
            print(Fore.RED + 'Error Download')


def isExist(files:list, title:str):
    return True if title in files else False

def isPlaylist(url):
    try:
        YouTube(url)
        return False
    except:
        try:
            Playlist(url)
            return True
        except:
            return None

def playlistInfos(pl:Playlist):
    try:
        title = pl.title
    except:
        title = 'Error getting Title'
    try:
        owner = pl.owner
    except:
        owner = 'Error getting Owner'
    try:
        length = pl.length
    except:
        length = 'Error getting Length'
    try:
        lastUp = pl.last_updated
    except:
        lastUp = 'Error getting Last Update Date'
    print(Fore.WHITE + f'Name: {title}', end='')
    print(Fore.WHITE + f' | Owner: {owner}', end='')
    print(Fore.WHITE + f' | Length: {length}', end='')
    print(Fore.WHITE + f' | Last Update: {lastUp}')

def getPlaylistTubes(playlist:Playlist, args:Args):
    temp = list(playlist.videos)
    pl_title = 'Unknow'
    for i in range(3):
        try:
            pl_title = playlist.title
        except:
            continue
    if (args.jump > 0):
        del temp[0:args.jump-1]
    if (args.to > 0):
        del temp[args.to-args.jump+1:]
    tubes, failed  = [], []
    for i in temp:
        try:
            tubes.append(Tubes(i, args.path + pl_title))
        except:        
            failed.append(i)
    for i in failed:
        try:
            tubes.append(Tubes(i, args.path + pl_title))
        except:
            print(Fore.RED + f'Fail to obtain download information for: {i.title}')
    return tubes

def main():
    AUDIO_PATH = str(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Music') + '\\DLYoutube\\')
    VIDEO_PATH = str(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Videos') + '\\DLYoutube\\')

    PLAYLISTS = {
        'lofi': 'https://www.youtube.com/playlist?list=PLnCmeDfRjs0K7Hu837u7b1xez3oPxJYzm',
        'funk': 'https://www.youtube.com/playlist?list=PLnCmeDfRjs0KmGrVK9mDWLIM1kM-y3UXv',
        'rap': 'https://www.youtube.com/playlist?list=PLnCmeDfRjs0IGQVkf3wQoc15Mr-iH1zBN',
        'all': 'https://www.youtube.com/playlist?list=PLnCmeDfRjs0LwagG24PmxcK2S3uc1t2FT'
    }

    arg = sys.argv
    links = []
    typedl: str = 'audio'
    jump: int = 0
    to: int = 0

    match len(arg):
        case 1:
            [links.append(PLAYLISTS[key]) for key in PLAYLISTS]
        case 2:
            for key in PLAYLISTS:
                if (arg[-1] == key):
                    links.append(PLAYLISTS[key])
            if len(links) == 0:
                links.append(arg[-1])
        case 3:
            if arg[1].isdigit():
                jump = int(arg[1])
            else:
                typedl = arg[1]
        case 4:
            if arg[1].isdigit() and arg[2].isdigit():
                jump = int(arg[1])
                to = int(arg[2])
            else:
                typedl = arg[1]
                jump = int(arg[2])
        case 5:
            typedl = arg[1]
            jump = int(arg[2])
            to = int(arg[3])
    audio = True if typedl.lower() in ['audio', 'a', 'aux'] else False
    path = AUDIO_PATH if audio else VIDEO_PATH
    return Args(links, path, audio, jump, to)


if __name__ == '__main__':
    BANNER = """
__  __                 ____                      __                __   ______      __       
\ \/ /___  __  __     / __ \____ _      ______  / /___  ____ _____/ /  /_  __/_  __/ /_  ___ 
 \  / __ \/ / / /    / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  /    / / / / / / __ \/ _ \\
 / / /_/ / /_/ /    / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /    / / / /_/ / /_/ /  __/
/_/\____/\__,_/____/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/____/_/  \__,_/_.___/\___/ 
             /_____/                                            /_____/                      
    """
    os.system("cls")
    args = main()
    init(autoreset=True)
    print(Fore.MAGENTA + BANNER)
    print(Fore.RED + 'WAIT PLEASE. It can take some time before appearing something depending on number of video the playlist have and innternet connection speed')
    print('-'*100)
    for url in args.url:
        match isPlaylist(url):
            case None:
                print(Fore.RED + 'The URL is not from youtube')
                continue
            case False:
                tubes = Tubes(url, args.path)
            case True:
                playlistInfos(Playlist(url))
                tubes = getPlaylistTubes(Playlist(url), args)
        filesPath = [f for f in listdir(tubes[0].path) if isfile(join(tubes[0].path, f))]

        for c, tube in enumerate(tubes):
            print(f'[{c+1:^4}/{len(tubes):^4}] - ', end='')
            title = tube.title if len(tube.title) < 50 else tube.title[0:49] 
            print(f'{title:<50} |', end='')
            if isExist(filesPath, tube.title):
                print(Fore.YELLOW + 'Already Exist')
                continue
            tube.download(args.audio)
    print('-'*100)