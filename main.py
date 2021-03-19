"""
Proyecto 1, Logistica para la estacion espacial

Autor: Eduard Valls Yue
"""
"""
Este es el programa principal que llama al resto de modulos y funciones

Imports:
    Se importan todos los modulos creados para que se ejecuten las distintas funcionalidades del programa a excepcion del de datos

Funciones:
    desplegarMenu(): Despliega el menu con las distintas opciones para elegir
        1. Se utiliza el separador "\n" para dar formato de saltos de linea

    elegirModulo(): Recibe el input del usuario y arranca el modulo que se ha seleccionado:
        1. Se lee la eleccion del menu del usuario
        2. Segun la eleccion se ejecuta el modulo que corresponda
            2.1. Se devuelve True para salir del bucle del programa principal

    run(): Funcion principal que inicia el programa llamando al resto de funciones
        1. Boolean que al cambiar a True hara que salgamos del programa
        2. Bucle para no salir del programa principal sin input del usuario
            2.1. Si la funcion elegirModulo devuelve True, se sale del programa principal 
"""

from modules import cohetes
from modules import peticiones
from modules import lanzamientos
from modules import asignar
from modules import dias
from modules import informacion


def desplegarMenu():
    print(
        '\n¡Bienvenido al sistema de de suministros para la estacion espacial!',
        'Elija una de las siguientes opciones:',
        '1. Insertar nuevo cohete en el hangar',
        '2. Realizar nueva peticion para la estacion',
        '3. Disponer nuevo lanzamiento',
        '4. Asignar peticiones a lanzamientos',
        '5. Avanzar dias / cambiar fecha simulacion',
        '6. Informacion del sistema',
        '7. Salir',
    sep='\n') # 1


def elegirModulo():
    # 1
    eleccion = input()
    print('')
    # 2
    if eleccion == '1':
        cohetes.run()
    elif eleccion == '2':
        peticiones.run()
    elif eleccion == '3':
        lanzamientos.run()
    elif eleccion == '4':
        asignar.run()
    elif eleccion == '5':
        dias.run()
    elif eleccion == '6':
        informacion.run()
    elif eleccion == '7' or eleccion.lower() == 'salir':
        return True # 2.1
    else:
        print('Por favor, elige una opcion valida')


def run():
    # 1
    salirPrograma = False
    # 2
    while not salirPrograma:
        desplegarMenu()
        salirPrograma = elegirModulo()  # 2.1


"""
Convencion para arrancar la funcion principal del programa, run()
"""
if __name__ == '__main__':
    run()