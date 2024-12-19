# -*- coding: utf-8 -*-
"""
@author: Micaela
"""

from tkinter import Tk,Label,Button,Frame,filedialog #libreria para crear la raiz
from PIL import Image, ImageTk
import imageio.v2 as imageio
import numpy as np 
import matplotlib.pyplot as plt
from tkinter.ttk import Combobox
from scipy.ndimage import convolve

KERNEL_BARLET_3X3 = np.array([[1,2,1], [2,4,2], [1,2,1]])
KERNEL_BARLET_5X5 = np.array([
    [1,2,3,2,1], 
    [2,4,6,4,2], 
    [3,6,9,6,3], 
    [2,4,6,4,2], 
    [1,2,3,2,1]
    ])
KERNEL_BARLET_7X7 = np.array([
    [1,2,3,4,3,2,1], 
    [2,4,6,8,6,4,2], 
    [3,6,9,12,9,6,3], 
    [4,8,12,16,12,8,4], 
    [3,6,9,12,9,6,3],
    [2,4,6,8,6,4,2],
    [1,2,3,4,3,2,1]
    ])
KERNEL_GAUSSIANO_5X5 = np.array([[1, 4, 6, 4, 1], [4, 16, 24, 16, 4], [6, 24, 36, 24, 6], [4, 16, 24, 16, 4], [1, 4, 6, 4, 1]])
KERNEL_LAPLACIANO_V4 = np.array([[0,-1,0], [-1,4,-1], [0,-1,0]])
KERNEL_LAPLACIANO_V8 = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])

def apply_convolution(image, kernel):
    return convolve(image, kernel, mode='constant', cval=0.0)

def RGBaYIQ(img):
    yiq = np.zeros(img.shape) # crea una matriz vacía para almacenar una imagen transformada en un espacio de color YIQ
    yiq[:,:,0] = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]  # Y (luminancia)
    yiq[:,:,1] = 0.595716*img[:,:,0] - 0.274453*img[:,:,1] - 0.321263*img[:,:,2]  # I (In-phase)
    yiq[:,:,2] = 0.211456*img[:,:,0] - 0.522591*img[:,:,1] + 0.311135*img[:,:,2]  # Q (Quadrature)
    return yiq
    
class FrMain(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.matriz_imagen1 = np.ones((100, 100, 3), dtype=np.uint8)
        self.grid()
        
        
        self.frame1 = Frame(self, width=350, height=400,bg="red")# width es ancho, height es altura, bg me asigna el color
        self.frame1.grid_propagate(False)
        self.frame1.grid()
        self.fr_subimg = Frame(self.frame1, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_img1 = Label(self.fr_subimg)
        self.btn_open = Button(self.frame1, text="abrir imagen", command=lambda:self.abrir_imagen(self.lbl_img1, 1))
        self.btn_open.grid()
        
        self.frame1.grid(row=0, column=0)
        
        self.frame3 = Frame(self, width=350, height=400,bg="blue")
        self.frame3.grid_propagate(False)
        self.frame3.grid()
        self.fr_subimg = Frame(self.frame3, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_resultado = Label(self.fr_subimg)
        self.btn_open = Button(self.frame3, text="Guardar")
        self.btn_open["command"] = lambda: self.guardar_imagen()
        self.btn_open.grid()
        
        self.frame3.grid(row=0, column=1)
        
        self.fr_btn = Frame(self, width=700, height=200,bg="yellow")
        self.fr_btn.grid_propagate(False)
        self.fr_btn.grid()
        
        # Menú desplegable con Combobox
        self.lbl_dropdown = Label(self.fr_btn, text="Selecciona una opción:")
        self.lbl_dropdown.grid(pady=10)
        
        self.combobox = Combobox(self.fr_btn, values=["Pasabajo Barlet 3x3",
                                                      "Pasabajo Barlet 5x5",
                                                      "Pasabajo Barlet 7x7",
                                                      "Pasabajo Gaussiano 5x5",
                                                      "Pasaalto Laplaciano V4", 
                                                      "Pasaalto Laplaciano V8"])
        self.combobox.grid()

        # Evento que detecta el cambio en el combobox
        self.combobox.bind("<<ComboboxSelected>>", self.ejecutar_funcion)
        
        self.fr_btn.grid(row=1, column=0,columnspan=3)
        

    def abrir_imagen(self, lbl_img, num_img):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            # Abre la imagen seleccionada con Pillow
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((300,300))
            # Convierte la imagen a un formato que tkinter pueda mostrar
            imagen_tk = ImageTk.PhotoImage(imagen)
            lbl_img.config(width=300, height=300)
            lbl_img.config(image=imagen_tk)
            lbl_img.image = imagen_tk  # Conserva una referencia para evitar que la imagen sea destruida por el recolector de basur
            lbl_img.grid()
            if num_img == 1:
                self.matriz_imagen1 = imageio.imread(ruta_imagen)
            if num_img == 2:
                self.matriz_imagen2 = imageio.imread(ruta_imagen)
    
    def ejecutar_funcion(self, event):
        seleccion = self.combobox.get()
        img_rgb_clip = np.clip(self.matriz_imagen1/255, 0., 1.)
        yiq = RGBaYIQ(img_rgb_clip)
        img_luminancia = yiq[:,:,0]
        if seleccion == "Pasabajo Barlet 3x3":
            filtro = self.barlet(img_luminancia, 3)
        if seleccion == "Pasabajo Barlet 5x5":
            filtro = self.barlet(img_luminancia, 5)
        if seleccion == "Pasabajo Barlet 7x7":
            filtro = self.barlet(img_luminancia, 7)
        if seleccion == "Pasabajo Gaussiano 5x5":
            filtro = self.gaussiano(img_luminancia, 5)
        
        if seleccion == "Pasaalto Laplaciano V4":
            filtro = self.laplaciano(img_luminancia, 4)
        
        if seleccion == "Pasaalto Laplaciano V8":
            filtro = self.laplaciano(img_luminancia, 8)
        
        self.mostrar_resultado(filtro)

    def barlet(self, luminancia, tipo):
        if tipo == 3:
            kernel = KERNEL_BARLET_3X3/KERNEL_BARLET_3X3.sum()
        if tipo == 5:
            kernel = KERNEL_BARLET_5X5/KERNEL_BARLET_5X5.sum()
        if tipo == 7:
            kernel = KERNEL_BARLET_7X7/KERNEL_BARLET_7X7.sum()
        filtro = apply_convolution(luminancia, kernel)
        return filtro
    
    def gaussiano(self, luminancia, tipo):
        if tipo == 5:
            kernel = KERNEL_GAUSSIANO_5X5 /KERNEL_GAUSSIANO_5X5.sum()
        filtro = apply_convolution(luminancia, kernel)
        return filtro
    
    def laplaciano(self, luminancia, version):
        if version == 4:
            kernel = KERNEL_LAPLACIANO_V4 
        else:
            kernel = KERNEL_LAPLACIANO_V8  
        filtro = apply_convolution(luminancia, kernel)
        return filtro
    
    
    def mostrar_resultado(self, resultado):
        self.resultado_imagen = (resultado * 255).astype("uint8") #asigno un valor a la imagen distinto de none(vacio)
        image_tk = ImageTk.PhotoImage(image=Image.fromarray((resultado*255).astype("uint8")).resize((300, 300)))
        self.lbl_resultado.config(width=300, height=300)
        self.lbl_resultado.config(image=image_tk)
        self.lbl_resultado.image = image_tk 
        self.lbl_resultado.grid()
        
    def guardar_imagen(self):
        if self.resultado_imagen is not None:
            ruta_guardar = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if ruta_guardar:
                imagen_a_guardar = Image.fromarray(self.resultado_imagen)
                imagen_a_guardar.save(ruta_guardar)
                print(f"Imagen guardada en {ruta_guardar}")
        else:
            print("No hay imagen para guardar")


if __name__ == "__main__":
    root = Tk()  #se hace el llamado a la clase tk//para cambiar el icomo: img.ico 
    root.wm_title("TP 3 Convolucion") #me permite cambiar el titulo de la ventana// root.iconbitmap ("dir directorio")
    app = FrMain(root)
    app.mainloop() #con este metodo permitimos ver y ejecutar la ventana