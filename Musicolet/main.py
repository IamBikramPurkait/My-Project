from tkinter import *
from tkinter import ttk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import messagebox as mb
from PIL import ImageTk, Image
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
    dir_files = os.listdir(dir_)
    for file in dir_files:
        for ex in extension:
            if file.split('.')[-1] == ex:
                playlistbox.insert(END, file.replace('.mp3', ''))
                songs.append(file)
                status.set('Playlist Updated')


def fileselect():
    song = filedialog.askopenfilename(
        initialdir='audio/', title="Choose A Song")
    os.chdir(os.path.dirname(song))
    song = song.split('/')[-1]
    song = song.replace(".mp3", "")
    playlistbox.insert(END, song)
    songs.append(f'{song}.mp3')


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
            show_detail(file)

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
    show_detail(file)


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
    show_detail(file)


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
        image = makealbumartimage('temp.jpg')
        album_art_label.configure(image=image)
        album_art_label.image = image



def makealbumartimage(image_path):
    image = Image.open(image_path)
    image = image.resize((290, 270), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


def about():
    mb.showinfo('Musicolet', 'It is the basic music player with some advance feature made in Python.😎\nIt is created by Bikram Purkait with ❤.\nIt is completed on 02/03/2021.\nThanks for using the application.👍')


def shortcut_key():
    mb.showinfo('Shortcut Key','1> Select a Folder - ctrl + o\n2> Select a File - ctrl + l\n3> Delete a song - Delete\n4> Delete all song - ctrl + Delete\n5> Exit - e\n6> Play/Pause - Spacebar\n7> Select and Play Song - Double Click Left Mouse Button\n8> Prev Song - Up Arrow\n9> Next Song - Down Arrow\n10> Stop - s\n11> Mute - m ')

def exit_fun(event):
    stop()
    exit()


def repeat():
    status.set('Feature Coming Soon.Please Stay with Us.')



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
filemenu.add_command(label='Folder Select - ctrl + o',font='Helvetica 10 bold', command=loadmusic)
filemenu.add_command(label='File Select - ctrl + l',font='Helvetica 10 bold',  command=fileselect)
filemenu.add_separator()
filemenu.add_command(label='Delete a Song - Delete',font='Helvetica 10 bold',  command=delete_song)
filemenu.add_command(label='Delete all song - ctrl + Delete',font='Helvetica 10 bold',  command=delete_allsong)
filemenu.add_separator()
filemenu.add_command(label='Exit - e',font='Helvetica 10 bold',  command=exit)

mainmenu.add_cascade(label='File', menu=filemenu)
aboutmenu = Menu(mainmenu, tearoff=0)
mainmenu.add_command(label='About', command=about)
mainmenu.add_command(label='Shortcut Key', command=shortcut_key)

root.config(menu=mainmenu)


# Create LabelFrame
songtrack_frm = LabelFrame(master=root, text="Song Track",font='Helvetica 11 bold italic',fg='indian red')
songtrack_frm.place(x=0, y=0, width=350, height=350)


playlist_frm = LabelFrame(master=root, text="Playlist",font='Helvetica 11 bold italic',fg='peachpuff4')
playlist_frm.place(x=350, y=0, width=450, height=350)


control_frm = LabelFrame(master=root, text="Control Bar",font='Helvetica 11 bold italic',fg='blue')
control_frm.place(x=0, y=350, width=800, height=110)


status_frm = LabelFrame(master=root, text="Song Status",font='Helvetica 11 bold italic',fg='DarkOrange4')
status_frm.place(x=0, y=460, width=800, height=40)

s = ttk.Style()
s.configure('TButton', font='Helvetica 10 bold italic')
# Create PlaylistBox and set vertical scroll and add load button
loadbtn = ttk.Button(playlist_frm, text="Load Music", command=loadmusic,style='TButton')
loadbtn.pack()


def load_fun(event):
    loadmusic()

def file_select_fun(event):
    fileselect()

def delete_song_fun(event):
    delete_song()

def delete_all_song_fun(event):
    delete_allsong()

def mute_key_fun(event):
    mute_fun()


root.bind('<Control-o>', load_fun)
root.bind('<Control-l>', file_select_fun)
root.bind('<Delete>', delete_song_fun)
root.bind('<Control-Delete>', delete_all_song_fun)
root.bind('<e>', exit_fun)
root.bind('<m>', mute_key_fun)


x_scroll = ttk.Scrollbar(playlist_frm, orient=HORIZONTAL)
y_scroll = ttk.Scrollbar(playlist_frm, orient=VERTICAL)
playlistbox = Listbox(playlist_frm, yscrollcommand=y_scroll.set,
                      xscrollcommand=x_scroll.set, height=350,font='Helvetica 10 italic',fg='purple4')
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
album_art_label.place(x=25, y=25)


# Creating Button
playbtn = Button(control_frm, command=play, image=play_image, bd=0)
playbtn.place(x=350, y=5)


def on_enter_play(event):
    play_des.place(x=325, y=35)


def on_leave_play(event):
    play_des.place(x=1000, y=1000)


def play_fun(event):
    if event.char == ' ':
        play()


def play_fun_doublebutton(event):
    stop()
    play()


playbtn.bind('<Enter>', on_enter_play)
playbtn.bind('<Leave>', on_leave_play)
root.bind('<Key>', play_fun)
root.bind('<Double-Button-1>', play_fun_doublebutton)


prevbtn = Button(control_frm, image=prev_image, bd=0, command=prev_song)
prevbtn.place(x=300, y=0)


def prev_fun(event):
    prev_song()


def on_enter_prev(event):
    prev_des.place(x=290, y=35)


def on_leave_prev(event):
    prev_des.place(x=1000, y=1000)


prevbtn.bind('<Enter>', on_enter_prev)
prevbtn.bind('<Leave>', on_leave_prev)
root.bind('<Up>', prev_fun)


nextbtn = Button(control_frm, image=next_image, bd=0, command=next_song)
nextbtn.place(x=380, y=0)


def next_fun(event):
    next_song()


def on_enter_next(event):
    next_des.place(x=365, y=35)


def on_leave_next(event):
    next_des.place(x=1000, y=1000)


nextbtn.bind('<Enter>', on_enter_next)
nextbtn.bind('<Leave>', on_leave_next)
root.bind('<Down>', next_fun)


stopbtn = Button(control_frm, command=stop, image=stop_image, bd=0)
stopbtn.place(x=425, y=5)


def stop_fun(event):
    stop()


def on_enter_stop(event):
    stop_des.place(x=410, y=35)


def on_leave_stop(event):
    stop_des.place(x=1000, y=1000)


stopbtn.bind('<Enter>', on_enter_stop)
stopbtn.bind('<Leave>', on_leave_stop)
root.bind('<s>', stop_fun)


vol_btn = Button(control_frm, command=mute_fun, image=vol_image, bd=0)
vol_btn.place(x=600, y=10)


def on_enter_vol(event):
    vol_des.place(x=595, y=35)


def on_leave_vol(event):
    vol_des.place(x=1000, y=1000)


vol_btn.bind('<Enter>', on_enter_vol)
vol_btn.bind('<Leave>', on_leave_vol)


repeat_btn = Button(control_frm, image=repeat_image, bd=0, command=repeat)
repeat_btn.place(x=265, y=7)


def on_enter_repeat(event):
    repeat_des.place(x=255, y=35)


def on_leave_repeat(event):
    repeat_des.place(x=1000, y=1000)


repeat_btn.bind('<Enter>', on_enter_repeat)
repeat_btn.bind('<Leave>', on_leave_repeat)


global volume_bar
volume_bar = ttk.Scale(control_frm, from_=0, to=100,
                       orient=HORIZONTAL, command=set_volume)
volume_bar.set(70)
mixer.music.set_volume(0.7)
volume_bar.place(x=630, y=8)


# Time Durations
global dur_start, dur_end
dur_start = Label(control_frm, text='00:00',font='Helvetica 11 bold italic',fg='dark violet')
dur_start.place(x=80, y=50)
dur_end = Label(control_frm, text='00:00',font='Helvetica 11 bold italic',fg='dark violet')
dur_end.place(x=650, y=50)


status_lbl = Label(status_frm, textvariable=status,font='Helvetica 11 bold italic',fg='dark green')
status_lbl.pack()


global myscroll
myscroll = ttk.Scale(control_frm, from_=0, to=100,
                     orient=HORIZONTAL, length=500)
myscroll.place(x=130, y=50)
myscrolllabel = Label(control_frm, text='')
myscrolllabel.place(x=400, y=70)


play_des = Label(control_frm, text='Play/Pause', relief='groove')
stop_des = Label(control_frm, text='Stop Music', relief='groove')
prev_des = Label(control_frm, text='Previous Track', relief='groove')
next_des = Label(control_frm, text='Next Track', relief='groove')
vol_des = Label(control_frm, text='Mute', relief='groove')
repeat_des = Label(control_frm, text='Repeat', relief='groove')


root.mainloop()
