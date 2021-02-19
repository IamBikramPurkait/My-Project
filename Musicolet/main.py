from tkinter import *
from pygame import mixer


def play():
    mixer.music.play()


mixer.init()
mixer.music.load("sample.mp3")

root=Tk()
root.title("Musicolet")
root.geometry('370x240')

frm1=Frame(master=root)
frm1.grid()
frm2=Frame(master=root)
frm2.grid(row=2)


loadbtn=Button(frm1,text="Load Music")
loadbtn.grid(row=1,column=1)

pausebtn=Button(frm2,text="Pause")
pausebtn.grid(row=1,column=0)
playbtn=Button(frm2,text="Play",command=play)
playbtn.grid(row=1,column=1)
stopbtn=Button(frm2,text="Stop")
stopbtn.grid(row=1,column=2)

root.mainloop()


