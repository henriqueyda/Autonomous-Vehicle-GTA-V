'''
Autonomous-Vehicle-GTA-V
Data acquisition Interface
Authors: Gustavo A. M. Novello and Henrique Y. Yamamoto
'''
# Importing Libraries
import numpy as np
from PIL import ImageGrab
import cv2
import time
import shutil
import pygame
import csv
import pyautogui
import keyboard
import string
from threading import *
import threading
import os

keys = list('p'+'o'+'z'+'9')

#Global Variables
Photos=[]
Control=[]
Recording=False;
count=0
pygame.init()
j = pygame.joystick.Joystick(1)
j.init()
#----------------------------------------------------------------------

def listen(key):
    '''
    Press one of the following keys to start each task:
    Keys:
        o: Starts screen recording
        p: Stops current recording and save data
        z: Stops program
        9: Stops recording without saving data
    '''
    global Recording, Photos, Control, count
    while True:
        keyboard.wait(key)
        #Stops current recording and save data
        if key == 'p' and Recording:
            Recording = False
            print("Recording stopped...")
            Saving = Thread(target=Save, kwargs={"x":Photos[0:count],"y":Control[0:count]})
            Saving.start()
        #Starts screen recording
        elif key == 'o' and not Recording:
            print("Recording started...")
            Recording = True
            Camera()
        #Stops program
        elif key == 'z':
            exit()
        #Stops recording without saving data
        elif key == '9':
            print("Deleting...")
            Recording = False
            
#----------------------------------------------------------------------
            
def Camera():
    '''
    Function to acquire and organize data
    
    '''
    global Recording, Photos, Control, count

    print("Starting camera...")

    #Variables assignment
    n=10000 # Maximum number of examples to save
    L=240 #Image width
    H=150 #Image height
    Fotos=np.zeros((n,H,L,3),dtype='uint8') #Image array
    Controle=np.zeros((n,4)) #Driving commands and speed array
    i=0 #Counter
    time_between=0.1 # Time between two consecutive acquisitions

    #Waits a few seconds before start
    for i in list(range(4))[::-1]:
        print(i+1)
        #Checks if acquisition was not interrupted during wait time
        if not Recording:
            return
        time.sleep(1)
    print("GOOOO")

    #Data acquisition loop
    while Recording:
        last_time = time.time()
        #Screen capture
        screen =  np.array(ImageGrab.grab(bbox=None))
        image = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
        #Reads txt file with speed values
        Go=False
        while not Go:
            try:
                shutil.copyfile('D://Speed.txt ', 'temp.txt')
                file = open ( 'temp.txt ', "r" )
                file_lines = file.readlines()
                file.close()
                speed = float(file_lines[len(file_lines)-1])
                Go = True
            except Exception:
                Go = False
        #Reads joystick buttons
        events = pygame.event.get()
        output=[(j.get_axis(4)+1)/2,(j.get_axis(5)+1)/2,(j.get_axis(0)+1)/2, speed]
        #Puts data in numpy array
        Photos[i]=image
        Control[i,:]=output
        #Prints after every 50 samples
        if i%50==0:
            print(i, " Images")
        cont=i
        i=i+1

        #Checks if maximum size was exceeded
        if i==n:
            print("Maximum size exceeded...")
            Recording=False
            Saving = Thread(target=Save, kwargs={"x":Photos,"y":Control})
            Saving.start()
            return

        #Checks time since last acquisition
        if (time.time()-last_time) < time_between:
            time.sleep(time_between-(time.time()-last_time))
        else:
            print("Took",time_between-(time.time()-last_time))
    
            
#----------------------------------------------------------------------

def Save(x,y):
    '''
    Save acquired data in numpy array in "Data" folder.
    Images are saved as Xtrain and driving commands and speed are saved as Ytrain 
    '''

    #Path to save data
    FileX="Data/XTrain.npy"
    FileY="Data/YTrain.npy"

    #Checks last saved file number
    flag=True
    i=0
    while flag:
        FileX="Data/XTrain"+str(i)+".npy"
        FileY="Data/YTrain"+str(i)+".npy"
        if not os.path.isfile(FileX) and not os.path.isfile(FileY):
            print("Save file number: ",i)
            flag=False
        else:
            i=i+1

    #Salva os arquivos numpys
    np.save(FileX,x)
    np.save(FileY,y)
    print("File number ",i, " Saved")
    return

#----------------------------------------------------------------------


#Starts threads to read keys [1]
keybd = [Thread(target=listen, kwargs={"tecla":key}) for key in keys]
for thread in keybd:
    thread.start()

#----------------------------------------
#[1] https://pt.stackoverflow.com/questions/327492/como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python