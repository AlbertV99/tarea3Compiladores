import TablaSimbolos as ts
import Lexer as l

ARCHIVO_ENTRADA = 'fuente.txt'
ARCHIVO_SALIDA = 'salida.txt'

#CLASES PARA TRADUCCION
class ObjetoJson:
    def __init__(self):
        self.hijos = []

    def traducirXML(self):
        temp = ""
        for i in self.hijos:
            temp+= i.traducirXML()

        return temp

class Hijo:
    def __init__(self):
        self.clave = ""
        self.valor = None

    def traducirXML(self):
        temp = "<"+self.clave+">"+self.valor.traducirXML()+"</"+self.clave+">"
        return temp

class Valor:
    def __init__(self,valor=None):
        self.valor = valor

    def traducirXML(self):
        temp=""
        if(isinstance(self.valor,Vector)):
            temp = self.valor.traducirXML()
        else:
            temp = (self.valor if self.valor != None else " ")

        return temp

class Vector:
    def __init__(self):
        self.hijos=[]

    def traducirXML(self):
        temp = ""
        for i in self.hijos:
            temp += "<item>"+i.traducirXML()+"</item>"

        return temp

# CLASE PARSER
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
        self.analisisLexico()
        self.posicion_analisis=0
        self.resultado_sintactico = self.validarJson()

    def validarJson(self):
        # try:
        aux = self.validarElemento()
        if(self.posicion_analisis==len(self.resultado_lexico)):
            print("Analisis sintactico termino sin errores")
            return aux
        else:
            print("Ha ocurrido un error, Se esperaba un solo Elemento Json pero se obtuvo mas de uno")

        # except Exception as e:
        #     print(e)
        #     print("Error sintactico")


    def validarElemento(self):
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_LLAVE'):
            aux = self.validarObjeto()

        elif(self.resultado_lexico[self.posicion_analisis][0]=='L_CORCHETE'):
            aux = self.validarArray()

        else:
            raise Exception ('Se esperaba Inicio de Objeto o Array, caracter obtenido >'+self.resultado_lexico[self.posicion_analisis][1]+'<')

        return aux


    def validarObjeto(self):
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_LLAVE'):
            self.posicion_analisis+=1
            aux = ObjetoJson()
            if(self.resultado_lexico[self.posicion_analisis][0]=='R_LLAVE'):
                self.posicion_analisis+=1
                return aux
            else:
                hijos = self.validarListaAtributos()
                aux.hijos = hijos
                self.match('R_LLAVE')
                self.posicion_analisis+=1

        return aux


    def validarListaAtributos(self):
        aux = []
        while(True):
            hijo = Hijo()
            hijo.clave = self.validarClaveAtributo()
            self.match('DOS_PUNTOS')
            self.posicion_analisis+=1
            hijo.valor = self.validarValorAtributo()
            aux.append(hijo)

            if (self.resultado_lexico[self.posicion_analisis][0]=='COMA'):
                self.match('COMA')
                self.posicion_analisis+=1
                continue
            elif(self.resultado_lexico[self.posicion_analisis][0]=='R_LLAVE'):
                break
            else:
                print(self.posicion_analisis)
                raise Exception("Se esperaba Token >COMA< o >R_LLAVE< valor obtenido>"+self.resultado_lexico[self.posicion_analisis][1]+"<")
        return aux

    def validarClaveAtributo(self):
        self.match('LITERAL_CADENA')
        self.posicion_analisis+=1
        return self.resultado_lexico[self.posicion_analisis-1][1]

    def validarValorAtributo(self):
        valoresPosibiles=['PR_FALSE','PR_TRUE','LITERAL_NUM','LITERAL_CADENA']
        aux = None
        for temp in valoresPosibiles:
            if(self.resultado_lexico[self.posicion_analisis][0]==temp):
                self.match(temp)
                self.posicion_analisis+=1
                return Valor(('"'+self.resultado_lexico[self.posicion_analisis-1][1]+'"' if temp == 'LITERAL_CADENA' else self.resultado_lexico[self.posicion_analisis-1][1]))
        aux = self.validarElemento()
        return aux
        # self.posicion_analisis+=1

    def validarArray(self):
        aux = Vector()
        if(self.resultado_lexico[self.posicion_analisis][0]=='L_CORCHETE'):
            self.posicion_analisis+=1
            if(self.resultado_lexico[self.posicion_analisis][0]=='R_CORCHETE'):
                self.posicion_analisis+=1
                return aux
            else:
                hijos = self.validarListaElementos()
                self.match('R_CORCHETE')
                aux.hijos = hijos
                self.posicion_analisis+=1
        return aux

    def validarListaElementos(self):
        aux = []
        while(True):
            hijo = self.validarElemento()
            aux.append(hijo)
            if(self.resultado_lexico[self.posicion_analisis][0]=="COMA"):
                self.match("COMA")
                self.posicion_analisis+=1
                continue
            elif (self.resultado_lexico[self.posicion_analisis][0]=="R_CORCHETE"):
                break
        return aux

    def match(self,token_esperado):
        if( self.resultado_lexico[self.posicion_analisis][0]==token_esperado):
            return True
        else:
            raise Exception("Valor sintactico inesperado>"+self.resultado_lexico[self.posicion_analisis][1]+"<. Se esperaba >"+token_esperado+"< \n posicion Carrete" + str(self.posicion_analisis))
