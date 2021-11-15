import Parser as P

def main():
    try:
        p = P.Parser()
        p.analisisLexico()
        p.analisisSintactico()
        print(p.resultado_sintactico.traducirXML())
    except Exception as e:
        print(e)


if (__name__ == '__main__') :
    main()
