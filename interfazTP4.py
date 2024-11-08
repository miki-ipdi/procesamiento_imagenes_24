# -*- coding: utf-8 -*-
"""
@author: Micaela
"""

from tkinter import Tk,Label,Button,Frame,filedialog #libreria para crear la raiz
from PIL import Image, ImageTk
import imageio.v2 as imageio
import numpy as np 
from tkinter.ttk import Combobox
from scipy import ndimage

KERNEL_3X3 = np.ones((3,3))
KERNEL_5X5 = np.ones((5,5))

def _morph_multiband(im, se, op):
    result = np.zeros(im.shape)
    offset = (np.array(se.shape)-1)//2
    im = np.pad(im,[(offset[0],offset[0]),(offset[1],offset[1]),(0,0)],'edge')
    for y, x in np.ndindex(result.shape[:2]):
        pixels = im[y:y+se.shape[0], x:x+se.shape[1]][se]
        result[y, x] = pixels[op(pixels[:,0])]
    return result

def _morph_color(im, se, op):
    im2 = (RGBaYIQ(im)[:, :, 0])[:, :, np.newaxis]
    im2 = np.concatenate((im2, im),axis=2)
    result = _morph_multiband(im2, se, op)[:, :, 1:]
    return result

def im_dilate(im, se):
    if im.ndim == 3:
        return _morph_color(im, se, np.argmax)
    else:
        return ndimage.grey_dilation(im, footprint = se)
    
def im_erode(im, se):
    if im.ndim == 3:
        return _morph_color(im, se, np.argmin)
    else:
        return ndimage.grey_erosion(im, footprint = se)

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
        
        self.combobox = Combobox(self.fr_btn, values=["Dilatacion 3x3",
                                                      "Dilatacion 5x5",
                                                      "Erosion 3x3",
                                                      "Erosion 5x5"])
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
        if seleccion == "Dilatacion 3x3":
            filtro = im_dilate(img_luminancia, KERNEL_3X3)
        if seleccion == "Dilatacion 5x5":
            filtro = im_dilate(img_luminancia, KERNEL_5X5)
        if seleccion == "Erosion 3x3":
            filtro = im_erode(img_luminancia, KERNEL_3X3)
        if seleccion == "Erosion 5x5":
            filtro = im_erode(img_luminancia, KERNEL_5X5)
        self.mostrar_resultado(filtro)

    
    
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
    root.wm_title("TP 4") #me permite cambiar el titulo de la ventana// root.iconbitmap ("dir directorio")
    app = FrMain(root)
    app.mainloop() #con este metodo permitimos ver y ejecutar la ventana
