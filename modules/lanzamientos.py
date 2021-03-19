"""
Modulo donde creamos misiones, lanzamientos de misiles, se guardan en un el archivo de lanzamientos.json.

Imports:
    Se importa el modulo que se creo para guardar y leer los datos almacenados
    Se importa el modulo de dias para poder utilizar el dia actual
    Se importa el modulo de cohetes para poder elegirlos para su lanzamiento

Constantes:
    ARCHIVO_LANZAMIENTOS: Constante con el nombre del archivo donde se almacenan los datos de los lanzamientos

Funciones:
    listarLosLanzamientos(): Lista todos los lanzamientos
        1. Devuelve una lista con todos los diccionarios de lanzamientos

    mostrarLanzamientos(): Muestra los lanzamientos con formato adecuado:
        1. Se comprueba si existe el archivo, si no existe se informa de que no hay lanzamientos que mostrar
        2. Se recorren los lanzamientos y se muestran

    __anadirLanzamiento(): Permite anadir un nuevo lanzamiento
        1. Se utiliza la funcion de mostrarCohetes() de cohetes.py para mostrar la informacion disponible y conseguir un diccionario con opcion y tipo de cohete
        2. Se compara la eleccion del usuario entre las del diccionario y se identifica el idTipo que corresponde y se guarda en idEleccion
            2.1. Si se escribe el id directamente tambien funcionara
        3. Se recorren todos los cohetes para comprobar que la cantidad es suficiente, si lo es se llama a la funcion para restar 1 a la cantidad.
        4. Se pregunta cuantos dias tarda hasta la estacion
        5. Si el numero es negativo se pide de nuevo
        6. Se crea un id unico para el lanzamiento
            6.1. Si hay archivo con lanzamientos se listan los lanzamientos
                6.1.1. Se buscan los que tengan el mismo modelo de cohete que el que se esta ingresando
                6.1.2. Se genera un id con el idTipo y el numero siguiente total (ejemplo Falcon 1-lan2)
            6.2. Si no existe el archivo es que es el primer lanzamiento
        7. Se guardan los datos en un nuevo diccionario y se envian al json, el dia de lanzamiento aun no se asigna

    __menuLanzamientos(): Despliega el menu de este modulo:
        1. Se despliega el menu de lanzamientos
        2. Segun eleccion se ejecuta la funcion que corresponda

    __salir(): Pregunta si queremos salir o introducir mas datos:
        * Para detalles vease la comentarios de __salir() en el modulo cohetes.py

    run(): Arrancar el modulo con todas las funciones:
        * Para detalles vease la comentarios de run() en el modulo cohetes.py
"""

from modules import datos
from modules import dias
from modules import cohetes

ARCHIVO_LANZAMIENTOS = 'lanzamientos.json'


def listarLosLanzamientos():
    # 1
    return datos.leerArchivo(ARCHIVO_LANZAMIENTOS)['lanzamientos']


def mostrarLanzamientos():
    # 1
    if not datos.leerArchivo(ARCHIVO_LANZAMIENTOS):
        print('No hay lanzamientos registrados')
        return
    # 2
    listaLanzamientos = listarLosLanzamientos()
    listaLanzamientos = datos.ordenarLista(listaLanzamientos, 'idLanzamiento')
    
    print('Estamos a dia', dias.hoy())
    for lanzamiento in listaLanzamientos:
        print(lanzamiento['idLanzamiento'], 'Dias a la estacion:', lanzamiento['diasTarda'], 'Dia del lanzamiento:', lanzamiento['diaLanzamiento'])
        
    print('')


def __anadirLanzamiento():
    # 1
    print('Has seleccionado realizar un nuevo lanzamiento.')
    print('Estos son los cohetes disponibles:')
    dicOpciones = cohetes.mostrarCohetes(1)

    # 2
    eleccion = input('Elige el cohete que asignar lanzamiento: ')

    for opcion in dicOpciones:
        if eleccion == opcion or eleccion == dicOpciones[opcion]:   # 2.1
            idEleccion = dicOpciones[opcion]
    
    # 3
    listaCohetes = cohetes.listarLosCohetes()
    for cohete in listaCohetes:
        if cohete['idTipo'] == idEleccion:
            if cohete['cantidad'] <= 0:
                print('No quedan suficientes cohetes de este modelo')
                return
            else:
                cohetes.cambiarCantidadCohete(cohete, -1)

    # 4
    diasTarda = int(input('Cuantos dias tarda hasta llegar a la estacion? '))

    # 5
    while diasTarda < 0:
        print('Ese numero es negativo y... ¿dias negativos?')
        diasTarda = float(input('Escribe de nuevo el numero de dias, por favor: '))

    # 6
    if datos.leerArchivo(ARCHIVO_LANZAMIENTOS):     # 6.1
        listaLanzamientos = listarLosLanzamientos()
        contarIds = 1
        for lanzamiento in listaLanzamientos:
            if lanzamiento['idTipo'] == idEleccion :   # 6.1.1
                contarIds += 1
        
        idLanzamiento = idEleccion + ' - lan' + str(contarIds)   # 6.1.2
    else:   # 6.2
        idLanzamiento = idEleccion + ' - lan1'

    # 7
    nuevoLanzamiento = {
        'idTipo': idEleccion,
        'diasTarda': diasTarda,
        'idLanzamiento': idLanzamiento,
        'diaLanzamiento': 'sin asignar'
    }
    datos.guardarEnArchivo(ARCHIVO_LANZAMIENTOS, nuevoLanzamiento)
    print('')


def __menuLanzamientos():
    # 1
    print(
        'Has elegido la opcion de crear lanzamientos.',
        'Elige la opcion que deseer realizar:',
        '1. Crear un nuevo lanzamiento',
        '2. Mostrar los lanzamientos',
    sep='\n')

    # 2
    seleccion = input()
    print('')
    if seleccion == '1':
        __anadirLanzamiento()
    elif seleccion == '2':
        mostrarLanzamientos()
    else:
        print('Por favor, selecciona una opcion valida')


def __salir():
    malInput = True
    
    while malInput:
        print(
            '¿Deseas volver al menu de lanzamientos?',
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


def run():
    salirModulo = False

    while not salirModulo:
        __menuLanzamientos()
        salirModulo = __salir()