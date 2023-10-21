# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934) 
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)


import re
import sys

s = "def abc() {\n}"
if len(sys.argv) == 1:
    print("Forneca o path para o arquivo a ser lido")
    exit(0)

s = open(sys.argv[1], "r").read()

palavras_reservadas = {"def", "print", "for" "int", "float", "string"}

def substituir(matchobj):
    if matchobj.group(0) in palavras_reservadas or re.match("\w+|\d", matchobj.group(0)):
        return "IDENT"

    elif s[matchobj.start(0)-1] in [" ", "\n"] and s[matchobj.end(0):matchobj.end(0)+1] == " ":
        return "OUTRO"
    
    elif s[matchobj.start(0)-1] == " " and s[matchobj.end(0):matchobj.end(0)+1] != " ":
        return "OUTRO "
    
    elif s[matchobj.end(0):matchobj.end(0)+1] == " " and s[matchobj.start(0)-1] != " ":
        return " OUTRO"
    
    else:
        return " OUTRO "

comp = re.compile("\w+|\S", re.MULTILINE)

j = re.sub(comp, substituir, s)

print(j)