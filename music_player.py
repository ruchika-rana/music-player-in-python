import os
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer
import time
import threading
from ttkthemes import themed_tk as tk

# root is the main window created by using tkinter library.
# ThemedTk tk is fn used of ttkthemes to give theme to the GUI window.
root = tk.ThemedTk()

# statusbar shows the current status of the app for eg. Playing Music.
statusbar = ttk.Label(root, text="Welcome to Music Player", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# menubar is used to create a menu bar which contains submenu i.e. buttons such as Files.
menubar = Menu(root)
root.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)

# playlist is the list of songs that are added to it by using Add button.
playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Full path + filename is required to play the music inside play_music function


# browse_file() fn is used to create a dialogue box to open a music file from a specific location.
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    PlaylistBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


# about_us() fn shows the description about the app using a messagebox
def about_us():
    tkinter.messagebox.showinfo('About Us', 'This is a music player app developed by Jay Jagani')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)

# initializes the mixer
mixer.init()

root.title('Harmony')
# iconbitmap is used to add a icon to the window of app
root.iconbitmap(r'Images/music_player.ico')

# Window(root) is divided into 2 parts: Right and Left using frames
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=10)

# PlaylistBox is used to create a space where playlist songs are added and displayed
PlaylistBox = Listbox(leftframe)
PlaylistBox.pack()

AddButton = ttk.Button(leftframe, text="+ ADD", command=browse_file)
AddButton.pack(side=LEFT)


def remove_song():
    selected_song = PlaylistBox.curselection()
    selected_song = int(selected_song[0])
    PlaylistBox.delete(selected_song)
    playlist.pop(selected_song)


RemoveButton = ttk.Button(leftframe, text="REMOVE", command=remove_song)
RemoveButton.pack()

rightframe = Frame(root)
rightframe.pack()

# Rightframe id further divided into 3 parts: TOP, MIDDLE, BOTTOM
# Topframe is created
topframe = Frame(rightframe)
topframe.pack()

# lengthlabel is used to show thw total length of the song
lengthLabel = ttk.Label(topframe, text='Total Length - --:--')
lengthLabel.pack(pady=10)

# currenttimeLabel is used to show the current time of the song playing
currenttimeLabel = ttk.Label(topframe, text='Current Time - --:--')
currenttimeLabel.pack()


def show_details(music):
    file_data = os.path.splitext(music)
    if file_data[1] == '.mp3':
        audio = MP3(music)
        total_length = audio.info.length
    else:
        a = mixer.sound(music)
        total_length = a.get_length()

    # div - total_length/60 and mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Playing " + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    Current_time = 0
    # mixer.get_busy() - Returns a False value when stop button is pressed or music is stopped.
    # continue - ignores all the statements below it. We check if the music is paused or not.
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(Current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimeLabel['text'] = "Current Time " + ' - ' + timeformat
            time.sleep(1)
            Current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = PlaylistBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File Opening Failed', "The Music Player could not found the file")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = False


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = False


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        unmute_btn.configure(image=unmute_photo)
        vol_contoller.set(50)
        muted = False
    else:
        mixer.music.set_volume(0)
        unmute_btn.configure(image=mute_photo)
        vol_contoller.set(0)
        muted = True


# Middleframe is created
middleframe = Frame(rightframe)
middleframe.pack(pady=10, padx=30)

# All functional buttons are created
play_photo = PhotoImage(file='Images/play.png')
play_btn = ttk.Button(middleframe, image=play_photo, command=play_music)
play_btn.grid(row=0, column=0, padx=10)

stop_photo = PhotoImage(file='Images/stop.png')
stop_btn = ttk.Button(middleframe, image=stop_photo, command=stop_music)
stop_btn.grid(row=0, column=1, padx=10)

pause_photo = PhotoImage(file='Images/pause.png')
pause_btn = ttk.Button(middleframe, image=pause_photo, command=pause_music)
pause_btn.grid(row=0, column=2, padx=10)

# Bottomframe is created
bottomframe = Frame(rightframe)
bottomframe.pack()

mute_photo = PhotoImage(file='Images/Mute.png')
unmute_photo = PhotoImage(file='Images/Unmute.png')
unmute_btn = ttk.Button(bottomframe, image=unmute_photo, command=mute_music)
unmute_btn.grid(row=0, column=0)

# Volume Controller is created
vol_contoller = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
vol_contoller.set(50)
mixer.music.set_volume(50)
vol_contoller.grid(row=0, column=1, pady=15, padx=30)


# on_closing fn is used to stop the threading i.e. playing music, if it is, before closing the app.
def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
