import re

class Token :
    def __init__(self,token,patron,lexema):
        self.__token = token
        self.__lexema = lexema
        self.__patron = patron
        self.__patron_compilado = re.compile(self.__patron,re.M | re.I  )

    def validar(self, temp):
        # realizar la comparacion entre el temp y el patron (regex), se retornara verdadero o falso
        return self.__patron_compilado.fullmatch(str(temp))

    def obtenerToken(self):
        #retornara el token del objeto
        return self.__token


class TablaSimbolos:
    def __init__(self):
        self.tablaTokens = [
            Token('L_CORCHETE','\[','['),
            Token('R_CORCHETE','\]',']'),
            Token('L_LLAVE','\{','{'),
            Token('R_LLAVE','\}','}'),
            Token('COMA',',',','),
            Token('DOS_PUNTOS',':',':'),
            Token('LITERAL_NUM','[0-9]+(\.[0-9]+)?((e|E)(\+|-)?[0-9]+)?','number'),
            Token('PR_TRUE','(TRUE)','true'),
            Token('PR_FALSE','(FALSE)','false'),
            Token('PR_NULL','(NULL)','null'),
            Token('LITERAL_CADENA','.*','string'),
        ]
        self.terminales = [
            'L_CORCHETE',
            'R_CORCHETE',
            'L_LLAVE',
            'R_LLAVE',
            'COMA',
            'DOS_PUNTOS',
            ]


    def verificarToken(self,valor):
        for tokenTemp in self.tablaTokens:
            if(tokenTemp.validar(valor)):
                return (tokenTemp.obtenerToken(),valor)
            
        raise Exception("Caracter invalido encontrado <"+valor+">")
