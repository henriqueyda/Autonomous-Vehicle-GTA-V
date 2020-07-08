'''
Autonomous-Vehicle-GTA-V
Gustavo and Henrique
'''
#Bibliotecas utilizadas
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

teclas = list('p'+'o'+'z')
global Gravando, j, Fotos, Controle, cont, graph, Maximo, Vjoy, ativo, velocidade;
Rede="Redes/vgg_avg.h5" #Local de armazenamento da rede neural

#----------------------------------------------------------------------

def listen(tecla):
    '''
    Após pressionar umas das teclas de controle, executa a função correspondente.
    Teclas:
        o: Inicia o controle do veiculo
        p: Desliga a atuação do controle no ambiente de simulação
        z: Encerra a execução do programa de controle
    '''
    global Gravando,Fotos, Controle, cont, Vjoy
    while True:
        keyboard.wait(tecla)
        #Desliga a atuação do controle no ambiente de simulação
        if tecla == 'p' and Gravando:
            Gravando=False
            reseta(Vjoy)
            print("Controle parado")
        #Inicia o controle do veiculo   
        elif tecla == 'o' and not Gravando:
            print("Começando a controlar")
            Gravando=True
            Camera()
        #Encerra a execução do programa de controle
        elif tecla == 'z':
            reseta(Vjoy)
            exit()
            
#----------------------------------------------------------------------
            
def Camera():
    '''
    Aquisição de dados e atuação do controle do veiculo autonomo no ambiente
    de simulação GTA V
    '''
    global Gravando, j, Fotos, Controle, cont, graph, Maximo, Vjoy, velocidade
    print("Iniciando camera")
    ini=time.time();
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    n=10000
    L=240
    H=150 #
    i=0
    tempo=0.1 #Determina frequencia de atuação

    #Espera para iniciar o controle
    for i in list(range(1))[::-1]:
        print(i+1)
        #Verifica se o controle foi interropido
        if not Gravando:
            return
        time.sleep(1)

    #Loop de controle    
    print("Controlando")
    while Gravando:
        last_time = time.time()
        if Gravando:
            #Aquisição da imagem
            screen =  np.array(ImageGrab.grab(bbox=None))
            imagem = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
            imagem=imagem.reshape(1,H,L,3)
            #Aquisição da velocidade
            velocidade = np.roll(velocidade, -1)
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
            #Calculo da ação de controle - Rede neural
            with graph.as_default():
                Saida = model.predict([imagem,velocidade])
            #Atualiza a posição dos pedais e volante
            if Gravando:
                Vjoy.set_axis(pyvjoy.HID_USAGE_RZ,int(Maximo*Saida[0][0]))
                Vjoy.set_axis(pyvjoy.HID_USAGE_Z, int(Maximo*Saida[0][1]))
                Vjoy.set_axis(pyvjoy.HID_USAGE_X, int(Maximo*Saida[0][2]))
        #Verifica se teve atraso na atuação do controle
        if (time.time()-last_time) <tempo:
            time.sleep((tempo-(time.time()-last_time)))
        else:
            print("Demorou",tempo-(time.time()-last_time))
            
#----------------------------------------------------------------------
           
def reseta(j):
    '''
    Reseta o joystick virtual e coloca o volante e pedais na posição neutra
    '''
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

#Inicia variaveis
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

#Inicia as threads para leitura das teclas [1]
teclado = [Thread(target=listen, kwargs={"tecla":tecla}) for tecla in teclas]
for thread in teclado:
    thread.start()
#----------------------------------------
#[1] https://pt.stackoverflow.com/questions/327492/como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python
