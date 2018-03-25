# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:02:08 2018

@author: ghaza
"""

""" SAMPLE RECORDER for SCYLLA
code to record sample staged videos 

The recording starts if movement is detected in camera view area. 
The recording stops when 'idletime' seconds no changes are detected or 'q' is pressed
The recording resumes in cycle 

Created on Mar 24 00:15:35 2018
@author: Ara Ghazaryan
"""
import re
import datetime
import os
import time
from PIL import Image, ImageTk
from tkinter import Tk, BOTH
from tkinter.ttk import Frame, Label, Button, Style

camip  = '192.168.178.87'
camip  = '192.168.0.26'
qualityflag = 0 # 0  640x 352  capture resolution 
                # 1 1280 x 720
idletime = 7 # idle time threshold
maxduration = 300
idlethreshold = 50
fontsize = 0.75 + 0.75 *qualityflag

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)
# find the maximum of the filename number
def lastfilenumber (path, mode): 
    filenum = 1
    for root, dirs, files in os.walk(path):
        for file in files:
            numgroup=''
            if file.endswith(".mp4"):
                 if mode in file:
                     numgroup= re.search(r'\d+', file)
                     if numgroup:
                         i=numgroup.group(0)
                         if i.isdigit(): 
                             i = int(i)
                             if filenum < i:
                                 filenum = i                                              
    return filenum

class MakeAChoice(Frame):
    def __init__(self):
        super().__init__()   
        self.initUI()
    def initUI(self):
        self.master.title("Choisce of Mode") #Title
        self.pack(fill=BOTH, expand=1)
        
        Style().configure("TFrame", background="#CCC")
        
        # list of texts for labels above the dual choice question box
        textbase = ["Choose the Scene Mode",  
                    "Are you ready to rec?",
                    "Do you need a preview?"]
        # list of texts on left and right button, respectively 
        buttonbase = ['General','Violence',
                      'Cancel','Record',
                      'Preview', 'Record']
        # files of images should be 80x80 named qNl.png and qNr.png 
        # for left and right Nth question, respectively
        imLeft = ImageTk.PhotoImage(Image.open('q' +str(QFlag)+'l.png'))
        imRight = ImageTk.PhotoImage(Image.open('q' +str(QFlag)+'r.png'))
        lbl2 = Label(text=textbase[QFlag-1], width=100, background="#CCC", foreground="black", font=("Courier", 12))    
        Button1 = Button(self, text=buttonbase[QFlag*2-2], command= self.leftbut)
        Button2 = Button(self,  text=buttonbase[QFlag*2-1], command= self.rightbut)
                # positionning of components 
        label1 = Label(self, image=imLeft)
        label1.image = imLeft
        label1.place(x=21, y=27)        
        label2 = Label(self, image=imRight)
        label2.image = imRight
        label2.place(x=147, y=28)        
        Button1.place(x=25, y=117)
        Button2.place(x=151, y=117)
        lbl2.place(x=18, y=3)
    def leftbut(self):
        self.m = 0
        self.master.destroy()
    def rightbut(self):
        self.m = 1
        self.master.destroy()        

def question(QFlag):
    root = Tk()
    root.geometry("250x148+300+300")
    thechoice = MakeAChoice()
    root.mainloop() 
    return thechoice.m 




# *************************    STARTs HERE    *******************************
# Ask for preview
QFlag = 3
previewChoice = question(QFlag) 
if not previewChoice:
    import cv2    
    if qualityflag:
        captstream = cv2.VideoCapture("rtsp://admin:admin@" +camip+"/11") # connect to remote IP cam
    else:
        captstream = cv2.VideoCapture("rtsp://admin:admin@" +camip+"/12") # connect to remote IP cam
    fourcc = cv2.VideoWriter_fourcc(*'MP4V') # fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object
    nochange = 1
    while nochange:
        ret, frame = captstream.read()
        text = "Preview mode. press 'q' when ready"
        cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontsize,(50,180,0))
        cv2.imshow('frame',frame)  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            nochange=0
            break
    captstream.release()
    cv2.destroyAllWindows()
    
# qustion the scene mode
QFlag = 1
scenechoice = question(QFlag) 
# request confirmation to start recording
QFlag = 2
rec =  question(QFlag)
recflag = 0

if rec:
    if scenechoice: 
        mode="violent"
    else:
        mode="general"
    import cv2
    import numpy as np
    if qualityflag:
        captstream = cv2.VideoCapture("rtsp://admin:admin@" +camip+"/11") # connect to remote IP cam
    else:
        captstream = cv2.VideoCapture("rtsp://admin:admin@" +camip+"/12") # connect to remote IP cam
    fourcc = cv2.VideoWriter_fourcc(*'MP4V') # fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object
    ret, frame = captstream.read()
    if ret==True:
        recflag = 1 
        currentpath = os.getcwd()
        videopath  = os.getcwd() + '\\' + datetime.datetime.now().strftime("%Y%m%d") # make the folder from date
        print ('Recording ' + mode + ' video')    
    else:
        quit()
            
    tic = time.time()
    text = 'IDLE state. Will start recording, once change is detected'       
    cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontsize,(180,50,0))
    
    while recflag:
        #errarr = []
        nochange = 1
        ret, frame = captstream.read()
        text = 'IDLE state. Will start recording, once change is detected'       
        cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontsize,(180,50,0))
        cv2.imshow('frame',frame)  
        minitic = time.time()
        print ('In Idle mode. The recording will start when there are changes in camera viewing area')  
        frameold = frame 
        # ***************************   IDLE mode **********************************
        while nochange:
            ret, frame = captstream.read()
            text = 'IDLE state. Will start recording, once change is detected'       
            cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontsize,(180,50,0))
            cv2.imshow('frame',frame)  
            if time.time()-minitic>0.5:
                err = np.sum((frame.astype("float") - frameold.astype("float")) ** 2)
                err /= float(frame.shape[0] * frameold.shape[1])
                #errarr.append(err)  plt.plot(errarr) plt.show()
                frameold=frame
                if err> idlethreshold:
                    nochange=0
                else:
                    minitic = time.time()
                    frameold= frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                nochange=0
                break
            
        # changes detectd -> prepareing for recording
        if not os.path.exists(videopath): 
            os.makedirs(videopath)
            filenumber = 1
        else:
            filenumber = lastfilenumber (currentpath, mode)+1
        filename =  mode + '_' + str(filenumber) + '.mp4'
        if qualityflag:  # chose the stream (quality)
            out = cv2.VideoWriter(videopath + '\\' + filename,fourcc, 30.0, (1280,720)) # connect to remote IP cam
        else:
            out = cv2.VideoWriter(videopath + '\\' + filename,fourcc, 30.0, (640,352))
        print ('File name: ' + filename)    
    
        # ****************************** RECORDING ****************************
        tic = time.time()
        tocfornochange = time.time()
        while not nochange:
            toc = time.time()        
            ret, frame = captstream.read()
            if ret:
                out.write(frame)
                text = 'Recording ' + filename
                cv2.putText(frame, text,(20, 40),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontsize,(0,0,255))
                cv2.imshow('frame',frame)
                if toc -minitic> 0.5:
                    err = np.sum((frame.astype("float") - frameold.astype("float")) ** 2)
                    err /= float(frame.shape[0] * frameold.shape[1])
                    #errarr.append(err) plt.plot(errarr) plt.show()
                    minitic = time.time()
                    frameold=frame
                    if err<idlethreshold:
                        if time.time()-tocfornochange >idletime:
                            nochange =1
                            print ('Stopped recording - idle for too long')
                    else:
                        tocfornochange = time.time()            
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    recflag=0
                    break
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    nochange=1
                    break
            if not captstream.isOpened() or (time.time()-tic)>maxduration:
                recflag = 0
               
    # Release everything when job is finished
    captstream.release()
    out.release()
    cv2.destroyAllWindows()
