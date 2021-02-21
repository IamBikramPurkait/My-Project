from tkinter import *
from tkinter import ttk
from pygame import mixer
from tkinter import messagebox as mb
from tkinter import filedialog
import os



playing = False
paused = False
mute = False










def play():
    global playing
    global paused
    try:
        if playing==False:
            global file
            file=playlistbox.get(ACTIVE)
            mixer.music.load(file)
            mixer.music.play()
            status.set('Playng -'+str(file.split('.mp3')[0]))
            playbtn['image']=pause_image
            playing = True
        else:
            if paused == True:
                mixer.music.unpause()
                status.set('Playng again  -'+str(file.split('.mp3')[0]))
                playbtn['image']=pause_image
                paused = False
            else:
                mixer.music.pause()
                status.set('Music Paused')
                playbtn['image']=play_image
                paused = True
    except:
        mb.showerror('error','No file found to play.')







    

def stop():
    global playing
    mixer.music.stop()
    status.set('Music Stopped')
    playing = False
    playbtn['image']=play_image


def prev_song():
    mixer.music.load(songtracks[0]-1)
    mixer.music.play()

def next_song():
    mixer.music.load(songtracks[0]+1)
    mixer.music.play()



def loadmusic():
    dir_=filedialog.askdirectory(initialdir='Desktop',title='Select Directory')
    os.chdir(dir_)
    status.set('Playlist Updated.')
    dir_files = os.listdir(dir_)
    for file in dir_files:
        playlistbox.insert(END,file)


def mute_fun():
    global mute
    
    if mute == False:
        mixer.music.set_volume(0.0)
        status.set('Music Mute')
        vol_btn['image']=mute_image
        mute = True
    else:
        
        mixer.music.set_volume(1.0)
        vol_btn['image']=vol_image
        status.set('Playng  -'+str(file.split('.mp3')[0]))
        mute = False




def set_volume(num):
    volume=volume_bar.get()
    mixer.music.set_volume(float(volume/100))



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







loadbtn=Button(playlist_frm,text="Load Music",command=loadmusic)
loadbtn.pack()


y_scroll=Scrollbar(playlist_frm,orient=VERTICAL)

playlistbox=Listbox(playlist_frm,yscrollcommand=y_scroll.set,height=350)

y_scroll.pack(side=RIGHT,fill=Y)
y_scroll.config(command=playlistbox.yview)

playlistbox.pack(fill=BOTH)







pause_image=PhotoImage(file = "icon/pause.png")
mute_image=PhotoImage(file = "icon/mute.png")



play_image=PhotoImage(file = "icon/play.png")
playbtn=Button(control_frm,text="Play",command=play,image=play_image)
playbtn.grid(row=1,column=1)

stop_image=PhotoImage(file = "icon/stop.png")
stopbtn=Button(control_frm,text="Stop",command=stop,image=stop_image)
stopbtn.grid(row=1,column=2)


prev_image=PhotoImage(file = "icon/prev.png")
prevbtn=Button(control_frm,text="Prev",command=prev_song,image=prev_image)
prevbtn.grid(row=1,column=4)

next_image=PhotoImage(file = "icon/next.png")
nextbtn=Button(control_frm,text="Next",command=next_song,image=next_image)
nextbtn.grid(row=1,column=5)

vol_image=PhotoImage(file = "icon/vol.png")
vol_btn=Button(control_frm,text="Volume",command=mute_fun,image=vol_image)
vol_btn.grid(row=1,column=6)

global volume_bar
volume_bar=ttk.Scale(control_frm,from_=0,to=100,orient=HORIZONTAL,command=set_volume)
volume_bar.set(70)
mixer.music.set_volume(0.7)
volume_bar.grid(row=1,column=7)





















status_lbl=Label(status_frm,textvariable=status)
status_lbl.pack()




root.mainloop()


