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
capture = cv2.VideoCapture('./videos/video.mp4')
# capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# capture.set(cv2.CAP_PROP_SATURATION, 150)

# Ahora clasifico el video
frame = 0

paleta = np.array([[0,0,255],[0,255,0],[255,0,0], [0,0,0]],dtype='uint8')

shrinkFactor = 4
segImg = np.empty((config.imageShape['height']/shrinkFactor, config.imageShape['width']/shrinkFactor, 3), dtype='uint8')

# outIm = cv2.VideoWriter('./videos/demoImagen.mp4', cv2.VideoWriter_fourcc(*'XVID'), 25, (320, 240))
# outSeg = cv2.VideoWriter('./videos/demoSegm.mp4', cv2.VideoWriter_fourcc(*'XVID'), 25, (320/4, 240/4))


times = []
while (capture.isOpened()):
    beg = time.time()
    
    ret, im = capture.read()
    # outIm.write(im)

    cv2.imshow('Real', im)

    # segmentation
    imHSV = im[0::shrinkFactor,0::shrinkFactor,:]
    imHSV = cv2.cvtColor(imHSV, cv2.COLOR_BGR2HSV)
    imHS = imHSV[:,:,(0,1)]
    
    def predictRow(i):
        segImg[i] = paleta[clf.predict(imHS[i])]

    [predictRow(i) for i in range(imHS.shape[0])]


    cv2.imshow("Segmentacion Euclid",cv2.cvtColor(segImg,cv2.COLOR_RGB2BGR))
    
    times.append(time.time() - beg)

    print np.mean(np.array(times))
 
    cv2.waitKey(1)

    # outSeg.write(cv2.cvtColor(segImg,cv2.COLOR_RGB2BGR))