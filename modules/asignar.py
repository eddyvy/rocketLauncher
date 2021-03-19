"""
Modulo donde asignamos lanzamientos y peticiones.

Imports:
    Se importa el modulo de dias para poder utilizar el dia actual
    Se importan los modulo de cohetes, lanzamientos y de peticiones
    Se importa el modulo de datos para ordenar listas y para actualizar datos

Funciones:
    __hallarCargaQueCabe(lanzamiento): Halla la carga que cabe en el lanzamiento
        1. Se recorre el listado de cohetes
            1.1. Cuando coinciden los idTipo es que ese cohete corresponde a ese lanzamiento
            1.2. Obtiene la carga total que puede caber
        2. Se recorren las peticiones y si corresponden a ese lanzamiento, se reta la carga a la que cabe

    __asignar(diasParaLanzamiento = 0): Se ejecuta el algoritmo que asigna las peticiones con lanzamientos y guarda los datos
        Parametro:
            diasParaLanzamiento: Dias que quedan para realizar los lanzamientos, por defecto es 0 (para dia actual) y se deja por si se desa dar la opcion en el futuro
        
        1. Se recorre la lista de cohetes que se pasa como parametros, comprobandose la existencia de los archivos
        2. Se asigna el dia de lanzamiento a los lanzamientos y se guardan los datos
            2.1. Si el lanzamiento no tiene dia asignado se le asigna ahora
            2.2. Se guarda como elemento el dia que llegara el lanzamiento
        4. Se recorren las peticiones y se calcula, en funcion del di�a que se crean y el maxDias, el dia que debe llegar como maximo la peticion
            4.1. Se anaden a los diccionarios de esta lista estas cantidades
        5. Se ordenan las listas en funcion de la prioridad temporal
        6. En este momento ocurre la magia de la asignacion, se asignan de manera optima las peticiones a los lanzamientos
            6.0. Se salta el lanzamiento si ese lanzamiento ya ha despegado
            6.1. Se halla con la funcion __hallarCargaUtil cuanta carga cabe en el lanzamiento y se calcula que dia llega
            6.2. Se recorren las peticiones
                6.2.1. Si la peticion no tiene asignacion se continua, si tiene entonce no hace falta darsela
                6.2.2. Entonces, si cuando esta bien que llegue la peticion es despues o el mismo dia que llega, se continua
                6.2.3. Se resta a la carga que cabe la carga de la peticion
                6.2.4. Si este numero es negativo, entonces no cabe en el lanzamiento, se devuelve al valor anterior por si cabe la siguiente carga
                6.2.5. Si cabe, se asigna a la peticion el lanzamiento, si elimina el atributo temporal 'diaQueDebeLlegar' para poder eliminarlo de memoria y luego guardarlo actualizado
        7. Se comprueba si quedan peticiones sin asignar, y se informa al usuario
                


    __menuAsignar(): Despliega el menu de opciones y ejecuta la funcion que corresponda segun eleccion
        1. Se ejecuta la asignacion con los lanzamientos realizandose inmediatamente

    __salir(): Pregunta si queremos salir o introducir mas datos:
        * Para detalles vease la comentarios de __salir() en el modulo cohetes.py

    run(): Arrancar el modulo con todas las funciones:
        * Para detalles vease la comentarios de run() en el modulo cohetes.py
"""

from modules import dias
from modules import cohetes
from modules import lanzamientos
from modules import peticiones
from modules import datos


def __hallarCargaQueCabe(lanzamiento):
    # 1
    listaCohetes = cohetes.listarLosCohetes()
    for cohete in listaCohetes:
        if cohete['idTipo'] == lanzamiento['idTipo']:   # 1.1
            cargaQueCabe = cohete['cargaUtil']             # 1.2
    # 2
    listaPeticiones = peticiones.listarLasPeticiones()
    for peticion in listaPeticiones:
        if peticion['lanzamientoAsignado'] == 'sin asignar':
            cargaQueCabe = cargaQueCabe
        elif peticion['lanzamientoAsignado'] == lanzamiento['idLanzamiento']:
            cargaQueCabe -= peticion['peso']
    return cargaQueCabe


def __asignar(diasParaLanzamiento = 0):
    # 1
    if not datos.leerArchivo(peticiones.ARCHIVO_PETICIONES):
        print('No hay peticiones registradas')
        return
    
    if not datos.leerArchivo(lanzamientos.ARCHIVO_LANZAMIENTOS):
        print('No hay lanzamientos registrados')
        return

    listaPeticiones = peticiones.listarLasPeticiones()
    listaLanzamientos = lanzamientos.listarLosLanzamientos()

    # 2
    diaDeLanzamiento = dias.hoy() + diasParaLanzamiento

    for lanzamiento in listaLanzamientos:
        
        if lanzamiento['diaLanzamiento'] == 'sin asignar':  # 2.1
            datos.eliminarDeArchivo(lanzamientos.ARCHIVO_LANZAMIENTOS, lanzamiento)
            lanzamiento['diaLanzamiento'] = diaDeLanzamiento
            datos.guardarEnArchivo(lanzamientos.ARCHIVO_LANZAMIENTOS, lanzamiento)

        diaQueLlega = lanzamiento['diaLanzamiento'] + lanzamiento['diasTarda']
        lanzamiento['diaQueLlega'] = diaQueLlega                # 2.2

    # 4
    for peticion in listaPeticiones:
        diaQueDebeLlegar = peticion['maxDias'] + peticion['diaPeticion']
        peticion['diaQueDebeLlegar'] = diaQueDebeLlegar         # 4.1

    # 5
    listaPeticiones = datos.ordenarLista(listaPeticiones, 'diaQueDebeLlegar')
    listaLanzamientos = datos.ordenarLista(listaLanzamientos, 'diaQueLlega')
    
    # 6
    for lanzamiento in listaLanzamientos:
        # 6.0
        if lanzamiento['diaLanzamiento'] < dias.hoy():
            continue
        # 6.1
        lanzamiento['cargaQueCabe'] = __hallarCargaQueCabe(lanzamiento)
        diaQueLlega = lanzamiento['diaQueLlega']
        # 6.2
        for peticion in listaPeticiones:
            # 6.2.1
            if peticion['lanzamientoAsignado'] == 'sin asignar':
                # 6.2.2
                if peticion['diaQueDebeLlegar'] >= diaQueLlega:

                    lanzamiento['cargaQueCabe'] -= peticion['peso'] # 6.2.3

                    if lanzamiento['cargaQueCabe'] < 0: # 6.2.4
                        lanzamiento['cargaQueCabe'] += peticion['peso']

                    else:   # 6.2.5
                        peticion.pop('diaQueDebeLlegar')
                        datos.eliminarDeArchivo(peticiones.ARCHIVO_PETICIONES, peticion)
                        peticion['lanzamientoAsignado'] = lanzamiento['idLanzamiento']
                        datos.guardarEnArchivo(peticiones.ARCHIVO_PETICIONES, peticion)
                        print(
                            peticion['idPeticion'],
                            'ha sido asignada en',
                            lanzamiento['idLanzamiento'],
                            '\n Llegara en ',
                            diaQueLlega - dias.hoy(),
                            'dias',
                        )

    # 7
    haySinAsignar = False

    for peticion in listaPeticiones:

        if peticion['lanzamientoAsignado'] == 'sin asignar':
            haySinAsignar = True
            # 7.1
            if peticion['diaQueDebeLlegar'] < dias.hoy():
                print(
                    'La peticion',
                    peticion['idPeticion'],
                    'ha caducado porque ya tendria que haber llegado...',
                    '\n El dia maximo para llegar era dia',
                    peticion['diaQueDebeLlegar'],
                )
            else:
                print(
                    'Ha sido imposible asignar la peticion',
                    peticion['idPeticion'],
                    'o no cabe o no llegaria a tiempo',
                )

    if not haySinAsignar:
        print('No hay peticiones sin lanzamiento asignado')
    
    print('')


def __menuAsignar():
    print(
        'Bienvenido al asistente de asignar peticiones a lanzamientos',
        '¿Que deseas hacer?',
        '1. Asignar las peticiones y realizar los lanzamientos hoy',
        '2. No asignar nada todavia, salir',
    sep='\n')
    eleccion = input()
    print('')

    if eleccion == '1':
        __asignar()   # 1
    if eleccion == '2':
        return
    else:
        print('Pon una opcion valida, por favor')


def __salir():
    malInput = True
    
    while malInput:
        print(
            '¿Deseas volver al menu de asignar?',
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
        __menuAsignar()
        salirModulo = __salir()