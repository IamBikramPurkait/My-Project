from tkinter import *
from tkinter import ttk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import messagebox as mb
from tkinter import filedialog
import os
import time


playing = False
paused = False
mute = False
current_time = 0
total_time = 0
current_time_converted = 0

songs = []
file = ''


def loadmusic():
    extension = ['mp3', 'wav', 'mpeg', 'm4a', 'wma', 'ogg']
    global songs, dir_
    dir_ = filedialog.askdirectory(
        initialdir='Desktop', title='Select Directory')
    os.chdir(dir_)
    status.set('Playlist Updated')
    dir_files = os.listdir(dir_)
    for file in dir_files:
        for ex in extension:
            if file.split('.')[-1] == ex:
                playlistbox.insert(END, file.replace('.mp3', ''))
                songs.append(file)


def fileselect():
    song = filedialog.askopenfilename(initialdir='audio/',title="Choose A Song")
    song = song.replace(".mp3", "")
    playlistbox.insert(END, song)




def play():
    global playing
    global paused

    try:
        if playing == False:
            global file
            file = playlistbox.get(ACTIVE)
            file = f"{file}.mp3"
            mixer.music.load(file)
            mixer.music.play()
            status.set('Playng - '+str(file.split('.mp3')[0]))
            playbtn['image'] = pause_image
            playing = True
            # show_detail(file)

        else:
            if paused == True:
                mixer.music.unpause()
                status.set('Playng - '+str(file.split('.mp3')[0]))
                playbtn['image'] = pause_image
                paused = False
            else:
                mixer.music.pause()
                status.set('Music Paused')
                playbtn['image'] = play_image
                paused = True

        play_time()

    except:
        mb.showerror('error', 'No file found to play.')


def play_time():
    current_time = mixer.music.get_pos()/1000
    current_time_converted = time.strftime('%M:%S', time.gmtime(current_time))
    dur_start.config(text=current_time_converted)
    myscroll.config(value=int(current_time))

    dur_start.after(1000, play_time)
    global file
    song = MP3(file)
    global total_time
    total_time = song.info.length
    total_time_converted = time.strftime('%M:%S', time.gmtime(total_time))
    dur_end.config(text=total_time_converted)

    slider_pos = int(total_time)
    myscroll.config(to=slider_pos)


def stop():
    global playing, dur_start
    mixer.music.stop()
    playing = False
    playbtn['image'] = play_image
    playlistbox.selection_clear(ACTIVE)
    status.set('Music Stopped')
    dur_start.config(text='00:00')


def prev_song():
    global songs
    global file
    index = songs.index(file)-1
    file = songs[index]
    mixer.music.load(file)
    mixer.music.play()
    status.set('Playng - '+str(file.split('.mp3')[0]))
    playlistbox.selection_clear(0, END)
    playlistbox.activate(index)
    playlistbox.selection_set(index, last=None)
    # show_detail(file)


def next_song():
    global file
    global songs
    index = songs.index(file)+1
    file = songs[index]
    mixer.music.load(file)
    mixer.music.play()
    status.set('Playng - '+str(file.split('.mp3')[0]))
    playlistbox.selection_clear(0, END)
    playlistbox.activate(index)
    playlistbox.selection_set(index, last=None)
    # show_detail(file)


def mute_fun():
    global mute

    if mute == False:
        mixer.music.set_volume(0.0)
        status.set('Music Mute')
        vol_btn['image'] = mute_image
        mute = True
    else:

        mixer.music.set_volume(1.0)
        vol_btn['image'] = vol_image
        status.set('Playng  -'+str(file.split('.mp3')[0]))
        mute = False


def set_volume(num):
    volume = volume_bar.get()/100
    mixer.music.set_volume(float(volume))


def delete_song():
    status.set('Song Deleted')
    playlistbox.delete(ANCHOR)
    mixer.music.stop()
    playlistbox.selection_clear(ANCHOR)


def delete_allsong():
    status.set('All song deleted')
    playlistbox.delete(0, END)
    mixer.music.stop()


def show_detail(play_song):
    with open('temp.jpg', 'wb') as img:
        a = ID3(play_song)
        img.write(a.getall('APIC')[0].data)
        image = makeAlbumArtImage('temp.jpg')
        album_art_label.configure(image=image)
        album_art_label.image = image


def makeAlbumArtImage(image_path):
    image = Image.open(image_path)
    image = image.resize((150, 150), Image.ANTIALIAS)
    return PhotoImage(image)


def about():
    mb.showinfo('Musicolet', 'It is the basic music player with some advance feature made in Python.😎\nIt is created by Bikram Purkait with ❤.\nIt is completed on 01/03/2021.\nThanks for using the application.👍')


def shortcut_key():
    pass


# Main Gui
mixer.init()
root = Tk()


# Initial Work
root.title("Musicolet")
root.geometry('800x520')
root.resizable(height=False, width=False)
root.iconbitmap("icon/icon.ico")

status = StringVar()
status.set('❤Welcome to you in Musiocolet❤')

# create a menubar
mainmenu = Menu(root, tearoff=0)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label='Folder Select', command=loadmusic)
filemenu.add_command(label='File Select', command=fileselect)
filemenu.add_separator()
filemenu.add_command(label='Delete Song', command=delete_song)
filemenu.add_command(label='Delete all song', command=delete_allsong)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit)

mainmenu.add_cascade(label='File', menu=filemenu)
aboutmenu = Menu(mainmenu, tearoff=0)
mainmenu.add_command(label='About', command=about)
mainmenu.add_command(label='Shortcut Key', command=shortcut_key)

root.config(menu=mainmenu)


# Create LabelFrame
songtrack_frm = ttk.LabelFrame(master=root, text="Song Track")
songtrack_frm.place(x=0, y=0, width=350, height=350)


playlist_frm = ttk.LabelFrame(master=root, text="Playlist")
playlist_frm.place(x=350, y=0, width=450, height=350)


control_frm = ttk.LabelFrame(master=root, text="Control Bar")
control_frm.place(x=0, y=350, width=800, height=110)


status_frm = ttk.LabelFrame(master=root, text="Song Status")
status_frm.place(x=0, y=460, width=800, height=40)


# Create PlaylistBox and set vertical scroll and add load button
loadbtn = ttk.Button(playlist_frm, text="Load Music", command=loadmusic)
loadbtn.pack()


x_scroll = ttk.Scrollbar(playlist_frm, orient=HORIZONTAL)
y_scroll = ttk.Scrollbar(playlist_frm, orient=VERTICAL)
playlistbox = Listbox(playlist_frm, yscrollcommand=y_scroll.set,
                      xscrollcommand=x_scroll.set, height=350)
x_scroll.pack(side=BOTTOM, fill=X)
y_scroll.pack(side=RIGHT, fill=Y)
x_scroll.config(command=playlistbox.xview)
y_scroll.config(command=playlistbox.yview)
playlistbox.pack(fill=BOTH)


# Creating image for buttons
pause_image = PhotoImage(file="icon/pause.png")
mute_image = PhotoImage(file="icon/mute.png")
vol_image = PhotoImage(file="icon/vol.png")
play_image = PhotoImage(file="icon/play.png")
prev_image = PhotoImage(file="icon/prev.png")
next_image = PhotoImage(file="icon/next.png")
stop_image = PhotoImage(file="icon/stop.png")
repeat_image = PhotoImage(file="icon/repeat.png")
repeat_one_image = PhotoImage(file="icon/repeat_one.png")
shuffle_image = PhotoImage(file="icon/shuffle.png")


album_art_label = Label(songtrack_frm)
album_art_label.place(x=0, y=0)

# Creating Button
playbtn = Button(control_frm, command=play, image=play_image, bd=0)
playbtn.place(x=350, y=5)

prevbtn = Button(control_frm, image=prev_image, bd=0, command=prev_song)
prevbtn.place(x=300, y=0)

nextbtn = Button(control_frm, image=next_image, bd=0, command=next_song)
nextbtn.place(x=380, y=0)

stopbtn = Button(control_frm, command=stop, image=stop_image, bd=0)
stopbtn.place(x=425, y=5)

vol_btn = Button(control_frm, command=mute_fun, image=vol_image, bd=0)
vol_btn.place(x=600, y=10)

repeat_btn = Button(control_frm, image=repeat_image, bd=0)
repeat_btn.place(x=265, y=7)

global volume_bar
volume_bar = ttk.Scale(control_frm, from_=0, to=100,
                       orient=HORIZONTAL, command=set_volume)
volume_bar.set(70)
mixer.music.set_volume(0.7)
volume_bar.place(x=630, y=8)


# Time Durations
global dur_start, dur_end
dur_start = ttk.Label(control_frm, text='00:00')
dur_start.place(x=80, y=50)
dur_end = ttk.Label(control_frm, text='00:00')
dur_end.place(x=650, y=50)


status_lbl = Label(status_frm, textvariable=status)
status_lbl.pack()


global myscroll
myscroll = ttk.Scale(control_frm, from_=0, to=100,
                     orient=HORIZONTAL, length=500)
myscroll.place(x=130, y=50)
myscrolllabel = Label(control_frm, text='')
myscrolllabel.place(x=400, y=70)


root.mainloop()
