from tkinter.ttk import *
from tkinter import *
import threading as t
from PIL import ImageTk, Image
import cv2
import pyautogui
import numpy as np
import time 
from datetime import datetime
from tkinter import filedialog

root=Tk()
root.title("Screen Recorder Python")

#Vars 
action=StringVar()  #Deals with storing name of icon to display (record/pause)
actionID=IntVar()    #States kind of action   (1 for record, 2 for stop)
action.set("Click to record Video")


#Select folder to store video
def folder_select():
    folder_dir=filedialog.askdirectory()
    return folder_dir

#Recorder part
def recorder():
    #Screen resolution
    screen_size=(1920,1080)

    #Opencv object 
    fourcc=cv2.VideoWriter_fourcc(*"XVID")

    #FPS parameters
    FPS=120

    #Path from dialog
    path=folder_select()

    #Video Frame params
    prev=0
    #CV object
    out=cv2.VideoWriter(path+"\output.avi",fourcc,20.0,(screen_size))
    while actionID.get()==1:
        #capture frame
        time_elapsed=time.time()-prev

        #Capture screenshot
        img=pyautogui.screenshot()

        #time management
        if time_elapsed> (1/FPS):
            prev=time.time()
            frame=np.array(img)
            #Convert BGR frame to RGB
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #Export frame to file 
            out.write(frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Release resources
    cv2.destroyAllWindows()
    out.release()



#Images
img1 = ImageTk.PhotoImage(Image.open("banner.png"))
img2 = ImageTk.PhotoImage(Image.open("record.jpg"))

#Deal with record video
def record_pause():
    #if actionId is 0 (i.e. default) or 2 (i.e. idle mode) set it to record mode (1)
    if (actionID.get()==0 or actionID.get()==2):
        actionID.set(1)
        action.set("Click to Stop")
        #Threads
        thread=t.Thread(target=recorder)
        thread.start()
    else:
        actionID.set(2)  #if active in recording then put to hold (i.e. 2)
        action.set("Click to record Video")

#Display banner image
Label(root, image = img1).grid(row=1)

#Label about inst
Label(root, textvariable=action).grid(row=3,columnspan=5,pady=10,padx=3)

#Display button
Button(root, image=img2, command=record_pause).grid(row=5)

root.mainloop()