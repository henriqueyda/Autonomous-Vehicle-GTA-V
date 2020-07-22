'''
Autonomous-Vehicle-GTA-V
Control Interface
Authors: Gustavo A. M. Novello and Henrique Y. Yamamoto
'''
# Importing Libraries
import numpy as np
from PIL import ImageGrab
import cv2
import time
import pygame
import csv
import shutil
import pyautogui
import keyboard
import string
from threading import *
import threading
import os
import pyvjoy
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import tensorflow as tf

keys = list('p'+'o'+'z')
Model="NN/vgg_avg.h5" # Path to save model

# Global Variables
speed = np.zeros((1,1,50))
Photos = []
Control = []
Recording = False
count = 0
Maximum = 32767

#----------------------------------------------------------------------

def listen(key):
    '''
    Press one of the following keys to start each task:
    Keys:
        o: Starts vehicle control
        p: Turns off vehicle control in simulation environment
        z: Stops program execution
    '''
    global Recording, Photos, Control, count, Vjoy
    while True:
        keyboard.wait(key)
        # Turns off vehicle control in simulation environment
        if key == 'p' and Recording:
            Recording=False
            reset(Vjoy)
            print("Control stopped")
        # Starts vehicle control   
        elif key == 'o' and not Recording:
            print("Control starting")
            Recording=True
            Camera()
        # Stops program execution
        elif key == 'z':
            reset(Vjoy)
            exit()
            
#----------------------------------------------------------------------
            
def Camera():
    '''
    Data acquisition and autonomous vehicle control in GTA V simulation environment 

    '''
    global Recording, j, Photos, Control, count, graph, Maximum, Vjoy, speed
    print("Starting camera")
    ini=time.time();
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    n=10000
    L=240
    H=150 #
    i=0
    tim=0.1 # Actuation rate

    # Delay to start control
    for i in list(range(1))[::-1]:
        print(i+1)
        # Checks if control was interrupted
        if not Recording:
            return
        time.sleep(1)

    # Control Loop   
    print("Controlling")
    while Recording:
        last_time = time.time()
        # Image Acquisition
        screen =  np.array(ImageGrab.grab(bbox=None))
        image = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
        image=image.reshape(1,H,L,3)
        # Speed Acquisition
        speed = np.roll(speed, -1)
        Go=False
        while not Go and Recording:
            try:
                shutil.copyfile('D://Speed.txt ', 'temp.txt')
                file = open ( 'temp.txt ', "r" )
                file_lines = file.readlines()
                file.close()
                spd = float(file_lines[len(file_lines)-1])
                spd = (spd-53.5)/28
                speed[0][0][49] = spd
                Go = True
            except Exception:
                Go = False
        # Control commands prediction - Neural Network
        with graph.as_default():
            Output = model.predict([image,speed])
        # Sets driving commands in controller
        if Recording:
            Vjoy.set_axis(pyvjoy.HID_USAGE_RZ,int(Maximum*Output[0][0]))
            Vjoy.set_axis(pyvjoy.HID_USAGE_Z, int(Maximum*Output[0][1]))
            Vjoy.set_axis(pyvjoy.HID_USAGE_X, int(Maximum*Output[0][2]))
        # Checks for control delay 
        if (time.time()-last_time) < tim:
            time.sleep((tim-(time.time()-last_time)))
        else:
            print("Delayed ",tim-(time.time()-last_time))
            
#----------------------------------------------------------------------
           
def reset(j):
    '''
    Resets virtual joystick and sets steering wheel and pedals to neutral position
    
    '''
    print("Resetting...")
    j.reset()
    j.reset_buttons()
    j.reset_povs()
    j.update()
    j.set_axis(pyvjoy.HID_USAGE_X, 16384)
    j.set_axis(pyvjoy.HID_USAGE_Y, 16384)
    j.set_axis(pyvjoy.HID_USAGE_RX, 16384)
    j.set_axis(pyvjoy.HID_USAGE_RY, 16384)
    j.set_axis(pyvjoy.HID_USAGE_Z, 1)
    j.set_axis(pyvjoy.HID_USAGE_RZ, 1)

#----------------------------------------------------------------------

pygame.init()
Vjoy = pyvjoy.VJoyDevice(1)
reset(Vjoy)
model = keras.models.load_model(Model)
model.summary()
print("\nNeural Network: ", Model)
model._make_predict_function()
graph = tf.get_default_graph()
j = pygame.joystick.Joystick(0)
j.init()

#Starts threads to read keys [1]
keybd = [Thread(target=listen, kwargs={"key":key}) for key in keys]
for thread in keybd:
    thread.start()
#----------------------------------------
#[1] https://pt.stackoverflow.com/questions/327492/como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python
