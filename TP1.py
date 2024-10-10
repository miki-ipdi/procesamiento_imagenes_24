# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 08:31:34 2024

@author: Micaela
"""
import imageio
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen (ajusta la ruta de la imagen según sea necesario)
img = imageio.imread('image1.png') / 255.0

# Imprimir tamaño y tipo de la imagen
print(img.shape, img.dtype)

# Mostrar la imagen original
plt.figure(0)
plt.imshow(img)
plt.title('Imagen Original')
plt.show()  # Mostrar la imagen y luego continuar con el resto de la ejecución

# Mostrar las imágenes RGB en sus diferentes canales
plt.figure(1)
plt.imshow(img[:,:,0], cmap='Reds')  # Canal R en tonos de rojo
plt.title('Canal R')

plt.figure(2)
plt.imshow(img[:,:,1], cmap='Greens')  # Canal G en tonos de verde
plt.title('Canal G')

plt.figure(3)
plt.imshow(img[:,:,2], cmap='Blues')  # Canal B en tonos de azul
plt.title('Canal B')
plt.show()  # Mostrar los tres canales de color y luego continuar

# Función de transformación de RGB a YIQ
def RGBaYIQ(img):
    yiq = np.zeros(img.shape)
    yiq[:,:,0] = np.clip(0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2], 0, 1)  # Y
    yiq[:,:,1] = np.clip(0.595*img[:,:,0] - 0.274*img[:,:,1] - 0.321*img[:,:,2], -0.5957, 0.5957)  # I
    yiq[:,:,2] = np.clip(0.211*img[:,:,0] - 0.523*img[:,:,1] + 0.312*img[:,:,2], -0.5226, 0.5226)  # Q
    return yiq

yiq = RGBaYIQ(img)

# Mostrar las imágenes en YIQ en sus diferentes canales
plt.figure(4)
plt.imshow(yiq)
plt.title('Imagen en YIQ')

plt.figure(5)
plt.imshow(yiq[:,:,0], cmap='gray')  # Canal Y
plt.title('Canal Y')

plt.figure(6)
plt.imshow(yiq[:,:,1], cmap='gray')  # Canal I
plt.title('Canal I')

plt.figure(7)
plt.imshow(yiq[:,:,2], cmap='gray')  # Canal Q
plt.title('Canal Q')
plt.show()  # Mostrar las imágenes en YIQ

# Función para modificar la luminancia y saturación
def modificarYIQ(yiq, a, b):
    yiq_mod = yiq.copy()
    yiq_mod[:,:,0] = np.clip(yiq_mod[:,:,0] * a, 0, 1)  # Modificar luminancia (Y)
    yiq_mod[:,:,1] = np.clip(yiq_mod[:,:,1] * b, -0.5957, 0.5957)  # Modificar saturación (I)
    yiq_mod[:,:,2] = np.clip(yiq_mod[:,:,2] * b, -0.5226, 0.5226)  # Modificar saturación (Q)
    return yiq_mod

# Valores de ajuste
a = 0.5  # Factor de reducción de luminancia
b = 1.3  # Factor de aumento de saturación
modif_yiq = modificarYIQ(yiq, a, b)

# Mostrar la imagen modificada en YIQ
plt.figure(8)
plt.imshow(modif_yiq)
plt.title('Imagen YIQ Modificada')
plt.show()

# Función para transformar de YIQ a RGB
def YIQaRGB(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:,:,0] = np.clip(yiq[:,:,0] + 0.9663*yiq[:,:,1] + 0.6210*yiq[:,:,2], 0, 1)  # Banda R
    rgb[:,:,1] = np.clip(yiq[:,:,0] - 0.2721*yiq[:,:,1] - 0.6474*yiq[:,:,2], 0, 1)  # Banda G
    rgb[:,:,2] = np.clip(yiq[:,:,0] - 1.1070*yiq[:,:,1] + 1.7046*yiq[:,:,2], 0, 1)  # Banda B
    return rgb

# Convertir la imagen modificada de YIQ de nuevo a RGB
rgb2 = YIQaRGB(modif_yiq)

# Mostrar la imagen RGB final obtenida y la original
plt.figure(9)
plt.imshow(img)
plt.title('Imagen Original en RGB')

plt.figure(10)
plt.imshow(rgb2)
plt.title('Imagen RGB Transformada desde YIQ Modificada')
plt.show()
