from tkinter import *
from tkinter import ttk


from pygame import mixer
from tkinter import messagebox as mb
from tkinter import filedialog
import os



playing = False
paused = False
mute = False

songs=[]
file=''

def loadmusic():
    extension=['mp3','wav','mpeg','m4a','wma','ogg']
    global songs
    dir_=filedialog.askdirectory(initialdir='Desktop',title='Select Directory')
    os.chdir(dir_)
    status.set('Playlist Updated')
    dir_files = os.listdir(dir_)
    for file in dir_files:
        for ex in extension:
            if file.split('.')[-1]==ex:
                playlistbox.insert(END,file)
                songs.append(file)






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
    global songs
    global file
    index = songs.index(file)-1
    file=songs[index]
    mixer.music.load(file)
    mixer.music.play()

def next_song():
    global file
    global songs
    index=songs.index(file)+1
    file=songs[index]
    mixer.music.load(file)
    mixer.music.play()





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




def fileselect():
    pass

def about():
    mb.showinfo('Musicolet','It is the basic music player with some advance feature made in Python.😎\nIt is created by Bikram Purkait with ❤.\nIt is completed on 22/02/2021.\nThanks for using the application.👍')

def shortcut_key():
    pass







# Main Gui

mixer.init()
root=Tk()


# Initial Work
root.title("Musicolet")
root.geometry('800x520')
root.resizable(height = False, width = False)
root.iconbitmap("icon/icon.ico")

status = StringVar()
status.set('❤Welcome to you in Musiocolet❤')

# create a menubar
mainmenu=Menu(root,tearoff=0)

openmenu=Menu(mainmenu,tearoff=0)
openmenu.add_command(label='Folder Select',command=loadmusic)
openmenu.add_command(label='File Select',command=fileselect)
openmenu.add_separator()
openmenu.add_command(label='Exit',command=exit)
mainmenu.add_cascade(label='Open',menu=openmenu)
aboutmenu=Menu(mainmenu,tearoff=0)
mainmenu.add_command(label='About',command=about)
mainmenu.add_command(label='Shortcut Key',command=shortcut_key)

root.config(menu=mainmenu)






# Create LabelFrame
songtrack_frm=ttk.LabelFrame(master=root,text="Song Track")
songtrack_frm.place(x=0,y=0,width=350,height=350)



playlist_frm=ttk.LabelFrame(master=root,text="Playlist")
playlist_frm.place(x=350,y=0,width=450,height=350)


control_frm=ttk.LabelFrame(master=root,text="Control Bar")
control_frm.place(x=0,y=350,width=800,height=110)


status_frm=ttk.LabelFrame(master=root,text="Song Status")
status_frm.place(x=0,y=460,width=800,height=40)







# Create PlaylistBox and set vertical scroll and add load button
loadbtn=ttk.Button(playlist_frm,text="Load Music",command=loadmusic)
loadbtn.pack()

y_scroll=ttk.Scrollbar(playlist_frm,orient=VERTICAL)
playlistbox=Listbox(playlist_frm,yscrollcommand=y_scroll.set,height=350)
y_scroll.pack(side=RIGHT,fill=Y)
y_scroll.config(command=playlistbox.yview)
playlistbox.pack(fill=BOTH)





# Creating image for buttons
pause_image=PhotoImage(file = "icon/pause.png")
mute_image=PhotoImage(file = "icon/mute.png")
vol_image=PhotoImage(file = "icon/vol.png")
play_image=PhotoImage(file = "icon/play.png")
prev_image=PhotoImage(file = "icon/prev.png")
next_image=PhotoImage(file = "icon/next.png")
stop_image=PhotoImage(file = "icon/stop.png")
repeat_image=PhotoImage(file="icon/repeat.png")
repeat_one_image=PhotoImage(file="icon/repeat_one.png")
shuffle_image=PhotoImage(file="icon/shuffle.png")



# Creating Button
playbtn=Button(control_frm,command=play,image=play_image,bd=0)
playbtn.place(x=350,y=5)

prevbtn=Button(control_frm,image=prev_image,bd=0,command=prev_song)
prevbtn.place(x=300,y=0)

nextbtn=Button(control_frm,image=next_image,bd=0,command=next_song)
nextbtn.place(x=380,y=0)

stopbtn=Button(control_frm,command=stop,image=stop_image,bd=0)
stopbtn.place(x=425,y=5)

vol_btn=Button(control_frm,command=mute_fun,image=vol_image,bd=0)
vol_btn.place(x=600,y=10)

repeat_btn=Button(control_frm,image=repeat_image,bd=0)
repeat_btn.place(x=265,y=7)

global volume_bar
volume_bar=ttk.Scale(control_frm,from_=0,to=100,orient=HORIZONTAL,command=set_volume)
volume_bar.set(70)
mixer.music.set_volume(0.7)
volume_bar.place(x=630,y=8)


progress_bar=ttk.Progressbar(control_frm,orient=HORIZONTAL,length=500)
progress_bar.place(x=130,y=50)



















status_lbl=Label(status_frm,textvariable=status)
status_lbl.pack()




root.mainloop()















