import TablaSimbolos as ts
import Lexer as l

ARCHIVO_ENTRADA = 'fuente.txt'
ARCHIVO_SALIDA = 'salida.txt'

#
# class Objeto:
#
#
# class Vector:
#
#
# class Hijo:
#
#
# class Valor:

class Parser:
    def __init__(self,archivo_entrada=ARCHIVO_ENTRADA,archivo_salida=ARCHIVO_SALIDA):
        self.tabla = ts.TablaSimbolos()
        self.archivo_salida = archivo_salida
        self.archivo_entrada = archivo_entrada
        self.analizador_lexico = l.Lexer(self.archivo_entrada,self.archivo_salida)
        self.resultado_lexico = None
        self.lista_errores = []
        self.posicion_analisis=0
        self.resultado_sintactico = None

    def analisisLexico(self):
        try:
            self.resultado_lexico = self.analizador_lexico.procesar_fichero()
            self.posicion_analisis=0
        except Exception as e:
            print(e)
            print(self.analizador_lexico.lista_errores)
            self.posicion_analisis=0

    def analisisSintactico(self):
        self.posicion_analisis=0
        self.resultado_sintactico = self.validarJson()

    def validarJson(self):
        # try:
        self.validarElemento()
        if(self.posicion_analisis==len(self.resultado_lexico)):
            print("todo correcto")
        else:
            print("Ha ocurrido un error, Se esperaba un solo Elemento Json pero se obtuvo mas de uno")
        # except Exception as e:
        #     print(e)
        #     print("Error sintactico")


    def validarElemento(self):
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_LLAVE'):
            self.validarObjeto()

        elif(self.resultado_lexico[self.posicion_analisis][0]=='L_CORCHETE'):
            self.validarArray()
        else:
            raise Exception ('Se esperaba Inicio de Objeto o Array, caracter obtenido >'+self.resultado_lexico[self.posicion_analisis][1]+'<')

    def validarObjeto(self):
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_LLAVE'):
            self.posicion_analisis+=1
            if(self.resultado_lexico[self.posicion_analisis][0]=='R_LLAVE'):
                self.posicion_analisis+=1
                return
            else:
                hijos = self.validarListaAtributos()
                self.match('R_LLAVE')
                self.posicion_analisis+=1


    def validarListaAtributos(self):
        while(True):
            self.validarClaveAtributo()
            self.match('DOS_PUNTOS')
            self.posicion_analisis+=1
            self.validarValorAtributo()
            if (self.resultado_lexico[self.posicion_analisis][0]=='COMA'):
                self.match('COMA')
                self.posicion_analisis+=1
                continue
            elif(self.resultado_lexico[self.posicion_analisis][0]=='R_LLAVE'):
                break
            else:
                print(self.posicion_analisis)
                raise Exception("Se esperaba Token >COMA< o >R_LLAVE< valor obtenido>"+self.resultado_lexico[self.posicion_analisis][1]+"<")

    def validarClaveAtributo(self):
        self.match('LITERAL_CADENA')
        self.posicion_analisis+=1

    def validarValorAtributo(self):
        valoresPosibiles=['PR_FALSE','PR_TRUE','LITERAL_NUM','LITERAL_CADENA']
        for temp in valoresPosibiles:
            if(self.resultado_lexico[self.posicion_analisis][0]==temp):
                self.match(temp)
                self.posicion_analisis+=1
                return
        self.validarElemento()
        # self.posicion_analisis+=1

    def validarArray(self):
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_CORCHETE'):
            self.posicion_analisis+=1
            if(self.resultado_lexico[self.posicion_analisis][0]=='R_CORCHETE'):
                self.posicion_analisis+=1
                return
            else:
                hijos = self.validarListaElementos()
                self.match('R_CORCHETE')
                self.posicion_analisis+=1

    def validarListaElementos(self):
        while(True):
            self.validarElemento()
            if(self.resultado_lexico[self.posicion_analisis][0]=="COMA"):
                self.match("COMA")
                self.posicion_analisis+=1
                continue
            elif (self.resultado_lexico[self.posicion_analisis][0]=="R_CORCHETE"):
                break

    def match(self,token_esperado):
        if( self.resultado_lexico[self.posicion_analisis][0]==token_esperado):
            return True
        else:
            raise Exception("Valor sintactico inesperado>"+self.resultado_lexico[self.posicion_analisis][1]+"<. Se esperaba >"+token_esperado+"< \n posicion Carrete" + str(self.posicion_analisis))
