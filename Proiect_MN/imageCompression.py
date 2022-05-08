#Realized by Alexandru-Andrei Carmici and Mihai Necula

import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image
from ipywidgets import interact, interactive, interact_manual
import ipywidgets as widgets
from IPython.display import display
import os
from os import path
import random
import time

def show_images(img_name):
    print("Loading...")
    plt.title("Original Image")
    plt.imshow(images[img_name])
    plt.show()

def compress_image(img_name, k):
    print("Processing...")
    start_time=time.time()

    global compressed_image
    img = images[img_name]

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    print("Compressing...")
    ur,sr,vr = svd(r)
    ug,sg,vg = svd(g)
    ub,sb,vb = svd(b)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sb[:k]), vb[:k,:]))

    print("Arranging...")
    rimg = np.zeros(img.shape)
    rimg[:,:,0] = rr
    rimg[:,:,1] = rg
    rimg[:,:,2] = rb

    for ind1, row in enumerate(rimg):
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value)
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255

    compressed_image = rimg.astype(np.uint8)
    
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
        sigma=random.randrange(0,20)

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