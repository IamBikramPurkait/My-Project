from tkinter import *
from pygame import mixer
from tkinter import filedialog
import os


def play():
    mixer.music.load(playlistbox.get(ACTIVE))

    mixer.music.play()
    status.set('Playng')

def stop():
    mixer.music.stop()
    status.set('Stop')

def pause():
    mixer.music.pause()
    status.set('Pause')


def unpause():
    mixer.music.unpause()
    status.set('UnPause')

def prev_song():
    mixer.music.load(songtracks[0]-1)
    mixer.music.play()

def next_song():
    mixer.music.load(songtracks[0]+1)
    mixer.music.play()

def mute():
    mixer.music.unpause()
    status.set('UnPause')


def loadmusic():
    dir_=filedialog.askdirectory(initialdir='D:\\',title='Select Directory')
    os.chdir(dir_)
    status.set('Playlist Updated.')
    dir_files = os.listdir(dir_)
    for file in dir_files:
        playlistbox.insert(END,file)







mixer.init()
root=Tk()



root.title("Musicolet")
root.geometry('800x500')
root.resizable(height = False, width = False)
root.iconbitmap("icon/icon.ico")

status = StringVar()

songtrack_frm=LabelFrame(master=root,text="Song Track")
songtrack_frm.place(x=0,y=0,width=350,height=350)



playlist_frm=LabelFrame(master=root,text="Playlist")
playlist_frm.place(x=350,y=0,width=450,height=350)


control_frm=LabelFrame(master=root,text="Control Bar")
control_frm.place(x=0,y=350,width=800,height=110)


status_frm=LabelFrame(master=root,text="Song Status")
status_frm.place(x=0,y=460,width=800,height=40)









play_image=PhotoImage(file = "icon/play.png")
playbtn=Button(control_frm,text="Play",command=play,image=play_image)
playbtn.grid(row=1,column=1)

unpause_image=PhotoImage(file = "icon/play.png")
unpause_btn=Button(control_frm,text="UnPause",command=unpause,image=unpause_image)
unpause_btn.grid(row=1,column=3)

pause_image=PhotoImage(file = "icon/pause.png")
pausebtn=Button(control_frm,text="Pause",command=pause,image=pause_image)
pausebtn.grid(row=1,column=0)

stop_image=PhotoImage(file = "icon/stop.png")
stopbtn=Button(control_frm,text="Stop",command=stop,image=stop_image)
stopbtn.grid(row=1,column=2)

prev_image=PhotoImage(file = "icon/prev.png")
prevbtn=Button(control_frm,text="Prev",command=prev_song,image=prev_image)
prevbtn.grid(row=1,column=4)

next_image=PhotoImage(file = "icon/next.png")
nextbtn=Button(control_frm,text="Next",command=next_song,image=next_image)
nextbtn.grid(row=1,column=5)

mute_image=PhotoImage(file = "icon/mute.png")
mutebtn=Button(control_frm,text="Mute",command=mute,image=mute_image)
mutebtn.grid(row=1,column=6)



loadbtn=Button(playlist_frm,text="Load Music",command=loadmusic)
loadbtn.pack()


y_scroll=Scrollbar(playlist_frm,orient=VERTICAL)

playlistbox=Listbox(playlist_frm,yscrollcommand=y_scroll.set,height=350)

y_scroll.pack(side=RIGHT,fill=Y)
y_scroll.config(command=playlistbox.yview)

playlistbox.pack(fill=BOTH)



# os.chdir("Music")
# songtracks = os.listdir()

# for track in songtracks:
#     playlistbox.insert(END,track)


















status_lbl=Label(status_frm,textvariable=status)
status_lbl.pack()




root.mainloop()


