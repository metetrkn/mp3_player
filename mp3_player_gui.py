import os
import pathlib
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory

class MusicPlayer(Frame):
    def __init__(self, master):
        super(MusicPlayer, self).__init__(master)

        # Prompt user to choose music directory
        self.directory = askdirectory()

        # Change working directory to the chosen music directory
        os.chdir(self.directory)

        # List valid audio extensions
        valid_extentions = [".mpc",  ".3gp",  ".aa",  ".aac",  ".aax",  ".act",  ".aiff",  ".alac",  ".amr", ".ape",  ".au", ".awb", ".dss",
        ".dvf", ".flac",  ".gsm", ".iklax", ".ivs", ".m4a", ".m4b", ".m4p", ".mmf", ".mp3", ".msv", ".nmf", ".ogg", ".oga",
        ".mogg", ".opus", ".ra", ".rm", ".raw", ".rf64", ".sln", ".tta", ".voc", ".vox", ".wav", ".wma", ".wv", ".webm",
        ".8svx", ".cda"]

        # Assign music files from the chosen directory to self.song_list
        self.song_list = os.listdir()

        # Create a playlist of songs
        self.playlist = Listbox(self, font="Helvetica, 12 bold", bg="yellow", selectmode=SINGLE)

        # Insert each song from song_list directory into the playlist
        for self.song in self.song_list:
 
            # Accept only files with valid extensions
            if pathlib.Path(self.song).suffix in valid_extentions:
 
                # Position of the 1st song in playlist Listbox
                self.pos = 0
                self.playlist.insert(self.pos, self.song)

                # Update each new song position as next position
                self.pos += 1

        # Audio file names in the playlist
        self.files_playlist = self.playlist.get(first=0, last="end")

        # Length of the playlist
        self.len_playlist = IntVar()
        self.len_playlist.set(len(self.files_playlist))

        # Current song index in the playlist
        self.index_song = IntVar() 

        self.grid()

        # Pause and Unpause button label change
        self.pause = StringVar()
        self.pause.set("PAUSE")

        # Control pause and unpause change
        self.un_pause_control = IntVar()
        self.un_pause_control.set(0)

        # Initialize pygame and pygame mixer
        pygame.init()   
        pygame.mixer.init()

        self.display_currentsong()

        # Function to create buttons
        self.create_buttons()

    def create_buttons(self):
        # Create button widgets

        # Play button widget
        self.button_play = Button(self, width=5, height=3, font="Helvetica  12 bold", text="PLAY",
                            command=self.play, bg="red", fg="white", bd="10", relief="groove").grid(row=1, column=1, ipadx=70)

        # Stop button
        self.button_exit = Button(self, width=5, height=3, font="Helvetica  12 bold", text="STOP",
                            command=self.ExitMusicPlayer, bg="purple", fg="white", bd="9", relief="groove").grid(row=2, column=1)

                # Pause and Unpause button
        self.button_pause_unpause = Button(self, width=5, height=3, font="Helvetica  12 bold", textvariable=self.pause,
                            command=self.pause_unpause, bg="purple", fg="white", bd="9", relief="groove").grid(row=0, column=1)

        # Next song button
        self.button_next = Button(self, width=5, height=3, font="Helvetica  12 bold", text="NEXT",
                            command=self.next, bg="green", fg="white", bd="9", relief="groove").grid(row=1, column=2)

        # Previous song button
        self.button_previous = Button(self, width=5, height=3, font="Helvetica  12 bold", text="PREVIOUS",
                            command=self.previous, bg="green", fg="white", bd="9", relief="groove").grid(row=1, column=0)
        
    # Button functions
        
    # Play song function
    def play(self):
        # Set current playing index of song
        self.index_song.set(self.files_playlist.index(self.playlist.get(ACTIVE)))

        # Load a music file for playback
        pygame.mixer.music.load(self.playlist.get(ACTIVE))

        # Set the chosen song to active state
        self.var.set(self.playlist.get(ACTIVE))

        # Play the chosen song
        pygame.mixer.music.play()

    # Stop music player function
    def ExitMusicPlayer(self):
        pygame.mixer.music.stop()

    # Pause and Unpause music function
    def pause_unpause(self):
        # Pause
        if self.un_pause_control.get() == 0:
            self.un_pause_control.set((self.un_pause_control.get()+1)%2)
            pygame.mixer.music.pause()
            self.pause.set("UNPAUSE")

        else:
            # Unpause
            self.un_pause_control.set((self.un_pause_control.get()+1)%2)
            pygame.mixer.music.unpause()
            self.pause.set("PAUSE")

    # Next song function
    def next(self):
        # Set next song index
        self.index_song.set((self.index_song.get()+1)%self.len_playlist.get())
        
        # Select related song to play
        pygame.mixer.music.load(self.files_playlist[self.index_song.get()])

        # Set displayed song name as next song
        self.var.set(self.files_playlist[self.index_song.get()])

        # Play chosen song
        pygame.mixer.music.play()

    # Previous song function
    def previous(self):
        # Set previous song index
        self.index_song.set((self.index_song.get()-1)%self.len_playlist.get())
        
        # Select related song to play
        pygame.mixer.music.load(self.files_playlist[self.index_song.get()])

        # Set displayed song name as previous song
        self.var.set(self.files_playlist[self.index_song.get()])

        # Play chosen song
        pygame.mixer.music.play()

    # Display current running song function
    def display_currentsong(self):
        # Display current running song
        self.var = StringVar()
        songtitle = Label(self, font="Helvetica 12 bold", textvariable=self.var, bg="light blue", fg="black", bd="9", relief="groove", anchor=CENTER, width=30)
        songtitle.grid(row=3, column=1) 
        self.playlist.grid(row=4, column=1)


# Top-up window
root = Tk()

# Unresizable window
root.resizable(height=False, width=False)

# App title
root.title("Music Player")

# Main window size
root.geometry("490x450")

# instanting app
app = MusicPlayer(root)

mainloop()


