"""
Modulo donde incrementamos en numero de cohetes, ya sean de un modelo ya existente en nuestra lista o un nuevo modelo para nuestra lista.

Imports:
    Se importa el modulo que se creo para guardar y leer los datos almacenados

Constantes:
    ARCHIVO_COHETES: Nombre del archivo donde se almacenan los datos de los cohetes

Funciones:
    listarLosCohetes(): Para listar todos los cohetes registrados
        1. Devuelve una lista con todos los diccionarios de los cohetes

    cambiarCantidadCohete(coheteAnterior, suma = 1): Incrementa la cantidad de cohetes que hay de ese tipo
        Parametros:
            coheteAnterior: Es el diccionario del tipo de cohete al que se le va a cambiar la cantidad
            suma: Es la cantidad de cohetes que se van a sumar, por defecto es 1, se puede aceptar un valor negativo para restar
        1. Se realiza una copia del diccionario para actualizarlo
        2. Se cambia la cantidad del nuevo diccionario creado para que encaje con la actualizada
        3. Si quedan menos de 0 cohetes, se retorna False
        4. Se actualizan los datos eliminando el cohete con la cantidad desactualizada y guardando el cohete con la cantidad actualizada

    mostrarCohetes(num = 2): Lista los tipos de cohetes en forma de opciones para el menu
        1. Las opciones del menu dependen del numero de cohetes que hay en la base de datos
            1.1. Se consigue la lista con todos los cohetes
            1.2. Se inicia un contador para escribir el numero de opcion del menu, la parte del listado a escribir aqui empieza por la 2a opcion
                se pasa a variable para poder utilizarse en otro modulo con el numero que se desee
                1.2.1 Se ordena la lista por su idTipo
            1.3. Se inicializa un diccionario vacio para devolverlo luego con claves opcion y valores idTipo
            1.4. En el bucle listamos los cohetes, mostrando el numero de opcion, el modelo y la cantidad que hay
                1.4.1. Se agrega una clave y un valor al diccionario creado (ej: {"1": "Falcon 1", "2": "Falcon Heavy"})
        2. Se retorna el valor del diccionario que liga las opciones con los tipos de cohete

    __anadirCohete(): Para añadir un nuevo modelo de cohete:
        1. Se pide el nuevo modelo/tipo de cohete al usuario
            1.1. Comprobacion de que la palabra tiene por lo menos 3 caracteres
        2. Se comprueba si el input que se da coincide con un modelo ya registrado:
            2.1. Se comprueba si existe el archivo, si no al guardar se creara
            2.2. Se leen los datos de anteriores cohetes llamando a la funcion anteriormente creada
            2.3. Se recorre el listado de cohetes para comprobar que el input (idTipo) no esta repetido en el listado
                2.3.1. Sale de la funcion entera para volver a preguntar
        3. Se pide la carga util del nuevo cohete al usuario
        4. Si se ingresa un numero negativo se pide al usuario ingresar el numero de nuevo
        5. Se crea un diccionario con los datos
            5.1. El programa esta pensado para añadir los cohetes de uno en uno
        6. Se guardan los datos en el almacenamiento

    __usarEleccion(dicOpciones): Pide la eleccion del usuario y la utiliza para ejecutar la funcion que corresponda:
        Parametro:
            dicOpciones: El diccionario que liga opciones con tipos de cohete (ej: {"1": "Falcon 1", "2": "Falcon Heavy"})
        1. Se recibe la opcion del usuario
        2. Si la opcion es 1, entonces quiere añadir un nuevo modelo de cohete, pues se llama a la funcion indicada
        3. Si la opcion es agregar un cohete al listado de modelos ya existentes, se busca en dicOpciones
            3.1. Con la opcion elegida y el diccionario dicOpciones se halla el idTipo que ha elegido el usuario
            3.2. Se recorre el listado de cohetes y se busca el seleccionado
            3.3. Cuando se encuentra se ejecuta la funcion para aumentar en 1 la cantidad

    __menuCohetes(): Para desplegar el menu de este modulo:
        1. Se despliega la confirmacion del modulo seleccionado, la peticion de que el usuario elija y la primera opcion del menu, añadir un nuevo tipo de cohete
        2. Se comprueba que existe el archivo para continuar
        3. Se guarda el diccionario con opciones y tipos de cohete que devuelve mostrarCohetes()
        4. Por ultimo se llama a la funcion que activa las funciones segun la eleccion del usuario

    __salir(): Pregunta si queremos salir o introducir mas datos:
        1. Validacion de la respuesta que nos da el usuario
            1.1. Se inicializa con True la variable para salir del bucle si se cambia a False
            1.2. Se pregunta al usuario si desea salir
                1.2.1. Si el input recibido es para continuar se sale del ciclo y se devuelve False
                1.2.2. Si el input recibido es para salir se sale del ciclo y se devuelve True

    run(): Arranca el modulo con todas las funciones:
        1. Se inicializa la variable de salir del modulo con False
        2. Mientras la variable sea False, se repite el programa
            2.1. Se recibe un valor de True o False de la funcion __salir() para salir o para volver a iniciar el modulo
"""

from modules import datos

ARCHIVO_COHETES = 'cohetes.json'


def listarLosCohetes():
    # 1
    return datos.leerArchivo(ARCHIVO_COHETES)['cohetes']


def cambiarCantidadCohete(coheteAnterior, suma = 1):
    # 1
    coheteNuevo = coheteAnterior.copy()
    # 2
    coheteNuevo['cantidad'] = coheteAnterior['cantidad'] + suma
    # 3
    if coheteNuevo['cantidad'] < 0:
        return False
    # 4
    datos.eliminarDeArchivo(ARCHIVO_COHETES, coheteAnterior)
    datos.guardarEnArchivo(ARCHIVO_COHETES, coheteNuevo)


def mostrarCohetes(num = 2):
    # 1
    listaCohetes = listarLosCohetes()   # 1.1
    listaCohetes = datos.ordenarLista(listaCohetes, 'idTipo')   # 1.2.1
    opcion = num                        # 1.2
    dicOpciones = {}                    # 1.3
    for cohete in listaCohetes:         # 1.4
        print(str(opcion) + '.', cohete['idTipo'], '(Hay ' + str(cohete['cantidad']) + ' unidades disponibles)')
        dicOpciones[str(opcion)] = cohete['idTipo'] # 1.4.1
        opcion += 1
    # 2
    return dicOpciones


def __anadirCohete():
    # 1
    print('Has seleccionado añadir un cohete de un modelo nuevo')
    idTipo = input('¿Cual es el nombre (identificador) del modelo?: ')
    
    while len(idTipo) < 3:  # 1.1
        input('La palabra debe tener por lo menos 3 caracteres: ')

    # 2
    if datos.leerArchivo(ARCHIVO_COHETES):      # 2.1
        listaCohetes = listarLosCohetes()       # 2.2
        for cohete in listaCohetes:             # 2.3
            if idTipo == cohete['idTipo']:
                print(
                    'Ya existe un tipo de cohete con esa identificacion',
                    'por lo que no se han agregado datos',
                sep='\n')
                return  # 2.3.1
    # 3
    cargaUtil = int(input('¿Cual es la carga util de este tipo de cohete? (en Kg): '))
    # 4
    while cargaUtil < 0:
        print('Ese numero es negativo y... llevar carga negativa es dificil')
        cargaUtil = int(input('Escribe de nuevo la carga util, por favor: '))
    # 5
    nuevoCohete = {
        'idTipo': idTipo,
        'cargaUtil': cargaUtil,
        'cantidad': 1,  # 5.1
    }
    # 6
    datos.guardarEnArchivo(ARCHIVO_COHETES, nuevoCohete)
    print('')
    

def __usarEleccion(dicOpciones):
    # 1
    numeroElegido = input()
    print('')
    # 2
    if numeroElegido == '1':
        __anadirCohete()
        return
    # 3
    if numeroElegido in dicOpciones:
        tipoCoheteElegido = dicOpciones[numeroElegido]  # 3.1
        for cohete in listarLosCohetes():               # 3.2
            if cohete['idTipo'] == tipoCoheteElegido:   # 3.3
                cambiarCantidadCohete(cohete)
    # 4
    else:
        print('Esa opcion no esta disponible')


def __menuCohetes():
    # 1
    print(
        'Has seleccionado la opcion de añadir cohetes.',
        'Selecciona el modelo de cohete que deseas añadir:',
        '1. Nuevo tipo de cohete',
    sep='\n')
    # 2
    if not datos.leerArchivo(ARCHIVO_COHETES):
        datos.crearArchivo(ARCHIVO_COHETES)
    # 3
    dicOpciones = mostrarCohetes()
    # 4
    __usarEleccion(dicOpciones)
    

def __salir():
    # 1
    malInput = True # 1.1
    
    while malInput:
        print(
            '¿Deseas introducir de nuevo un cohete?',
            '1. Si',
            '2. No',
        sep='\n')
        salirMenu = input() # 1.2
        print('')

        if salirMenu == '1' or salirMenu.lower() == 'si':
            malInput = False
            return False    # 1.2.1
        elif salirMenu == '2' or salirMenu.lower() == 'no':
            malInput = False
            return True     # 1.2.2
        else:
            print('Por favor, ingresa una respuesta valida')


def run():
    # 1
    salirModulo = False
    # 2
    while not salirModulo:
        __menuCohetes()
        salirModulo = __salir() # 2