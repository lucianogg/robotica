# Autores:
# Luciano Garcia Giordano - 150245
# Gonzalo Florez Arias - 150048
# Salvador Gonzalez Gerpe - 150044
 
import numpy as np
import cv2
from matplotlib import pyplot as plt
import config
import datasetGenerator
import clasificador
import math
import os
import time

'''
def predictRow(i):
      	# print segImg
        segImg[i] = clf.predict(imHS[i])


def segmentar(im):

	

	paleta = np.array([[0, 0, 255], [0, 255, 0], [255, 0, 0], [0, 0, 0]],
                  dtype='uint8')

	shrinkFactor = 4
	originalImageHeight = (config.imageShape['height'] / shrinkFactor)
	imageHeight = int(originalImageHeight*0.5)
	imageWidth = int(config.imageShape['width'] / shrinkFactor)

	segImg = np.empty((imageHeight,imageWidth),dtype='uint8')


	imHSV = im[((originalImageHeight - imageHeight)*shrinkFactor)::shrinkFactor, 0::shrinkFactor, :]
    	imHSV = cv2.cvtColor(imHSV, cv2.COLOR_BGR2HSV)
    	imHS = imHSV[:, :, (0, 1)]

	

    	[predictRow(i) for i in range(imHS.shape[0])]

    	imageOnPaleta = paleta[segImg]

    	arrow = np.zeros(segImg.shape, dtype='uint8')
    	line = np.zeros(segImg.shape, dtype='uint8')
    	# 0 - line
    	# 1 - floor
    	# 2 - symbols
    	# 3 - nothing - not used
    	line[segImg == 0] = 1
    	arrow[segImg == 2] = 1

	return arrow
'''

clf = clasificador.Clasificador(datasetGenerator.shapeD)
clf.train()

for cl in ['escalera', 'caballero', 'cabina', 'cruz', 'flecha']:
	skip_pixels_at_top = 0
	all_moments = []
	directory = "images/" + cl

	
	# Itero para todas las 100 imagenes
	for filename in os.listdir(directory):
		fullname = os.path.join(directory, filename)
		# Leo imagen
		img = cv2.imread(fullname)
		
		#labels = segmenter.segment(img[skip_pixels_at_top:, :])
		
		paleta = np.array([[0, 0, 255], [0, 255, 0], [255, 0, 0], [0, 0, 0]],
					dtype='uint8')

		shrinkFactor = 1
		originalImageHeight = int(config.imageShape['height'] / shrinkFactor)
		imageHeight = int(originalImageHeight)
		imageWidth = int(config.imageShape['width'] / shrinkFactor)

		segImg = np.empty((imageHeight,imageWidth),dtype='uint8')

		

		imHSV = img[((originalImageHeight - imageHeight)*shrinkFactor)::shrinkFactor, 0::shrinkFactor, :]
		imHSV = cv2.cvtColor(imHSV, cv2.COLOR_BGR2HSV)
		imHS = imHSV[:, :, (0, 1)]

		#cv2.imshow('imHS',imHSV)
		#cv2.waitKey()
		
		def predictRow(i):
			# print segImg
			segImg[i] = clf.predict(imHS[i])
			
		[predictRow(i) for i in range(imHS.shape[0])]


		#cv2.imshow('segIMG',segImg)
		#cv2.waitKey()

		imageOnPaleta = paleta[segImg]

		arrow = np.zeros(segImg.shape, dtype='uint8')
		line = np.zeros(segImg.shape, dtype='uint8')
		# 0 - line
		# 1 - floor
		# 2 - symbols
		# 3 - nothing - not used
		line[segImg == 0] = 1
		arrow[segImg == 2] = 1
		arrow = cv2.erode(arrow, None, dst=arrow, iterations=1)
		# arrow = cv2.dilate(arrow, None, dst=arrow, iterations=1)
		

		#print(len(arrow[arrow==1]))
		#print(len(arrow)*len(arrow[0]))
		#cv2.imshow('arrow',arrow)
		#cv2.waitKey()

		im = arrow
		# cv2.imshow('gilipollas', im)
		# print(im[imageHeight/2][imageWidth/2])
		# print(im)
		# cv2.imshow('gilipollas', im)
		cv2.imwrite('images/segms/' + cl + '_' + filename + '.segmentation.png', im*255)
		print(filename)
		# cv2.waitKey()
		#palette = np.array([[0, 0, 0], [0, 0, 255], [255, 0, 0], [0, 255, 0]], dtype=np.uint8)
	
		# ahora pinto la imagen con las segmentaciones activas
		#scene.segmented_image = cv2.cvtColor(palette[labels], cv2.COLOR_RGB2BGR)

		# paso imagen segmentada a escala de grises
		#grayscale_img = cv2.cvtColor(scene.segmented_image,cv2.COLOR_BGR2GRAY)
		# Binarizo imagen en escala de grises
		#_, binary_img = cv2.threshold(grayscale_img, 20, 255, cv2.THRESH_BINARY)

		# calculo los 7 momentos de hu y los incluyo en la lista de momentos de esta clase
		moments = cv2.HuMoments(cv2.moments(im)).flatten()
		all_moments.append(moments)
		# Cuando ha recorrido los 100 ficheros, guardo el dataset de esta clase.
	np.savetxt('data_' + cl + '.txt', all_moments)
	# all_moments = []
	print('terminado ' + cl)




