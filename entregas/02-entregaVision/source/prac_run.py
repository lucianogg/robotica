# Autores:
# Luciano Garcia Giordano - 150245
# Gonzalo Florez Arias - 150048
# Salvador Gonzalez Gerpe - 150044

import cv2
from matplotlib import pyplot as plt
import numpy as np
import config
import datasetGenerator
import clasificador

import time



clf = clasificador.Clasificador(datasetGenerator.shapeD)
clf.train()

# Inicio la captura de imagenes
capture = cv2.VideoCapture('./video.mp4')

# Ahora clasifico el video
frame = 0
while (True):
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame)
    frame += 2
    ret, im = capture.read()

    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    cv2.imshow('Real', im)

    # segmentation
    imHSV = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    imHS = imHSV[:,:,(0,1)]

    paleta = np.array([[0,0,0],[0,0,255],[0,255,0],[255,0,0]],dtype='uint8')  

    # print(imHS[1,2])

    # segImg = np.array([[paleta[clf.predict(imHS[i,j])] for j in range(imHS.shape[1])] for i in range(imHS.shape[0])], dtype='uint8')
    segImg = np.array([paleta[clf.predict(imHS[i])] for i in range(imHS.shape[0])], dtype='uint8')
 
    cv2.imshow("Segmentacion Euclid",cv2.cvtColor(segImg,cv2.COLOR_RGB2BGR))
 
    cv2.waitKey(1)
