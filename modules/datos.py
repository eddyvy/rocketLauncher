
"""
Modulo para leer y escribir los datos en la carpeta de almacenamiento.

NOTA: Los archivos se abren con "with open('file.txt') as f" ya que se evita tener que cerrarlos cada vez que se utilizan (f.close())

Imports:
    Para leer y escribir datos se utiliza el formato json, por lo que se importa este modulo de python para ello.
        Para leer los datos se utiliza la funcion load() y para escribir la funcion .dump() que acepta parametros como sort_keys o ident para dar formato.
    Se importa el modulo path para conseguir la ruta de un archivo o directorio

Constantes:
    RUTA_ALMACENAMIENTO: Constante con la ruta de la carpeta de almacenamiento

Funciones:
    rutaArchivo(nombreArchivo): Retorna un string con la ruta del archivo donde se guardan los datos:
        Parametro:
            nombreArchivo: El nombre que tiene el archivo (ej: 'cohetes.json')
    
    ordenarLista(lista, clave): Se le pasa una lista y la ordena de menor a mayor, se utiliza una tecnica llamada selection sort
        Parametros:
            lista: La lista con los elementos a ordenar
            clave: al pasar la clave, opcional, se ordenan segun esa clave de los objetos de la lista
        
        1. Se recorre la lista y se guarda el i�ndice desordenado
        2. Se recorre de nuevo y se compara el elemento del i�ndice desordenado con los siguientes, si el elemento del inDes es mayor, se giran los elementos
        3. Retorna la lista ordenada
    
    crearArchivo(nombreArchivo): Crear un nuevo archivo donde se crea un diccionario con un unico elemento:
        Parametro:
            nombreArchivo: El nombre que se desea poner al archivo (ej: 'cohetes.json')
        
        1. Se crea el string con la ruta del archivo, utilizando la funcion creada
        2. Se obtiene el nombre del archivo sin su extension (sin ".json")
        3. Se crea el nuevo diccionario con un elemento, cuya clave es el nombre del archivo (sin .json) y cuyo valor es una lista vacia
        4. Se crea el archivo utilizando el modulo json, al usar modo 'x' si existe el archivo se generara un error

    leerArchivo(nombreArchivo): Lee y retorna los datos del archivo json como un diccionario
        Parametros:
            nombreArchivo: El nombre que tiene el archivo (ej: 'cohetes.json')

        1. Se comprueba si existe el archivo (con su ruta y la funcion exists del modulo os.path), y si no existe se devuelve False
        2. Se abre el archivo en modo lectura y se retorna el valor de lo lei�do usando el modulo json

    guardarEnArchivo(nombreArchivo, nuevoDic): Guarda un diccionario a la lista del archivo
        Parametros:
            nombreArchivo: El nombre que tiene el archivo (ej: 'cohetes.json')
            nuevoDic: El nuevo diccionario a anadir al archivo (ej: {'idTipo': 'Falcon 1', 'cargaUtil': 670, 'cantidad': 1})

        1. Si leer archivo da False entonces se crea un nuevo archivo con ese nombre
        2. Se lee el archivo json obteniendo un diccionario con un elemento cuyo valor es la lista de diccionarios
            2.1. Se obtiene el nombre del archivo sin su extension (sin ".json"), que es la clave con valor la lista de diccionarios
            2.2. Se obtiene la lista de diccionarios con la clave antes obtenida
            2.3. Se agrega con append el nuevo diccionario que queremos a�adir a la lista
        3. Se sobrescriben los datos, agregando los actualizados

    eliminarDeArchivo(nombreArchivo, adiosDic): Elimina un diccionario de la lista del archivo:
        Parametros:
            nombreArchivo: El nombre que tiene el archivo (ej: 'cohetes.json')
            nuevoDic: El diccionario a eliminar del archivo (ej: {'idTipo': 'Falcon 1', 'cargaUtil': 670, 'cantidad': 1})

        1. Si el archivo no existe, leerArchivo retorna False y esta funcion tambien acabara retornando False
        2. Se lee el archivo json obteniendo un diccionario con un elemento cuyo valor es la lista de diccionarios
            2.1. Se obtiene el nombre del archivo sin su extension (sin ".json"), que es la clave con valor la lista de diccionarios
            2.2. Se obtiene la lista de diccionarios con la clave antes obtenida
            2.3. Se elimina con remove el diccionario que queremos eliminar de la lista
        3. Se sobrescriben los datos, con los actualizados que ya no tienen el diccionario eliminado
"""

import json
from os import path

RUTA_ALMACENAMIENTO = './store'


def rutaArchivo(nombreArchivo):
    return RUTA_ALMACENAMIENTO + '/' + nombreArchivo


def ordenarLista(lista, clave):
    if not clave:
        # 1
        for i in range(len(lista)):

            inDes = i
            # 2
            for j in range(i+1, len(lista)):
                if lista[inDes] > lista[j]:
                    inDes = j
            
            lista[i], lista[inDes] = lista[inDes], lista[i]
        # 3
        return lista
    else:
        # 1
        for i in range(len(lista)):

            inDes = i
            # 2
            for j in range(i+1, len(lista)):
                if lista[inDes][clave] > lista[j][clave]:
                    inDes = j
            
            lista[i], lista[inDes] = lista[inDes], lista[i]
        # 3
        return lista


def crearArchivo(nombreArchivo):
    # 1
    rutaArchivo(nombreArchivo)
    # 2
    claveArchivo = nombreArchivo.split('.')[0]
    # 3
    archivoNuevo = {
            claveArchivo: []
        }
    # 4
    with open(rutaArchivo(nombreArchivo), 'x') as jsonNuevo:
        json.dump(archivoNuevo, jsonNuevo, sort_keys=True, indent=4)
        

def leerArchivo(nombreArchivo):
    # 1
    if not path.exists(rutaArchivo(nombreArchivo)):
        return False
    # 2
    with open(rutaArchivo(nombreArchivo), 'r') as jsonLeido:
        return json.load(jsonLeido)


def guardarEnArchivo(nombreArchivo, nuevoDic):
    # 1
    if not leerArchivo(nombreArchivo):
        crearArchivo(nombreArchivo)
    # 2
    dicArchivo = leerArchivo(nombreArchivo)
    claveArchivo = nombreArchivo.split('.')[0]  # 2.1
    listaDic = dicArchivo[claveArchivo]         # 2.2
    listaDic.append(nuevoDic)                   # 2.3
    # 3
    with open(rutaArchivo(nombreArchivo), 'w') as jsonGuardado:
        json.dump(dicArchivo, jsonGuardado, sort_keys=True, indent=4)


def eliminarDeArchivo(nombreArchivo, adiosDic):
    # 1
    if not leerArchivo(nombreArchivo):
        return False
    # 2
    dicArchivo = leerArchivo(nombreArchivo)
    claveArchivo = nombreArchivo.split('.')[0]  # 2.1
    listaDic = dicArchivo[claveArchivo]         # 2.2
    listaDic.remove(adiosDic)                   # 2.3
    # 3
    with open(rutaArchivo(nombreArchivo), 'w') as jsonGuardado:
        json.dump(dicArchivo, jsonGuardado, sort_keys=True, indent=4)