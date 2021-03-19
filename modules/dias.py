"""
Modulo para realizar los calculos de dias y para avanzarlos como se desee

Imports:
    Se importa el modulo time para utilizar la funcion de espera (sleep)
    Se importa el modulo que se creo para guardar y leer los datos almacenados
    Se importa el modulo de informacion para mostrar el estado de los lanzamientos

Constantes:
    ARCHIVO_DIA: es el nombre del archivo donde se almacena el dia actual de la simulacion
    DIA_INICIAL: es la fecha 0 que se le da a la simulacion del programa
    PAUSA: segundos que tarda un dia en pasar al darle avanzar a la simulacion

Funciones:
    hoy(): Obtiene el dia actual de la simulacion
        1. Si hay archivo dia.json, lo lee y devuelve el dia guardado
            1.1. Se lee el dia del json
            1.2. Se retorna el dia
        2. Si no existe el archivo se crea por defecto en dia 1 y devuelve dicho dia
            2.1. Se guarda en un diccionario
            2.2. Al guardar se creara el archivo con ese diccionario
            2.3. Igual que 1.1
            2.4. Igual que 1.2

    __actualizarDia(diaNuevo): Guarda el dia en el archivo de dias.json
        Parametros:
            diaNuevo: dia que se actualiza, formato integer

        1. Se elimina el dia anteriormente guardado
        2. Se agrega el nuevo dia, de nuevo pasando a formato diccionario
        NOTA: Si no existe el archivo no habra error y se creara al guardar, ya que las funciones de leer y eliminar simplemente retornaran False

    __avanzarDias(numDias): Hacer avanzar los dias:
        Parametros:
            numDias: numero de dias a avanzar
        
        1. Se van pasando los dias que se han recibido del usuario
            1.1. Se suma un dia a la fecha actual con timedelta
            1.2. Se actualiza la fecha
            1.3. Se da una pausa para dar sensacion de paso de tiempo

    __menuDias(): Ejecuta el menu de opciones de del modulo:
        1. Se muestra la bienvenida al menu y se da opcion de avanzar o hacer reset
        2. Si selecciona avanzar, se pide el numero de dias a avanzar
            2.1. Se lee el numero de dias a avanzar como integer
            2.2. Si el numero a avanzar es menor que uno se pide al usuario que vuelva a escribirlo
            2.3. Se llama a la funcion para avanzar dias pasandole el numero a avanzar
        3. Si selecciona resetear se pregunta si esta seguro de que desea hacerlo
            3.1. Antes de ello, si el programa ya esta en el dia inicial, se le informa al usuario y se sale del mismo
            3.2. Si es que si, entonces se vuelve a la fecha por defecto
            3.3. Si es que no o un mal input, se escribe un mensaje y no se hace nada mas

    __salir(): Pregunta si queremos salir o introducir mas datos:
        * Para detalles vease la comentarios de __salir() en el modulo cohetes.py

    run(): Arrancar el modulo con todas las funciones:
        * Para detalles vease la comentarios de run() en el modulo cohetes.py
"""

import time
from modules import datos
from modules import informacion

ARCHIVO_DIA = 'dia.json'
DIA_INICIAL = 1
PAUSA = 0.5


def hoy():
    # 1
    if datos.leerArchivo(ARCHIVO_DIA):
        diaHoy = datos.leerArchivo(ARCHIVO_DIA)['dia'][0]['hoy']        # 1.1
        return diaHoy  # 1.2
    # 2
    else:
        diaPorDefecto = {
            'hoy': DIA_INICIAL,                                         # 2.1
        }
        datos.guardarEnArchivo(ARCHIVO_DIA, diaPorDefecto)              # 2.2
        diaHoy = datos.leerArchivo(ARCHIVO_DIA)['dia'][0]['hoy']        # 2.3
        return diaHoy  # 2.4


def __actualizarDia(diaNuevo):
    # 1
    dicDiaAnterior = datos.leerArchivo(ARCHIVO_DIA)['dia'][0]
    datos.eliminarDeArchivo(ARCHIVO_DIA, dicDiaAnterior)
    # 2
    dicDiaNuevo = {
        'hoy': diaNuevo
    }
    datos.guardarEnArchivo(ARCHIVO_DIA, dicDiaNuevo)


def __avanzarDias(numDias):
    # 1
    for dia in range(numDias):
        # 1
        print('\nEstamos a dia', hoy())
        informacion.mostrarEstadoLanzamientos()
        mañana = hoy() + 1               # 1.1
        __actualizarDia(mañana)          # 1.2
        time.sleep(PAUSA)                 # 1.3
    print('\nHemos llegado al dia', hoy())
    informacion.mostrarEstadoLanzamientos()


def __menuDias():
    # 1
    print(
        'Bienvenido al modulo para avanzar dias',
        'Selecciona la opcion que desees realizar:',
        '1. Avanzar dias en la simulacion',
        '2. Volver a la fecha de inicio (resetear a dia ' + str(DIA_INICIAL) +')',
    sep='\n')
    eleccion = input()
    # 2
    if eleccion == '1':
        numeroDias = int(input('Selecciona el numero de dias que deseas avanzar: '))  # 2.1

        while numeroDias < 1:                                                         # 2.2
            print('Por favor, debes introducir por lo menos 1 dia para que el programa se ejecute:')
            input('Selecciona de nuevo el numero de dias que deseas avanzar en esta simulacion:')

        __avanzarDias(numeroDias)                                                     # 2.3
    # 3
    elif eleccion == '2':
        if hoy() == DIA_INICIAL:    # 3.1
            print('¡Ya estamos en la fecha de inicio!\n')
            return
        
        print(
            '¿Estas seguro que deseas volver a la fecha inicial?',
            '1. Si',
            '2. No',
        sep='\n')

        resetear = input()

        if resetear == '1' or resetear.lower() == 'si':     # 3.2
            __actualizarDia(DIA_INICIAL)
        elif resetear == '2' or resetear.lower() == 'no':   # 3.3
            print ('No se resetea la fecha')
        else:
            print('Eso no es una respuesta valida, no se resetea la fecha')

    else:
        print('Esa no es una opcion valida')

    print('')


def __salir():
    malInput = True
    
    while malInput:
        print(
            '¿Deseas volver a modificar dias?',
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
        __menuDias()
        salirModulo = __salir()