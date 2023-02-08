from codecs import latin_1_decode
from email.policy import strict
from importlib.resources import path
from operator import index
from  tkinter import *
from tkinter.filedialog import askdirectory
from tokenize import String
from turtle import bgcolor, width
import pygame
import os
import pathlib

class MusicPlayer(Frame):
    def __init__(self, master):
        super(MusicPlayer, self).__init__(master)

        # propting user to choose music directory
        self.directory = askdirectory()

        # channging working directory into music directory where user input
        os.chdir(self.directory)

        # acceptable audio extentions
        valid_extentions = [".mpc",  ".3gp",  ".aa",  ".aac",  ".aax",  ".act",  ".aiff",  ".alac",  ".amr", ".ape",  ".au", ".awb", ".dss",
        ".dvf", ".flac",  ".gsm", ".iklax", ".ivs", ".m4a", ".m4b", ".m4p", ".mmf", ".mp3", ".msv", ".nmf", ".ogg", ".oga",
        ".mogg", ".opus", ".ra", ".rm", ".raw", ".rf64", ".sln", ".tta", ".voc", ".vox", ".wav", ".wma", ".wv", ".webm",
        ".8svx", ".cda"]

        # creating a variable where musics from music directory will be assigned to
        self.song_list = os.listdir()

        # creating playlist of songs
        self.playlist = Listbox(self, font="Helvetica, 12 bold", bg="yellow", selectmode=SINGLE)

        # inserting each song from song_list directory into playlist one at a time
        for self.song in self.song_list:
 
        # accepting only files with valid extentions
            if pathlib.Path(self.song).suffix in valid_extentions:
 
                # position of 1st song in playlist Listbox
                self.pos = 0
                self.playlist.insert(self.pos, self.song)

                # updating each new song postion as next position
                self.pos += 1

        # audio file names in playlist
        self.files_playlist = self.playlist.get(first=0, last="end")

        # len of playlist
        self.len_playlist = IntVar()
        self.len_playlist.set(len(self.files_playlist))

        # current song index in playlist
        self.index_song = IntVar() 

        self.grid()

        # pause-unpause button label change
        self.pause = StringVar()
        self.pause.set("PAUSE")

        # controlling pause-unpause change
        self.un_pause_control = IntVar()
        self.un_pause_control.set(0)

        # initilazing pygame and pygame mixer
        pygame.init()   
        pygame.mixer.init()

        self.display_currentsong()

        # function to create button
        self.create_buttons()

    def create_buttons(self):
        # creating button widgets

        # play button widget
        self.button_play = Button(self, width=5, height=3, font="Helvetica  12 bold", text="PLAY",
                            command=self.play, bg="red", fg="white", bd="10", relief="groove").grid(row=1, column=1, ipadx=70)

        # stop button
        self.button_exit = Button(self, width=5, height=3, font="Helvetica  12 bold", text="STOP",
                            command=self.ExitMusicPlayer, bg="purple", fg="white", bd="9", relief="groove").grid(row=2, column=1)

        # pause-unpause button
        self.button_pause_unpause = Button(self, width=5, height=3, font="Helvetica  12 bold", textvariable=self.pause,
                            command=self.pause_unpause, bg="purple", fg="white", bd="9", relief="groove").grid(row=0, column=1)

        # next song button
        self.button_next = Button(self, width=5, height=3, font="Helvetica  12 bold", text="NEXT",
                            command=self.next, bg="green", fg="white", bd="9", relief="groove").grid(row=1, column=2)

        # previous song button
        self.button_previous = Button(self, width=5, height=3, font="Helvetica  12 bold", text="PREVIOUS",
                            command=self.previous, bg="green", fg="white", bd="9", relief="groove").grid(row=1, column=0)
        
    # button functions
        
    # play song function
    def play(self):
        # setting current playing index of song
        self.index_song.set(self.files_playlist.index(self.playlist.get(ACTIVE)))

        # controllling steamed auido and loading a muisc file for playback
        # ACTIVE refers active state of the file that is selected when cursor move on
        pygame.mixer.music.load(self.playlist.get(ACTIVE))

        # whichever song from playlist chosen, set it active state
        self.var.set(self.playlist.get(ACTIVE))

        # plays chosen song
        pygame.mixer.music.play()

    # stopping music player function
    def ExitMusicPlayer(self):
        pygame.mixer.music.stop()

    # pausing-unpasing music function
    def pause_unpause(self):
        # pausing
        if self.un_pause_control.get() == 0:
            self.un_pause_control.set((self.un_pause_control.get()+1)%2)
            pygame.mixer.music.pause()
            self.pause.set("UNPAUSE")

        else:
            # unpausing
            self.un_pause_control.set((self.un_pause_control.get()+1)%2)
            pygame.mixer.music.unpause()
            self.pause.set("PAUSE")

    # next song function
    def next(self):
        # setting next song index
        self.index_song.set((self.index_song.get()+1)%self.len_playlist.get())
        
        # selecting related song to play
        pygame.mixer.music.load(self.files_playlist[self.index_song.get()])

        # setting displayed song name as next song
        self.var.set(self.files_playlist[self.index_song.get()])

        # plays chosen song
        pygame.mixer.music.play()

    # previous song function
    def previous(self):
        # setting next song index
        self.index_song.set((self.index_song.get()-1)%self.len_playlist.get())
        
        # selecting related song to play
        pygame.mixer.music.load(self.files_playlist[self.index_song.get()])

        # # setting displayed song name as previous song
        self.var.set(self.files_playlist[self.index_song.get()])

        # plays chosen song
        pygame.mixer.music.play()

    # displaying current running song function
    def display_currentsong(self):
        # display current running song
        self.var = StringVar()
        songtitle = Label(self, font="Helvetica 12 bold", textvariable=self.var, bg="light blue", fg="black", bd="9", relief="groove", anchor=CENTER, width=30)
        songtitle.grid(row=3, column=1) 
        self.playlist.grid(row=4, column=1)


# top-up windows
root = Tk()

# unresizable windows
root.resizable(height=False, width=False)

# title of app
root.title("music player")

# size of app main windows
root.geometry("426x450")

# instanting app
app = MusicPlayer(root)

mainloop()

                