# An end-to-end approach to autonomous vehicle control using deep learning

This repository contains the code developed in the undergraduate thesis written by Gustavo Antonio Magera Novello and Henrique Yda Yamamoto with the supervision of Prof. Eduardo Lobo Lustosa Cabral in Mechatronics Engineering Department of Polytechnic School of the University of São Paulo. 

We developed an autonomous vehicle controller inside a simulation enviroment (Grand Theft Auto V game) in an end-to-end approach. The model is composed of convolutional neural networks to process images from a front camera and a recurrent neural networks to process sequential speed data. After training with the data described in https://github.com/elcabral/Autonomous-vehicle-dataset the model outputs driving commands to control the car inside game. Tests with trained model made within the chosen circuit can be found in this youtube playlist https://youtu.be/8m_QSb9NPIM. The results show that the model after training is capable of obtaining a good driving performance even using only images and speed as input data.

The developed interfaces, to collect data and to control the vehicle are described in this repository in "Control Interface" and "Data Acquisition Interface" folders with source code. The Jupyter Notebook used to train the model is also available in "Model" folder.
