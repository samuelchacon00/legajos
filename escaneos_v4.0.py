import tkinter as tk
from tkinter.font import Font
import os,subprocess,PyPDF2,time
import pandas as pd
from PyPDF2 import PdfMerger
from datetime import datetime

modo_escaneo="Modo Legajos"
modo_color="blue"
est=0

alto_botones=150
ancho_etiquetas=84
altura_anuncio=210
ancho_anuncio=80
flag_caja=0
cantidad="conteo.txt"

#   las rutinas son las funciones que son llamadas
#   cuando un evento ocurre y ese evento es un boton que ha sido presionado

#   ---rutina
#   funcion que se utiliza para ejecutar la funcion ingresar
#   cuando se aprieta el boton o cuando se presiona enter
def Dale_Enter(event):
    ingresar()

#   recibe una lista de objetos pdf y los combina en ese orden
def armar(pdfs):
    nombre_archivo_salida = "salida.pdf"
    fusionador=PdfMerger()

    for pdf in pdfs:
        fusionador.append(open(pdf,'rb'))

    with open(nombre_archivo_salida,'wb') as salida:
        fusionador.write(salida)


#   toma el nombre del campo legajo y cambia el nombre del unico pdf suelto en el directorio
#   y crea un directorio con el mismo nombre, mueve el pdf adentro de dicho directorio y este directorio
#   adentro del directorio que tiene como nombre el campo Caja, si este no esta deja el directorio del
#   legajo suelto
def ingresar():
    nombre_legajo=LegajoBox.get()

    if("." in nombre_legajo):
        if not control.get():
            punto=nombre_legajo.split(".")
            elemento=punto[0]
            elemento+="."
            index=elemento.index(".")
            LegajoBox.delete(index+1,tk.END)
        else:
            LegajoBox.delete(0,tk.END)   
    else:
        LegajoBox.delete(0,tk.END)

    info2.config(text="")
    info3.config(text="")

    lista=os.listdir()
    filtro=[]

    for n in lista:
        if(n[-4:]==".pdf"):
            filtro.append(n)    
    
    cant=len(filtro)

    if(cant==0):
        mensaje1="No se encuentra ningun pdf"
        color="red"
    elif(cant>1):
        mensaje1="Hay mas de un pdf"
        color="red"
 
    if(cant==1):
        archivo=filtro[0]

        nombre_caja=CajaBox.get()
        if(nombre_caja==None or not nombre_caja in lista):
            flag_caja=0
        else:
            flag_caja=1

        if(nombre_legajo==None):
            if(est==1):
                mensaje1="Falta legajo!"
            else:
                mensaje1="Falta nombre!"
            color="red"
        else:

            if(est==1):
                subprocess.run(["rename",archivo,nombre_legajo+".pdf"],shell=True)
                if(flag_caja):
                    subprocess.run(["move",nombre_legajo+".pdf",nombre_caja],shell=True)
                mensaje1="Hecho!"
                color="green"
            else:        
                arch=open(archivo,"rb")
                pdf=PyPDF2.PdfReader(arch)
                copias=len(pdf.pages)
                arch.close()

                sumar_numero(copias)
            
                subprocess.run(["mkdir",nombre_legajo],shell=True)
                subprocess.run(["rename",archivo,nombre_legajo+".pdf"],shell=True)
                subprocess.run(["move",nombre_legajo+".pdf",nombre_legajo],shell=True)
                if(flag_caja):
                    subprocess.run(["move",nombre_legajo,nombre_caja],shell=True)

                mensaje1="Hecho! El pdf contiene "+str(copias)+" paginas"
                color="green"

    info1.config(text=mensaje1,foreground=color)

#   ---rutina--
#   lee la cantidad de paginas de cada pdf y las suma, esto funciona si los directorio de los legajos estan
#   dentro de otro directorio y por supuesto este esta en el campo Caja
def ver_escaneos():
    nombre_caja=CajaBox.get()
    if len(nombre_caja) and os.path.exists(nombre_caja) and os.path.isdir(nombre_caja):
        listado=os.listdir(nombre_caja)
        copias=0
        for legdir in listado:
            nom=nombre_caja+"\\"+legdir+"\\"+legdir+".pdf"
            arch=open(nom,"rb")
            pdf=PyPDF2.PdfReader(arch)
            copias+=len(pdf.pages)
            arch.close()
        mensaje2="Hay "+str(copias)+" escaneos"    
        info2.config(text=mensaje2,foreground="blue")
    else:
        mensaje2="el directorio \""+nombre_caja+"\" no existe!"
        info2.config(text=mensaje2,foreground="red")

#   ---rutina--
#   combina los pdf que estan en el directorio actual por orden de llegada 
def combinar():
    if(est==1):
        return

    lista=os.listdir()

    filtro=[]
    for n in lista:
        if(n[-4:] == ".pdf"):
            filtro.append(n)
    
    if(len(filtro)<=1):
        mensaje3="No hay suficientes archivos para combinar"
        color="red"
    else:
        fechas=[]

        for n in filtro:            
            fechas.append(datetime.fromtimestamp(os.stat(n).st_mtime))
        
        filtro=list(pd.DataFrame({"archivos":filtro,"fecha":fechas}).sort_values(by="fecha").reset_index()["archivos"])
        
        fusionador=PdfMerger()

        for pdf in filtro:
            fusionador.append(open(pdf, 'rb'))

        with open("salida.pdf",'wb') as salida:
            fusionador.write(salida)

        t=len(filtro)

        for n in filtro:
            os.remove(n) 

        mensaje3="hecho! se unieron "+str(t)+" pdfs."
        color="#106000"

    info3.config(text=mensaje3,foreground=color)

#   ---rutina--
#   funcion para cambiar el modo, funcion incompleta
def toggle_mode():
    return """funcion incompleta"""
    global est
    if(est==0):
        est=1
        modo_color="purple1"
        modo_escaneo="Modo Suelto"
        la_caja.config(text="Carpeta")
        Legajo.config(text="Nombre")
        MODO.config(text=modo_escaneo,foreground=modo_color)
    else:
        est=0
        modo_color="blue"
        modo_escaneo="Modo Legajos"
        la_caja.config(text="Caja")
        Legajo.config(text="Legajo")
        MODO.config(text=modo_escaneo,foreground=modo_color)


ventana=tk.Tk()
ventana.title("escaneos 4.0")
ventana.config(width=400,height=300)

#:::::::::::::::::::::Fuentes::::::::::::::::::::::::

fuente=Font(family="Roboto Cn",size=14)

#_-__-__-__-__-__-Etiquetas-__-__-__-__-__-__-

control=tk.IntVar()
check=tk.Checkbutton(ventana,text="borrar todo",variable=control)
check.place(x=280,y=65)
#control.pack()

MODO=tk.Label(text=modo_escaneo,font=fuente,foreground=modo_color)
MODO.place(x=130,y=10)

la_caja=tk.Label(text="Caja")
la_caja.place(x=ancho_etiquetas,y=50)

Legajo=tk.Label(text="Legajo")
Legajo.place(x=ancho_etiquetas,y=90)

info1=tk.Label(text="")
info1.place(x=ancho_anuncio,y=altura_anuncio)

info2=tk.Label(text="")
info2.place(x=ancho_anuncio,y=altura_anuncio+30)

info3=tk.Label(text="")
info3.place(x=ancho_anuncio,y=altura_anuncio+60)

#-=-=-=-=-=-=-=-=Botones=-=-=-=-=-=-=-=-=-=-=-=

hecho=tk.Button(text="Ingresar",command=ingresar)
hecho.place(x=50,y=alto_botones)

ver=tk.Button(text="Ver escaneos",command=ver_escaneos)
ver.place(x=110,y=alto_botones)

combinar=tk.Button(text="Combinar",command=combinar)
combinar.place(x=200,y=alto_botones)

toggle=tk.Button(text="Cambiar Modo",command=toggle_mode)
toggle.place(x=270,y=alto_botones)

#+-+-+-+-+-+-+-+-Cajas de texto-+-+-+-+-+-+-+-+-+

CajaBox=tk.Entry()
CajaBox.place(x=140,y=50)

LegajoBox=tk.Entry()
LegajoBox.place(x=140,y=90)

LegajoBox.bind('<Return>',Dale_Enter)

ventana.mainloop()