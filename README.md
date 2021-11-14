# tarea3Compiladores
Traductor Json -> Xml

BNF Json

json → element eof 
element → object | array 
array -> [element - list] | []

element-list → element-list element | element 
object → [attribute-list } |{}

attributes list → atribute-list atribute | atribute

atribute → atribut-name : atribute-value 
atribute-name → string 
atribute-value → element | string | number | true | false | null

JSON traducido 

json.trad → element.trad eof 
element.trad → object.trad | array.trad 
array.trad → </atribuite-name.trad> element-list.trad </atribuite-name.trad>

element-list.trad → element-list.trad element.trad | element.trad

object.trad → <item> atribute-list.trad </item> | <item> </item>

atribute-list.trad → atribute-list.trad atribute.trad | atribute.trad

atribute.trad → <atribute-name.trad> atribute-value.trad </atribute-name.trad>

atribute-name.trad → string.sin-comillas 
atribute value → element | string.sin-comillas | number | true | false | null 




