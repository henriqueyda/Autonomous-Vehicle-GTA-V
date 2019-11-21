
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
teclas = list('p'+'o'+'z'+'9')
global Gravando, j, Fotos, Controle, cont, graph, Maximo, Vjoy, ativo, velocidade;
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import tensorflow as tf
Rede="Redes/vgg_avg.h5"

#----------------------------------------------------------------------

def listen(tecla):
    global Gravando,Fotos, Controle, cont, Vjoy
    while True:
        keyboard.wait(tecla)
        if tecla == 'p' and Gravando:
            Gravando=False
            reseta(Vjoy)
            print("Controle parado")
        elif tecla == 'o' and not Gravando:
            print("Começando a controlar")
            Gravando=True
            Camera()
        elif tecla == 'z':
            reseta(Vjoy)
            exit()
            
#----------------------------------------------------------------------
            
def Camera():
    global Gravando, j, Fotos, Controle, cont, graph, Maximo, Vjoy, velocidade
    print("Iniciando camera")
    ini=time.time();
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    n=10000
    L=240
    H=150
    pixels=L*H*3
    i=0
    tempo=0.1
    for i in list(range(1))[::-1]:
        print(i+1)
        if not Gravando:
            return
        time.sleep(1)
    print("Controlando")
    while Gravando:
        last_time = time.time()
        if Gravando:
            screen =  np.array(ImageGrab.grab(bbox=None))
            imagem = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
            imagem=imagem.reshape(1,H,L,3)#float/255
            velocidade = np.roll(velocidade, -1)
            #TXT
            Go=False
            while not Go and Gravando:
                try:
                    shutil.copyfile('D://Velocidade.txt ', 'temp.txt')
                    file = open ( 'temp.txt ', "r" )
                    file_lines = file.readlines()
                    file.close()
                    vel = float(file_lines[len(file_lines)-1])
                    vel = (vel-53.5)/28
                    velocidade[0][0][49] = vel
                    Go = True
                except Exception:
                    Go = False
            #TXT    
            with graph.as_default():
                Saida = model.predict([imagem,velocidade])
            if Gravando:
                Vjoy.set_axis(pyvjoy.HID_USAGE_RZ,int(Maximo*Saida[0][0]))
                Vjoy.set_axis(pyvjoy.HID_USAGE_Z, int(Maximo*Saida[0][1]))
                Vjoy.set_axis(pyvjoy.HID_USAGE_X, int(Maximo*Saida[0][2]))
        if (time.time()-last_time) <tempo:
            time.sleep((tempo-(time.time()-last_time)))
        else:
            print("Demorou",tempo-(time.time()-last_time))
            
#----------------------------------------------------------------------
           
def reseta(j):
    print("Resetando...")
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

velocidade=np.zeros((1,1,50))
Fotos=[]
Controle=[]
Gravando=False
ativo=False
cont=0
pygame.init()
Maximo=32767
Vjoy = pyvjoy.VJoyDevice(1)
reseta(Vjoy)
model = keras.models.load_model(Rede)
model.summary()
print("\nRede: ",Rede)
model._make_predict_function()
graph = tf.get_default_graph()
j = pygame.joystick.Joystick(0)
j.init()
teclado = [Thread(target=listen, kwargs={"tecla":tecla}) for tecla in teclas]
for thread in teclado:
    thread.start()
#----------------------------------------
#Volante=16384
#tecla https://pt.stackoverflow.com/questions/327492/
#como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python
