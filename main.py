from pytube import YouTube, Playlist
from colorama import Fore, init
import sys
import os


class Args:
    def __init__(self, url, path, audio, jump, to):
        self.url    = url
        self.path   = path
        self.audio  = audio
        self.jump   = jump
        self.to     = to

    def debug(self):
        print(Fore.MAGENTA + f'Path: {self.path}\nAudio: {self.audio} | Jump: {self.jump} | To: {self.to}\n{self.url}')

class Tubes:
    def __init__(self, ytb:YouTube, path, audio):
        self.ytb        = ytb.streams.get_audio_only() if audio else ytb.streams.get_highest_resolution()
        self.title      = ytb.title
        self.path       = path

    def debug(self):
        print('---')

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

def getPlaylistTubes(playlist:Playlist, args:Args):
    temp = list(playlist.videos)
    pl_title = playlist.title
    if (args.jump > 0):
        del temp[0:args.jump-1]
    if (args.to > 0):
        del temp[args.to-args.jump+1:]
    return [Tubes(i, args.path + pl_title, args.audio) for i in temp]



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
    os.system("cls")
    args = main()
    init(autoreset=True)
    print(Fore.CYAN + 'You_Download_Tubes')

    for url in args.url:
        match isPlaylist(url):
            case None:
                print(Fore.RED + 'The URL is not from youtube')
            case False:
                print()
            case True:
                tubes = getPlaylistTubes(Playlist(url), args)
                for tube in tubes:
                    print()


