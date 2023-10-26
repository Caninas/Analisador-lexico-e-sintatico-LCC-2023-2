# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934) 
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)


import re
import sys

class ErroLexico(Exception):
    def __init__(self, msg="erro não especificado", linha=None, coluna=None):
        self.msg = "Erro léxico: " + msg + f"(linha {linha}, coluna {coluna})"
        super().__init__(self.msg)


s = "def abc() {\n}"
if len(sys.argv) == 1:
    print("Forneca o path para o arquivo a ser lido")
    exit(0)
s = open(sys.argv[1], "r").read()

palavras_reservadas = {"def", "print", "for" "int", "float", "string"}
tabela_palavras_finais = {
    "int": "int_constant",
    "float": "float_constant",
    "string": "string_constant"
}

outros = [";", "{", "}", "+", "-", "/", "*", "<", ">", "=", "!", "[", "]", "%"]
texto_final = ""

# diagrama outro
def isOutro(caracter):
    return caracter in outros

i = 0
linha = 0
while i != len(s):
    caracter = s[i]
    palavra = ""

    # diagrama letra
    if caracter[i].isalpha():
        i += 1
        while caracter[i].isalnum():
            # palavra += caracter[i]
            i += 1
        if isOutro(caracter[i]) or caracter[i] in [" ", "\n"]:
            texto_final += "IDENT"
            continue

    # diagrama int/float
    elif caracter[i].isnumeric():
        i += 1
        while caracter[i].isnumeric():
            # palavra += caracter[i]
            i += 1
        if isOutro(caracter[i]):
            texto_final += tabela_palavras_finais["int"]
            continue
        elif caracter[i] == ".":
            i += 1
            while caracter[i].isnumeric():
                i += 1
            if isOutro(caracter[i]):
                texto_final += tabela_palavras_finais["float"]
                continue
        
        raise ErroLexico("", linha, i)

    # diagrama string
    elif caracter[i] == '"':

    elif caracter[i] in [" ", "\n"]:
        










# def substituir(matchobj):
    
    # if matchobj.group(0) in palavras_reservadas or re.match("\w+|\d", matchobj.group(0)):
        # return "IDENT"

    # elif s[matchobj.start(0)-1] in [" ", "\n"] and s[matchobj.end(0):matchobj.end(0)+1] == " ":
        # return "OUTRO"
    
    # elif s[matchobj.start(0)-1] == " " and s[matchobj.end(0):matchobj.end(0)+1] != " ":
        # return "OUTRO "
    
    # elif s[matchobj.end(0):matchobj.end(0)+1] == " " and s[matchobj.start(0)-1] != " ":
        # return " OUTRO"
    
    # else:
        # return " OUTRO "

# comp = re.compile("\w+|\S", re.MULTILINE)

# j = re.sub(comp, substituir, s)

# print(j)