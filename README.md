# <h1 align=center> **Escaneo de legajos** </h1>

## Introduccion

Actualmente trabajo en la fotocopiadora de la facultad en la que estudio (UTN.BA), y desde hace un tiempo tenemos un servicio al departamentos de gestion academica, alumnos y deposito, este servicio consiste en el escaneo de los expedientes de los alumnos, en cada caja pueden haber entre 50 y 150 legajos aproximadamente, estos legajos se escanean no por uno y la impresora envia el archivo en pdf a la computadora, en el directorio donde envia el archivo, este pdf se le debe cambiar el nombre a numero del legajo por ejemplo 170.253-1.pdf y este debe ser movido a a un directorio con el nombre del legajo, cada uno de estos directorios con el nombre de su respectivo legajo van adentro de otro directorio que debe llevar el nombre de Caja N, donde N es el numero de la caja.

El objetivo del programa es facilitar esta tarea y hacerla mas eficiente.

## Descripcion del programa

El programa consiste en dos caja de texto, donde una es "Caja" y la otra es "Legajo", cuando haya un pdf solamente suelto en el directorio el programa va a tomar el nombre que hay en Legajo y va cambiar el nombre y creara un directorio con el mismo nombre y metera este pdf adentro de ese directorio, si en Caja hay texto y el directorio existe dentro del directorio actual, entonce mueve el directorio del legajo adentro deste directorio y muestra la cantidad de paginas que se acaban de ingresar, si no hay texto en el Caja simplemente lo dejara donde esta.

Tiene un boton para ver la cantidad de escaneos que hay dentro de un directorio que corresponde una caja.

Tiene otro que es para combinar los archivos por orden de llegada, a veces cuando se escanea se manda primero una parte y luego otra, y para hacer mas eficiente el trabajo de combinar 2 o varios archivos, el boton lo hace en un instante.

Tiene una casilla de seleccion que dice "borrar todo", si se estan escaneando unos legajos y justo se ecanea 170.253-1 el que le sigue es 170.254-x, y como el 170 sigue siendo igual borra todo hasta un '.' dejando 170. , si la casilla esta seleccionada borra todo despues de ingresar un legajo.

<p align="center">
<img src="https://github.com/samuelchacon00/legajos/blob/master/src/interfaz.png"  height=400></p>
