'''
Autonomous-Vehicle-GTA-V
Gustavo and Henrique
'''
#Bibliotecas utilizadas
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

teclas = list('p'+'o'+'z'+'9')
global Gravando, j, Fotos, Controle, cont;

#----------------------------------------------------------------------

def listen(tecla):
    '''
    Após pressionar umas das teclas de controle, executa a função correspondente.
    Teclas:
        o: Inicia a gravação
        p: Para a gravação atual e salva os dados
        z: Encerra a execução do programa de aquisição
        9: Para a gravação sem salvar os dados
    '''

    global Gravando,Fotos, Controle, cont
    while True:
        keyboard.wait(tecla)
        #Para a gravação atual e salva os dados
        if tecla == 'p' and Gravando:
            Gravando=False
            print("Gravação parada")
            Salvando = Thread(target=Salvar, kwargs={"x":Fotos[0:cont],"y":Controle[0:cont]})
            Salvando.start()
        #Inicia a gravação
        elif tecla == 'o' and not Gravando:
            print("Começando a gravar")
            Gravando=True
            Camera()
        #Encerra a execução do programa de aquisição
        elif tecla == 'z':
            exit()
        #Para a gravação sem salvar os dados
        elif tecla == '9':
            print("Excluindo")
            Gravando=False
            
#----------------------------------------------------------------------
            
def Camera():
    '''
    Função responsável por aquisitar e organizar os dados coletados.
    '''
    global Gravando, j, Fotos, Controle, cont
    print("Iniciando camera")

    #Inicia variaveis
    n=10000 #Numero maximo que é reservado para salvamento dos exemplos coletados
    L=240 #Largura da foto
    H=150 #Altura da foto
    Fotos=np.zeros((n,H,L,3),dtype='uint8') #Vetor de fotos
    Controle=np.zeros((n,4)) #Vetor com os dados de direção e velocidades
    i=0 #Contador
    tempo=0.1 #Tempo entre coleta de dados

    #Espera alguns segundos antes de iniciar
    for i in list(range(4))[::-1]:
        print(i+1)
        #Verifica se a coleta nao foi interropida durante a espera
        if not Gravando:
            return
        time.sleep(1)
    print("GOOOO")

    #Loop para coleta dos dados
    while Gravando:
        last_time = time.time()
        if Gravando:
            #Captura da teka
            screen =  np.array(ImageGrab.grab(bbox=None))
            imagem = cv2.resize(screen,(L,H),interpolation=cv2.INTER_CUBIC)
            #Leitura do arquivo txt com o valor da velocidade
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
            #Leitura do controle
            events = pygame.event.get()
            saida=[(j.get_axis(4)+1)/2,(j.get_axis(5)+1)/2,(j.get_axis(0)+1)/2, velocidade]
            #Organiza os dados no vetor numpy
            Fotos[i]=imagem
            Controle[i,:]=saida
            #Aviso a cada 50 amostras
            if i%50==0:
                print(i, " Fotos")
        cont=i
        i=i+1

        #Verifica se o limite defino foi alcançado
        if i==n:
            print("Limite alcançado...")
            Gravando=False
            Salvando = Thread(target=Salvar, kwargs={"x":Fotos,"y":Controle})
            Salvando.start()
            return

        #Verifica o tempo entre a ultima amostra coletada
        if (time.time()-last_time) <tempo:
            time.sleep(tempo-(time.time()-last_time))
        else:
            print("Demorou",tempo-(time.time()-last_time))
    
            
#----------------------------------------------------------------------

def Salvar(x,y):
    '''
    Salva os dados obtidos em vetores numpy no diretório Dados.
    As fotos são salvas com o nome Xtreino enquanto os dados do controle
    e velocidade são salvos com o nome Ytreino
    '''

    #Nomes dos locais de salvamento
    ArquivoX="Dados/XTreino.npy"
    ArquivoY="Dados/YTreino.npy"

    #Verifica o número do ultimo arquivo gravado
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

    #Salva os arquivos numpys
    np.save(ArquivoX,x)
    np.save(ArquivoY,y)
    print("Arquivo número ",i, " Salvo")
    return

#----------------------------------------------------------------------

#Iniciando variaveis
Fotos=[]
Controle=[]
Gravando=False;
cont=0
pygame.init()
j = pygame.joystick.Joystick(1)
j.init()

#Inicia as threads para leitura das teclas [1]
teclado = [Thread(target=listen, kwargs={"tecla":tecla}) for tecla in teclas]
for thread in teclado:
    thread.start()

#----------------------------------------
#[1] https://pt.stackoverflow.com/questions/327492/como-fa%C3%A7o-para-capturar-cada-tecla-digitada-em-python