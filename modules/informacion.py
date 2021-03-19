"""
Modulo donde mostramos la informacion y el estado actual del programa

Imports:
    Se importa modulo de datos para confirmar que existen los archivos
    Se importa el modulo de dias para poder utilizar el dia actual
    Se importan modulos de cohetes, peticiones y lanzamientos para su informacion

Funciones:
    mostrarInfoCohetes(): muestra la informacion de los cohetes
        1. Se comprueba si existe el archivo de cohetes
        2. Se recorre la lista de cohetes y se escriben en pantalla los datos
    
    mostrarInfoCohetes(): muestra la informacion de las peticiones
        1. Se comprueba si existe el archivo de peticiones
        2. Se recorre la lista de peticiones y se escriben en pantalla los datos

    mostrarEstadoLanzamientos(): muestra el estado de los lanzamientos
        1. Se comprueba si existe el archivo de lanzamientos
        2. Se recorre la lista de lanzamientos
            2.1. Si no hay dia de lanzamiento asignado se muestra
            2.2. Si tiene dia, se compara el dia actual con el dia que sale y que llega para mostrar el estado

    run(): Arrancar el modulo, muestra toda la informacion, llamando a las funciones para ello
"""
from modules import datos
from modules import dias
from modules import cohetes
from modules import peticiones
from modules import lanzamientos


def mostrarInfoCohetes():
    # 1
    if not datos.leerArchivo(cohetes.ARCHIVO_COHETES):
        print('No hay cohetes registrados')
        return

    # 2
    print('En el hangar quedan estos cohetes sin asignar lanzamiento:')
    listaCohetes = cohetes.listarLosCohetes()

    for cohete in listaCohetes:
        print(
            cohete['idTipo'],
            'Carga util:',
            cohete['cargaUtil'],
            'Kg',
            'Cantidad:',
            cohete['cantidad'],
        )


def mostrarInfoPeticiones():
    # 1
    if not datos.leerArchivo(peticiones.ARCHIVO_PETICIONES):
        print('No hay peticiones registradas')
        return

    # 2
    listaPeticiones = peticiones.listarLasPeticiones()
    
    for peticion in listaPeticiones:
        print(
            peticion['idPeticion'],
            peticion['descripcion'],
            'Peso:',
            peticion['peso'],
            'Kg',
            'Dia Limite: dia',
            peticion['maxDias'] + peticion['diaPeticion'],
            'Lanzamiento Asignado:',
            peticion['lanzamientoAsignado']
        )


def mostrarEstadoLanzamientos():
    # 1
    if not datos.leerArchivo(lanzamientos.ARCHIVO_LANZAMIENTOS):
        print('No hay lanzamientos registrados')
        return

    # 2
    listaLanzamientos = lanzamientos.listarLosLanzamientos()

    for lanzamiento in listaLanzamientos:
        # 2.1
        if lanzamiento['diaLanzamiento'] == 'sin asignar':
            print(
                lanzamiento['idLanzamiento'],
                'sin dia de lanzamiento asignado'
            )
        # 2.2
        else:
            diaSale = lanzamiento['diaLanzamiento']
            diaLlega = lanzamiento['diasTarda'] + diaSale

            if dias.hoy() < diaSale:
                print(
                    lanzamiento['idLanzamiento'],
                    'preparando motores',
                )
                print(
                    'Despegara dia',
                    diaSale,
                    'y llegara dia',
                    diaLlega
                )
            elif dias.hoy() == diaSale:
                print(
                    lanzamiento['idLanzamiento'],
                    'despega hoy mismo',
                )
                print(
                    'Llegara dia',
                    diaLlega
                )
            elif dias.hoy() > diaSale and dias.hoy() < diaLlega:
                print(
                    lanzamiento['idLanzamiento'],
                    'en ruta a la estacion',
                )
                print(
                    'Despego dia',
                    diaSale,
                    'y llegara dia',
                    diaLlega
                )
            elif dias.hoy() == diaLlega:
                print(
                    lanzamiento['idLanzamiento'],
                    'ha llegado hoy mismo',
                )
                print(
                    'Despego dia',
                    diaSale,
                )
            elif dias.hoy() > diaLlega:
                print(
                    lanzamiento['idLanzamiento'],
                    'ya esta en la estacion',
                )
                print(
                    'Despego dia',
                    diaSale,
                    'y llego dia',
                    diaLlega
                )


def run():
    print('\nEsta es la informacion del sistema:')
    print('Estamos a dia', dias.hoy())
    print('\nCohetes:')
    mostrarInfoCohetes()
    print('\nPeticiones:')
    mostrarInfoPeticiones()
    print('\nLanzamientos:')
    mostrarEstadoLanzamientos()