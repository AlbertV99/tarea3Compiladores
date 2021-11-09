import tabla_simbolos as p
ARCHIVO_ENTRADA = 'prueba.txt'
ARCHIVO_SALIDA = 'salida.txt'
EOF = ''

def main():
    tabla = p.TablaSimbolos()
    inicializar_archivo_salida()
    with open(ARCHIVO_ENTRADA) as fichero:
        procesar_fichero(fichero,tabla)
    fichero.close()


def procesar_fichero(fichero,tabla):
    retorno=""
    caracter = '1'
    variable = ''
    token = ''
    linea = ''
    nro_linea = 1
    caracter = fichero.readline(1)
    tabs = 0
    while (caracter != EOF) :
        try:

            if (caracter == '\n') :
                retorno+=linea #+ '\n'
                linea = '' + ("\t"*tabs) # linea nueva
                nro_linea += 1
                caracter = fichero.readline(1)
                continue
            elif (caracter == ' '):
                caracter = fichero.readline(1)
                continue
            elif (caracter == EOF):
                break
            elif (caracter.lower() == 'f' or caracter.lower() == 't') : #quiere decir que lo mas probable es que venga un falso
                token = tabla.buscar(procesar_booleano(fichero,caracter))
            else:
                token = tabla.buscar(caracter)
                if(token.numero==p.LITERAL_CADENA):
                    procesar_cadena(fichero)
                elif(token.numero==p.LITERAL_NUM):
                    token.nombre_token=procesar_numerico(fichero)
                elif(token.numero==p.L_CORCHETE or token.numero == p.L_LLAVE):
                    tabs+=1
                elif(token.numero==p.R_CORCHETE or token.numero == p.R_LLAVE):
                    tabs-=1

            linea += token.nombre_token + ' '
            caracter = fichero.readline(1)

            # token = None
        except Exception as error:
            # linea += token.nombre_token + ' '
            retorno+=linea + '\n'
            # print(str(error)+">"+str(nro_linea)+"<")
            raise Exception(str(str(error)+">"+str(nro_linea)+"<"))
            # exit(-1)
    return retorno

def procesar_cadena(fichero):
    while (True):
        caracter = fichero.readline(1)
        if (caracter == '"'):
            return "STRING"
        if(caracter == EOF):
            raise Exception("Archivo terminado sin cerrar Cadena")


def procesar_numerico(fichero):
    while (True):
        caracter = fichero.readline(1)
        if ((caracter == '' or caracter == '\n' or caracter == ',') and (True)) : #agregar condicion para que siempre encuentre numeros, si encuentra algo extraño, devolver error
            temp='NUMBER' +(' COMA' if (caracter ==',') else '')
            return temp
            break
    pass


def procesar_booleano(fichero,caracter):
    lista = [['f','a','l','s','e'],['t','r','u','e']]
    booleano = caracter
    while (True) :
        caracter = fichero.readline(1)
        booleano += caracter
        if (caracter=='e' ):
            break

    if(booleano == 'false'):
        return 'false'
    if(booleano =='true'):
        return 'true'
    raise Exception ("Hubo un error, valor booleano mal escrito")

    pass

def escribir_linea(linea):
    with open(ARCHIVO_SALIDA,'a') as salida :
        salida.write(linea)
    salida.close()

def inicializar_archivo_salida():
    with open(ARCHIVO_SALIDA,'w') as salida :
        print("")
    salida.close()

# NOTE: Agregar excepcion para cuando se llega al final de la linea, y una cadena no se cierra
if (__name__ == '__main__') :
    main()
