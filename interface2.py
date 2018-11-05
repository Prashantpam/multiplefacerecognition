import tkinter as tk
from tkinter import filedialog
from tkinter import *
import playVideo
import pkscanner
import takephoto
import pkimage


def quit(self):
    self.root.destroy()
    
def pic():
    file_path = filedialog.askopenfilename()
    #print(file_path)
    temp=list(map(str,file_path.strip().split('.')))
    if temp[-1]=="png" or temp[-1]=="jpeg" or temp[-1]=="jpg":
        pkimage.image(file_path)
        label  = Label(root, text= "thanks for providing pic, we're processing your pic and soon will show up the result")
    else:
        label  = Label(root, text= "Please, provide valid file !")
    label.pack()

def video():
    file_path = filedialog.askopenfilename()
    #print(file_path)
    temp=list(map(str,file_path.strip().split('.')))
    if temp[-1]=="mp4" or temp[-1]=="avi":
        playVideo.play(file_path)
        label  = Label(root, text= "thanks for providing videp, we're processing your request and soon will show up the result")
    else:
        label  = Label(root, text= "Please, provide valid file !")
    label.pack()
    label.pack()

def live():
    pkscanner.scanner()
    
def photo():
    takephoto.click()

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

slogan = tk.Button(frame,text="select video",command=video)
slogan.pack(side=tk.LEFT)

slogan = tk.Button(frame,text="live",command=live)
slogan.pack(side=tk.LEFT)

slogan = tk.Button(frame,text="select picture",command=pic)
slogan.pack(side=tk.LEFT)

slogan = tk.Button(frame,text="save photo",command=photo)
slogan.pack(side=tk.LEFT)



root.mainloop()



