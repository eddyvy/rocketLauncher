"""
Modulo donde realizamos peticiones, se guardan en un listado de peticiones.

Imports:
    Se importa el modulo que se creo para guardar y leer los datos almacenados
    Se importa el modulo de dias para poder utilizar el dia actual

Constantes:
    ARCHIVO_PETICIONES: Nombre del archivo donde se almacenan los datos de las peticiones

Funciones:
    listarLasPeticiones(): Lista todas los peticiones
        1. Devuelve una lista con todos los diccionarios de peticiones

    mostrarPeticiones(): Muestra las peticiones con formato adecuado:
        1. Se comprueba si existe el archivo, si no existe se informa de que no hay peticiones que mostrar
        2. Se recorren las peticiones y se muestran

    __anadirPeticion(): Permite anadir una nueva peticion
        1. Se solicita el identificador de la peticion
            1.1. Comprobacion de que la palabra tiene por lo menos 3 caracteres
        2. Se compara con el resto de identificadores de la lista para que no coincida
            2.1. Se comprueba si existe el archivo json, si no al guardar despues se creara
            2.2. Se leen los datos de anteriores peticiones llamando a la funcion anteriormente creada
            2.3. Se recorre el listado de peticiones
                2.3.1. Sale de la funcion entera para volver a preguntar
        3. Se solicita la descripcion
        4. Se solicita el peso y se obtiene como numero flotante
        5. Si el peso es negativo se pide de nuevo
        6. Se redondea hasta el 3r decimal
        7. Se solicita el maximo numero de dias
        8. Se comprueba que no sea negativo
        9. Se implementan los datos en un diccionario nuevo, incluyendo el dia que se ha realizado la peticion y con el campo de lanzamiento sin asignar
        10. Se guardan los datos

    __menuPeticiones(): Despliega el menu de este modulo:
        1. Se despliega el menu de peticiones
        2. Segun eleccion se ejecuta la funcion que corresponda

    __salir(): Pregunta si queremos salir o introducir mas datos:
        * Para detalles vease la comentarios de __salir() en el modulo cohetes.py

    run(): Arrancar el modulo con todas las funciones:
        * Para detalles vease la comentarios de run() en el modulo cohetes.py
"""
from modules import datos
from modules import dias

ARCHIVO_PETICIONES = 'peticiones.json'


def listarLasPeticiones():
    # 1
    return datos.leerArchivo(ARCHIVO_PETICIONES)['peticiones']


def mostrarPeticiones():
    # 1
    if not datos.leerArchivo(ARCHIVO_PETICIONES):
        print('Todavia no hay peticiones registradas')
        return
    # 2
    listaPeticiones = listarLasPeticiones()
    listaPeticiones = datos.ordenarLista(listaPeticiones, 'idPeticion')
    for peticion in listaPeticiones:
        print(peticion['idPeticion'], peticion['descripcion'], 'peso', peticion['peso'], 'Kg', 'maxDias', peticion['maxDias'])

    print('')


def __anadirPeticion():
    # 1
    print('Has seleccionado realizar una nueva peticion.')
    idPeticion = input('Ingresa el identificador unico de tu peticion: ')

    while len(idPeticion) < 3:  # 1.1
        idPeticion = input('La palabra debe tener por lo menos 3 caracteres: ')

    # 2
    if datos.leerArchivo(ARCHIVO_PETICIONES):   # 2.1
        listaPeticiones = listarLasPeticiones() # 2.2
        for peticion in listaPeticiones:        # 2.3
            if idPeticion == peticion['idPeticion']:
                print(
                    'Ya existe una peticion con esa identificacion',
                    'por lo que no se han agregado datos',
                sep='\n')
                return  # 2.3.1
    
    # 3
    descripcion = input('Escribe la descripcion de la peticion: ')

    # 4
    peso = float(input('Introduce el peso en Kg (hasta 3 decimales): '))

    # 5
    while peso < 0:
        print('Ese numero es negativo y... llevar carga negativa es dificil')
        peso = float(input('Escribe de nuevo el peso, por favor: '))

    # 6
    peso = round(peso, 3)
    # 7
    maxDias = int(input('Escribe el numero maximo de dias que debe tardar en llegar: '))

    # 8
    while peso < 0:
        print('Ese numero es negativo y... ¿dias negativos?')
        peso = float(input('Escribe de nuevo los dias, por favor: '))

    # 9
    nuevaPeticion = {
        'idPeticion': idPeticion,
        'descripcion': descripcion,
        'peso': peso,
        'maxDias': maxDias,
        'diaPeticion': dias.hoy(),
        'lanzamientoAsignado': 'sin asignar',
    }
    # 10
    datos.guardarEnArchivo(ARCHIVO_PETICIONES, nuevaPeticion)
    print('')


def __menuPeticiones():
    # 1
    print(
        'Has elegido la opcion de realizar peticiones.',
        'Elige la opcion que deseer realizar:',
        '1. Enviar nueva peticion',
        '2. Ver todas las peticiones',
    sep='\n')
    # 2
    seleccion = input()
    print('')
    if seleccion == '1':
        __anadirPeticion()
    elif seleccion == '2':
        mostrarPeticiones()


def __salir():
    malInput = True
    
    while malInput:
        print(
            '¿Deseas volver al menu de peticiones?',
            '1. Si',
            '2. No',
        sep='\n')
        salirMenu = input()
        print('')

        if salirMenu == '1' or salirMenu.lower() == 'si':
            malInput = False
            return False
        elif salirMenu == '2' or salirMenu.lower() == 'no':
            malInput = False
            return True
        else:
            print('Por favor, ingresa una respuesta valida')
            print('')


def run():
    salirModulo = False

    while not salirModulo:
        __menuPeticiones()
        salirModulo = __salir()