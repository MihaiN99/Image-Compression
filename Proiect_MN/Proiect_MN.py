#Realized by Alexandru-Andrei Carmici and Mihai Necula

#PySimpleGUI a fost importata pentru interfata grafica
#numpy a fost importata pentru utilizarea a unor comenzi precum: np.dot, np.diag
#matplotlib a fost importanta pentru afisarea imaginilor
#din numpy.linalg am importat functia svd
#PIL pentru prelucrare de imagini
#os folosim pentru path/calea fisierului 
#random folosim pentru a genera o valoarea aleatoare intre 0 si 20 pentru sigma
#time folosim pentru timpul de executie

import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image
import os
from os import path
import random
import time

def show_images(img_name):
    plt.title("Original Image")
    plt.imshow(images[img_name])
    plt.show()

def compress_image(img_name, k):
    #parcurgem fiecare vector
    print("Processing...")
    start_time=time.time()

    global compressed_image #imaginea rezultata
    img = images[img_name] #imaginea bruta

    #parametrii care definesc culoarea pixelului, format PNG cu 3 parametrii(RGB), nu cu 4 parametrii (RGBA)

    rosu = img[:,:,0]
    verde = img[:,:,1]
    blue = img[:,:,2]

    #print(r)
    #print(g)
    #print(b)
    print("Compressing...")
    #Se aplica svd pentru fiecare format de culoare

    matr_u_red,sigma_red,matr_v_red = svd(rosu) 
    matr_u_green,sigma_green,matr_v_green = svd(verde)
    matr_u_blue,sigma_blue,matr_v_blue = svd(blue)

    #Inmultirea matricelor - utilizata pentru compresie

    red_image = np.dot(matr_u_red[:,:k],np.dot(np.diag(sigma_red[:k]), matr_v_red[:k,:]))
    green_image = np.dot(matr_u_green[:,:k],np.dot(np.diag(sigma_green[:k]), matr_v_green[:k,:]))
    blue_image = np.dot(matr_u_blue[:,:k],np.dot(np.diag(sigma_blue[:k]), matr_v_blue[:k,:]))

    print("Arranging...")
    #Face imaginea initial nula/goala
     #Atribuim matricele obtinute mai sus in variabila imaginea

    imaginea = np.zeros(img.shape)

    imaginea[:,:,0] = red_image
    imaginea[:,:,1] = green_image
    imaginea[:,:,2] = blue_image

    #compressed_image[compressed_image < 0]=0
    #compressed_image[compressed_image >255]=255

    for ind1, row in enumerate(rimg): #parcurge fiecare pixel
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value) #daca valoarea este negativa, se aplica modulul
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255 # se pune 255 pentru a evita eventualele greseli in imagine

    compressed_image = rimg.astype(np.uint8) # aproximam la un intreg fiecare culoare al pixelului
    
    plt.title("Compressed Image\nElapsed time for compression: "+str(int(time.time()-start_time))+"s")
    plt.imshow(compressed_image)
    plt.show()
    compressed_image = Image.fromarray(compressed_image)

layout=[[sg.Text("Write the image's name with its extension: ")], [sg.Input(key="input")], [sg.Button("SELECT")]]
window=sg.Window("Image Compression", layout)

random.seed(0)

while True:
    event, values = window.read()
    if event == "SELECT":
        name=values["input"]
        sigma=random.randrange(0,20) # sigma ia o valoare intre 0 si 20
        #gradul de estompare

        if name=="":
            exit(1)
        elif path.exists(name)==False:
            continue

        images = {
            "image": np.asarray(Image.open(name))
        }

        show_images('image')
        compressed_image=None
        compress_image("image", sigma)
        compressed_image.save("compressed_image.png")
    elif event == sg.WIN_CLOSED:
        break
        
window.close()
