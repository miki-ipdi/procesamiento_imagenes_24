# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:27:15 2024

@author: Micaela
"""
from tkinter import Tk,Label,Button,Entry, Frame,filedialog,messagebox, Scale
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import imageio
import numpy as np

def RGBaYIQ(img):
    yiq = np.zeros(img.shape) # crea una matriz vacía para almacenar una imagen transformada en un espacio de color YIQ
    yiq[:,:,0] = 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]  # Y (luminancia)
    yiq[:,:,1] = 0.595716*img[:,:,0] - 0.274453*img[:,:,1] - 0.321263*img[:,:,2]  # I (In-phase)
    yiq[:,:,2] = 0.211456*img[:,:,0] - 0.522591*img[:,:,1] + 0.311135*img[:,:,2]  # Q (Quadrature)
    return yiq

def YIQaRGB(yiq):
    rgb = np.zeros(yiq.shape)
    rgb[:,:,0] = yiq[:,:,0] + 0.9663*yiq[:,:,1] + 0.6210*yiq[:,:,2] #BandaR
    rgb[:,:,1] = yiq[:,:,0] - 0.2721*yiq[:,:,1] - 0.6474*yiq[:,:,2] #BandaG
    rgb[:,:,2] = yiq[:,:,0] - 1.1070*yiq[:,:,1] + 1.7046*yiq[:,:,2] #BandaB
    return rgb

def more_ligther(yiq):
    result = np.zeros(yiq.shape)
    result[:,:,0] = np.sqrt(yiq[:,:,0])
    result[:,:,1] = yiq[:,:,1]
    result[:,:,2] = yiq[:,:,2]
    return result

def more_darker(yiq):
    result = np.zeros(yiq.shape)
    result[:,:,0] = yiq[:,:,0] * yiq[:,:,0]
    result[:,:,1] = yiq[:,:,1]
    result[:,:,2] = yiq[:,:,2]
    return result

class FrMain(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.matriz_imagen1 = np.ones((100, 100, 3), dtype=np.uint8)
        self.matriz_imagen2 = np.ones((100, 100, 3), dtype=np.uint8)
        self.grid()
    
        
        self.frame1 = Frame(self, width=350, height=700,bg="red")# width es ancho, height es altura, bg me asigna el color
        self.frame1.grid_propagate(False)
        self.frame1.grid()
        self.fr_subimg1 = Frame(self.frame1, width=300, height=300)
        self.fr_subimg1.grid(padx=25, pady= 10)
        self.lbl_img1 = Label(self.fr_subimg1)
        
        self.fr_frecuencia1 = Frame(self.frame1, width=450, height=300)
        self.fr_frecuencia1.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_frecuencia1 = Label(self.fr_frecuencia1)
        self.txt_frecuencia1= Label(self.fr_frecuencia1,text="Frecuencia")
        self.lbl_frecuencia1.grid(row=1,column=1)
        
        self.frame1.grid(row=0, column=0)
        
        self.frame2 = Frame(self, width=350, height=700,bg="blue")# width es ancho, height es altura, bg me asigna el color
        self.frame2.grid_propagate(False)
        self.frame2.grid()
        self.fr_subimg2 = Frame(self.frame2, width=300, height=300)
        self.fr_subimg2.grid(padx=25, pady= 10)
        self.lbl_img2 = Label(self.fr_subimg2)
        
        self.fr_frecuencia2 = Frame(self.frame2, width=450, height=300)
        self.fr_frecuencia2.grid(row=1, column=0, padx=10, pady=10)
        self.lbl_frecuencia2 = Label(self.fr_frecuencia2)
        self.txt_frecuencia2= Label(self.fr_frecuencia2,text="Frecuencia")
        self.lbl_frecuencia2.grid(row=1,column=1)
        
        self.frame2.grid(row=0, column=1)
        
        self.frame3 = Frame(self, width=350, height=400,bg="green")
        self.frame3.grid_propagate(False)
        self.frame3.grid()
        
        self.btn_open = Button(self.frame3, text="abrir imagen", command=lambda:self.abrir_imagen(self.lbl_img1))
        self.btn_open.grid()

        self.btn_operation = Button(self.frame3, text="Calcular")
        self.btn_operation['command'] = self.calculate
        self.btn_operation.grid()
        
        # Menú desplegable con Combobox
        self.lbl_dropdown = Label(self.frame3, text="Selecciona una opción:")
        self.lbl_dropdown.grid(pady=10)
        
        self.combobox = Combobox(self.frame3, values=["Raiz", "Exponencial"])
        self.combobox.grid()
        
        self.frame3.grid(row=0, column=2)

        

    def abrir_imagen(self, lbl_img):
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
            self.matriz_imagen1 = imageio.imread(ruta_imagen)
            
    def calculate(self):
        img_clip = np.clip(self.matriz_imagen1/255,0.,1.) #normalizando [0,1]
        yiq = RGBaYIQ(img_clip)
        self.calculate_histogram(yiq[:,:,0].flatten(),self.fr_frecuencia1)
        
        if (self.combobox.get() == 'Raiz'):
            yiq_modificado = more_ligther(yiq)
        if (self.combobox.get() == 'Exponencial'):
            yiq_modificado = more_darker(yiq)
        
        rgb = YIQaRGB(yiq_modificado)
        
        # image_tk2 = ImageTk.PhotoImage(image=Image.fromarray(np.clip((rgb*255),0.,255.).astype('uint8')).resize((300, 300)))
        image_tk2 = ImageTk.PhotoImage(image=Image.fromarray(self.matriz_imagen1).resize((300, 300)))
        
        self.lbl_img2.config(width=300, height=300)
        self.lbl_img2.config(image=image_tk2)
        self.lbl_img2.image = image_tk2
        self.lbl_img2.grid()
        fig, ax = plt.subplots(figsize=(4, 3))
        canvas = FigureCanvasTkAgg(fig, master=self.fr_frecuencia2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        self.calculate_histogram(yiq_modificado[:,:,0].flatten(),self.fr_frecuencia2)
       
       
    def calculate_histogram(self,values,frecuencia):
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.set(title='Histograma')
        n, bins, patches = ax.hist(values, bins=20, range=(0,1), density=True)    
        altura_total = np.sum(n)
        factor_de_escala = 100 / altura_total
        n *= factor_de_escala
        # Graficar el histograma escalado
        ax.bar(bins[:-1], n, width=np.diff(bins), align="edge", edgecolor='black')
        # Establecer límite en el eje y hasta 100%
        ax.set_ylim(0, 100)     
        canvas = FigureCanvasTkAgg(fig, master=frecuencia)# Crea el area de dibujo en Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
    
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
    root.wm_title("TP 5 Luminancia") #me permite cambiar el titulo de la ventana// root.iconbitmap ("dir directorio")
    app = FrMain(root)
    app.mainloop() #con este metodo permitimos ver y ejecutar la ventana