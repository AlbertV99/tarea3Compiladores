import tabla_simbolos as t
import tarea_compiladores as lexer
ARCHIVO_ENTRADA = 'prueba.txt'
EOF = ''
token = '' #declaramos como variable global
linea = 1
cadena = ''
posicion = 0
lista_errores = []
def main():
    tabla = t.TablaSimbolos()

    with open(ARCHIVO_ENTRADA) as fichero:
        try:
            cadena = lexer.procesar_fichero(fichero,tabla)
            # print(cadena +"\n longitud = "+ str(len(cadena)))
        except Exception as e:
            print("Error lexico")
            print(e)
        else:
            analizador_sintactico(cadena)
    fichero.close()


def analizador_sintactico(dato):
    global cadena
    global lista_errores
    cadena = dato
    get_token()
    json()
    if(len(lista_errores)<1):
        print('Sintaxis correcta')
    else:
        print("Han ocurrido errores a nivel sintactico")
        print(lista_errores)

def match(token_esperado) :
    if (token == token_esperado) : # aqui se compara con el token actual
        # print ("hice match con " + token)
        get_token()
        if (token == '') :
            get_token()
    else :
        raise Exception ('ha ocurrido un error se esperaba ----> ' + token_esperado) #+str(posicion)

#aqui se actualiza el valor del token por el siguiente que viene en el fichero
def get_token():

    global token #aqui le decimos que queremos utilizar la variable global creada
    global linea
    global cadena
    global posicion
    token = ''
    caracter =''
    while (posicion <len(cadena)) :
        if(caracter!='\t'):
            token += caracter

        caracter = cadena[posicion]
        posicion+=1
        if (caracter == '' or caracter == '\n' or caracter == ' ') :
            break

def json() :

    element ()

def element () :
    global lista_errores
    if (token == 'L_LLAVE') :
        object()
    elif (token == 'L_CORCHETE'):
        array ()
    else:
        raise Exception ('ha ocurrido un error en la linea ' + str(posicion))


def object ():
    global token
    try:
        match ('L_LLAVE')
        if (token == 'R_LLAVE') :
            match ('R_LLAVE')
        else :
            atribute_list()
            match ('R_LLAVE')

    except Exception as e:
        lista_errores.append(str(e)+" - "+str(posicion))
        while (token != 'R_LLAVE'):
            get_token()
        match('R_LLAVE')
        # raise Exception("Error al obtener objeto")

def array ():
    global token
    try:
        match ('L_CORCHETE')
        if (token == 'R_CORCHETE') :
            # print ("es una lista vacia")
            match ('R_CORCHETE')
        else :
            element_list()
            match('R_CORCHETE')
    except Exception as e:
        lista_errores.append(str(e))
        while (token != 'R_CORCHETE'):
            get_token()
        match('R_CORCHETE')

def element_list() :
    try:
        element()
        A_prima()
    except Exception as e:
        raise e

def A_prima():

    try:
        if (token == 'COMA') :
            match('COMA')
            element()
            A_prima()
        else :
            # print ("lista vacia")
            return #se cumple con el caso base
    except:
        raise Exception("ha ocurrido un error en A_prima() en la linea "+ str(linea))

def atribute_list() :
    try :
        atribute()
        B_prima()
    except Exception as e:
        raise e

def atribute ():

        atribute_name()
        match ('DOS_PUNTOS')
        atribute_value()

def B_prima():

    try :
        if (token == 'COMA'):
            match('COMA')
            atribute()
            B_prima()
        else :
            return # se cumple con el caso base

    except Exception as e:
        raise e

def atribute_name ():

    try :
        match ('STRING')
    except:
        raise Exception("Se esperaba token : STRING")

def atribute_value():

    if (token == 'L_CORCHETE' or token == 'L_LLAVE') :
        element()
    elif (token == 'STRING'):
        match('STRING')
    elif (token == 'NUMBER'):
        match('NUMBER')
    elif (token == 'PR_FALSE'):
        match('PR_FALSE')
    elif (token == 'PR_TRUE'):
        match('PR_TRUE')
    elif (token == 'PR_NULL'):
        match('PR_NULL')
    else:
        raise Exception('ha ocurrido un error en atribute_value.Se esperaba token :> STRING | NUMBER | CORCHETE | LLAVE | BOOLEANO | NULL <')


if (__name__ == '__main__') :
    # get_token() #tomamos el primer token del archivo
    # json()
    # fichero.close()
    main()
