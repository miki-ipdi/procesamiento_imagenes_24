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

    
class FrMain(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.matriz_imagen1 = np.ones((100, 100, 3), dtype=np.uint8)
        self.matriz_imagen2 = np.ones((100, 100, 3), dtype=np.uint8)
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
        
        self.frame2 = Frame(self, width=350, height=400,bg="green")
        self.frame2.grid_propagate(False)
        self.frame2.grid()
        self.fr_subimg = Frame(self.frame2, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_img2 = Label(self.fr_subimg)
        self.btn_open = Button(self.frame2, text="abrir imagen", command=lambda:self.abrir_imagen(self.lbl_img2, 2))
        self.btn_open.grid()
        
        self.frame2.grid(row=0, column=1)
        
        self.frame3 = Frame(self, width=350, height=400,bg="blue")
        self.frame3.grid_propagate(False)
        self.frame3.grid()
        self.fr_subimg = Frame(self.frame3, width=300, height=300)
        self.fr_subimg.grid(padx=25, pady= 10)
        self.lbl_resultado = Label(self.fr_subimg)
        self.btn_open = Button(self.frame3, text="Guardar")
        self.btn_open["command"] = lambda: self.guardar_imagen()
        self.btn_open.grid()
        
        self.frame3.grid(row=0, column=2)
        
        self.fr_btn = Frame(self, width=1050, height=200,bg="yellow")
        self.fr_btn.grid_propagate(False)
        self.fr_btn.grid()
        
        # Menú desplegable con Combobox
        self.lbl_dropdown = Label(self.fr_btn, text="Selecciona una opción:")
        self.lbl_dropdown.grid(pady=10)
        
        self.combobox = Combobox(self.fr_btn, values=["Suma Clampeada", "Resta Promediada", "Valor Absoluto"])
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
        
        if seleccion == "Suma Clampeada":
            self.suma_clampeada(self.matriz_imagen1 / 255, self.matriz_imagen2 / 255)
        elif seleccion == "Resta Promediada":
            self.resta_promediada(self.matriz_imagen1 / 255, self.matriz_imagen2 / 255)
        elif seleccion == "Valor Absoluto":
            self.valor_absoluto(self.matriz_imagen1 / 255, self.matriz_imagen2 / 255)
    
    
    def suma_clampeada(self, rgb1, rgb2):
        print("suma")
        suma = np.zeros(rgb1.shape)
        suma[:,:,0] = np.clip(rgb1[:,:,0] + rgb2[:,:,0], 0, 1)  # Rojo
        suma[:,:,1] = np.clip(rgb1[:,:,1] + rgb2[:,:,1], 0, 1)  # Verde
        suma[:,:,2] = np.clip(rgb1[:,:,2] + rgb2[:,:,2], 0, 1)  # Azul
        plt.imshow(suma)
        self.mostrar_resultado(suma)
        
    def resta_promediada(self, rgb1, rgb2):
       print("resta")
       resta_promedio = np.zeros(rgb1.shape)
       resta_promedio[:, :, 0] = np.clip((rgb1[:, :, 0] - rgb2[:, :, 0]) / 2.0, 0, 1)  # Rojo
       resta_promedio[:, :, 1] = np.clip((rgb1[:, :, 1] - rgb2[:, :, 1]) / 2.0, 0, 1)  # Verde
       resta_promedio[:, :, 2] = np.clip((rgb1[:, :, 2] - rgb2[:, :, 2]) / 2.0, 0, 1)  # Azul
       self.mostrar_resultado(resta_promedio)
       
       
    def valor_absoluto(self, rgb1, rgb2):
        print("resta_VA")
        # Inicializa el array para almacenar la resta con valor absoluto
        resta_abs = np.zeros(rgb1.shape)

        # Aplica la resta con valor absoluto para cada canal
        resta_abs[:, :, 0] = np.clip(np.abs(rgb1[:, :, 0] - rgb2[:, :, 0]), 0, 1)  # Rojo
        resta_abs[:, :, 1] = np.clip(np.abs(rgb1[:, :, 1] - rgb2[:, :, 1]), 0, 1)  # Verde
        resta_abs[:, :, 2] = np.clip(np.abs(rgb1[:, :, 2] - rgb2[:, :, 2]), 0, 1)  # Azul
        self.mostrar_resultado(resta_abs)
    
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
    root.wm_title("TP 2 Aritmetica de pixeles") #me permite cambiar el titulo de la ventana// root.iconbitmap ("dir directorio")
    app = FrMain(root)
    app.mainloop() #con este metodo permitimos ver y ejecutar la ventana