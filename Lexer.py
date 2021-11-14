import TablaSimbolos as t
EOF = ''

#VALORES CONSTANTES PARA CASOS EN DONDE NO SE PASE EL ARCHIVO DE ENTRADA O SALIDA UTILIZARA VALORES POR DEFECTO

ARCHIVO_ENTRADA = 'fuente.txt'
ARCHIVO_SALIDA = 'salida.txt'


class Lexer():
    def __init__(self,archivo_entrada=ARCHIVO_ENTRADA,archivo_salida=ARCHIVO_SALIDA):
        self.tabla = t.TablaSimbolos()
        self.archivo_salida = archivo_salida
        self.archivo_entrada = archivo_entrada
        self.lista_errores=[]
        self.lista_tokens=[]
        self.cadenaError=""
        self.inicializar_archivo_salida()

    def procesar_fichero(self):

        with open(self.archivo_entrada) as fichero:
            caracter = fichero.readline(1)
            tabs = 0
            aux_temp = None
            self.cadenaError = ""
            try:
                while (caracter != EOF) :
                    # print(caracter)
                    if(caracter == '\n' or caracter == ' ' or caracter == '\t'):
                        caracter = fichero.readline(1)
                        continue
                    else:
                        aux_temp = self.tabla.verificarToken(caracter)
                        # print (aux_temp[0]+" - "+aux_temp[1])
                        if (aux_temp[0] in self.tabla.terminales) :
                            self.actualizar_errores()
                            self.lista_tokens.append(aux_temp)
                        elif (caracter.lower() == 'f' or caracter.lower() == 't'):
                            self.actualizar_errores()
                            temp = self.procesar_booleano(fichero,caracter)
                            self.lista_tokens.append(temp)
                        elif (caracter.isnumeric()):
                            self.actualizar_errores()
                            temp = self.procesar_numerico(fichero,caracter)
                            self.lista_tokens.append(temp)
                            fichero.seek(fichero.tell()-1)
                        elif (caracter == '"'):
                            self.actualizar_errores()
                            temp = self.procesar_cadena(fichero,caracter)
                            self.lista_tokens.append(temp)
                        else:
                            self.cadenaError+=caracter

                        caracter = fichero.readline(1)


            except Exception as error:
                self.actualizar_errores()
                print("Errores encontrados")
                print(self.lista_errores)
                raise Exception(str(error))
                # exit(-1)

        fichero.close()
        return self.lista_tokens

    def actualizar_errores(self):
        if(self.cadenaError!=""):
            self.lista_errores.append(self.cadenaError)
            self.cadenaError=""

    def inicializar_archivo_salida(self):
        with open(self.archivo_salida,'w') as salida :
            print("")
        salida.close()

    def procesar_booleano(self,fichero,cadenaTemp):
        #avanzar en el buffer hasta completar todos los caracteres de true or false, y validar con el metodo de la tabla de simbolos
        caracter = fichero.readline(1)
        valoresCadena = ['t','r','u','e','f','a','l','s']
        while(caracter in valoresCadena) :
            cadenaTemp += caracter
            caracter = fichero.readline(1)

        return self.tabla.verificarToken(cadenaTemp)

    def procesar_cadena(self,fichero,cadenaTemp):
        #Avanzar en el buffer hasta encontrar una " como cierre y comparar con la tabla
        caracter = fichero.readline(1)
        cadenaTemp=""
        while(caracter !='"') :
            if(caracter == EOF):
                raise Exception("Archivo terminado sin cerrar Cadena")
            if(caracter == '\n'):
                caracter = fichero.readline(1)
            cadenaTemp += caracter
            caracter = fichero.readline(1)

        return self.tabla.verificarToken(cadenaTemp)

    def procesar_numerico(self,fichero,cadenaTemp):
        #avanzar en el buffer hasta encontrar un caracter que no coincida con la comparacion de la tabla de simbolos
        caracter = fichero.readline(1)
        while(self.tabla.verificarToken(cadenaTemp)[0] == 'LITERAL_NUM' and caracter !='\n') :
            cadenaTemp += caracter
            caracter = fichero.readline(1)


        cadenaTemp = cadenaTemp[:-1]
        return self.tabla.verificarToken(cadenaTemp)


def main():
    pass

if (__name__ == '__main__') :
    main()
