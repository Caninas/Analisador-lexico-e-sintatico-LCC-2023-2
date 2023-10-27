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


# if len(sys.argv) == 1:
#     print("Forneca o path para o arquivo a ser lido")
#     exit(0)
#sys.argv[1]
codigo_input = open("./exemplo1.lcc", "r").read()

palavras_reservadas = {"def", "print", "for" "int", "float", "string"}
tabela_palavras_finais = {
    "int": "int_constant",
    "float": "float_constant",
    "string": "string_constant"
}

outros = [";", "(", ")", "{", "}", "+", "-", "/", "*", "<", ">", "=", "!", "[", "]", "%", chr(3)]
texto_final = ""

# diagrama outro
def isOutro(caracter):
    return caracter in outros

i = 0
linha = 0

codigo_input += chr(3)

while i < len(codigo_input):
    #codigo_input[i] = s[i]

    # diagrama letra
    if codigo_input[i].isalpha():
        i += 1
        while codigo_input[i].isalnum():
            i += 1
        if isOutro(codigo_input[i]) or codigo_input[i] in [" ", "\n"]:
            texto_final += "IDENT"
            continue

        raise ErroLexico("", linha, i)
    # diagrama int/float
    elif codigo_input[i].isnumeric():
        i += 1
        while codigo_input[i].isnumeric():
            i += 1
        if isOutro(codigo_input[i]):
            texto_final += tabela_palavras_finais["int"]
            continue
        elif codigo_input[i] == ".":
            i += 1
            while codigo_input[i].isnumeric():
                i += 1
            if isOutro(codigo_input[i]):
                texto_final += tabela_palavras_finais["float"]
                continue
        
        raise ErroLexico("", linha, i)

    # diagrama string
    elif codigo_input[i] in ['"', "'"]:
        i += 1
        while codigo_input[i].isalnum() or isOutro(codigo_input[i]):
            i += 1

        if codigo_input[i] in ['"', "'"]:
            texto_final += tabela_palavras_finais["string"]
            continue

        raise ErroLexico("", linha, i)
    
    while isOutro(codigo_input[i]):
        i += 1
        texto_final += "OUTRO"
    
    while codigo_input[i] in [" ", "\n"]:
        if codigo_input[i] == "\n":
            linha += 1
            coluna = 0
        
        coluna += 1
        i += 1


print(texto_final)








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