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
#import pyvjoy
teclas = list('p'+'o'+'z'+'9')
global Gravando, j, Fotos, Controle, cont;

# Teste de commit

#----------------------------------------------------------------------

def listen(tecla):
    global Gravando,Fotos, Controle, cont
    while True:
        keyboard.wait(tecla)
        if tecla == 'p' and Gravando:
            Gravando=False
            print("Gravação parada")
            Salvando = Thread(target=Salvar, kwargs={"x":Fotos[0:cont],"y":Controle[0:cont]})
            Salvando.start()
        elif tecla == 'o' and not Gravando:
            print("Começando a gravar")
            Gravando=True
            Camera()
        elif tecla == 'z':
            exit()
        elif tecla == '9':
            print("Excluindo")
            Gravando=False
            
#----------------------------------------------------------------------
            
def Camera():
    global Gravando, j, Fotos, Controle, cont
    print("Iniciando camera")
    ini=time.time();
    n=10000
    L=240
    H=150
    pixels=L*H*3
    Fotos=np.zeros((n,H,L,3),dtype='uint8')
    Controle=np.zeros((n,4))#.astype('float')
    i=0
    tempo=0.1
    #sound = pygame.mixer.Sound("Samples/drum_tom_mid_hard.wav")
    #sound.play()
    for i in list(range(4))[::-1]:
        print(i+1)
        if not Gravando:
            return
        time.sleep(1)
    print("GOOOO")
    while Gravando:
        last_time = time.time()
        if Gravando:
            screen =  np.array(ImageGrab.grab(bbox=None))
            imagem = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
            #TXT
            Go=False
            while not Go:
                try:
                    shutil.copyfile('D://Velocidade.txt ', 'temp.txt')
                    file = open ( 'temp.txt ', "r" )
                    file_lines = file.readlines()
                    file.close()
                    velocidade = float(file_lines[len(file_lines)-1])
                    Go = True
                except Exception:
                    Go = False
            #TXT
            events = pygame.event.get()
            saida=[(j.get_axis(4)+1)/2,(j.get_axis(5)+1)/2,(j.get_axis(0)+1)/2, velocidade]
            Fotos[i]=imagem#Xvetor.reshape((1,pixels))#np.array(imagem)#
            Controle[i,:]=saida
            if i%50==0:
                print(i, " Fotos")
                #print("Salvamento parcial:  ",i," Fotos")
                #Salvando = Thread(target=Salvar, kwargs={"x":Fotos,"y":Controle})
                #Salvando.start()
            #Tela(imagem)
        cont=i
        i=i+1
        if i==n:
            print("Limite alcançado...")
            Gravando=False
            Salvando = Thread(target=Salvar, kwargs={"x":Fotos,"y":Controle})
            Salvando.start()
            return
        if (time.time()-last_time) <tempo:
            time.sleep(tempo-(time.time()-last_time))
        else:
            print("Demorou",tempo-(time.time()-last_time))
    
            
#----------------------------------------------------------------------

def Salvar(x,y):
    ArquivoX="Dados/XTreino.npy"
    ArquivoY="Dados/YTreino.npy"
    flag=True
    i=0
    while flag:
        ArquivoX="Dados/XTreino"+str(i)+".npy"
        ArquivoY="Dados/YTreino"+str(i)+".npy"
        if not os.path.isfile(ArquivoX) and not os.path.isfile(ArquivoY):
            print("Salvando Arquivo número: ",i)
            flag=False
        else:
            i=i+1
    np.save(ArquivoX,x)
    np.save(ArquivoY,y)
    print("Arquivo número ",i, " Salvo")
    return

    '''
    try:
        a=np.load("XTreino.npy")
        b=np.load("YTreino.npy")
        np.save("XTreino",np.cozncatenate((a, x), axis=0))
        np.save("YTreino",np.concatenate((b, y), axis=0))
    except:
        print("eee")
        print(e)
        print("Criando arquivo")
        np.save("XTreino",x)
        np.save("YTreino",y)

            with open('Dados/XTreino.csv', 'a', newline='') as Xtreino:
        escrever = csv.writer(Xtreino)
        escrever.writerows(x)
    with open('Dados/YTreino.csv', 'a', newline='') as Ytreino:
        escrever = csv.writer(Ytreino)
        escrever.writerows(y)        

        
    if os.path.isfile(Arquivo):
        print('Carregando dados')
        Treino = list(np.load(Arquivo))
    else:
        print('Novo arquivo')

        print("Salvamento Parcial")
    Xtreino = open('Dados/XTreino.csv', 'w', newline='')
    Ytreino = open('Dados/YTreino.csv', 'w', newline='')
    Xescrever = csv.writer(Xtreino)
    Yescrever = csv.writer(Ytreino)
    Xescrever.writerows(x)
    Yescrever.writerows(y)
    
    '''
    
#----------------------------------------------------------------------

def Tela(img):
    cv2.imshow('window',cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

#----------------------------------------------------------------------
Fotos=[]
Controle=[]
Gravando=False;
cont=0
pygame.init()
j = pygame.joystick.Joystick(1)
j.init()
teclado = [Thread(target=listen, kwargs={"tecla":tecla}) for tecla in teclas]
for thread in teclado:
    thread.start()
#----------------------------------------
#Volante=16384
#tecla https://pt.stackoverflow.com/questions/327492/
#como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python
