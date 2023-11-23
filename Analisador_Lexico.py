# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934) 
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)

import sys

class ErroLexico(Exception):
    def __init__(self, msg="erro não especificado", linha=None, coluna=None):
        self.msg = "Erro léxico: " + msg + f"(linha {linha}, coluna {coluna})"
        super().__init__(self.msg)


# if len(sys.argv) == 1:
#     print("Forneca o path para o arquivo a ser lido")
#     exit(0)
# sys.argv[1]

codigo_input = open("./exemplo1.lcc", "r").read()
# simbolo final
codigo_input += chr(3)

palavras_reservadas = {"def", "if", "else", "for", "break", "print", "read", 
                       "return", "new", "int", "float", "string", "null"}
simbolos_reservados = {";", "(", ")", "{", "}", "[", "]", "%", "+", "-", "*", 
                       "/", "<", ">", "=", "!"}
simbolos_n_unicos = {"=", "!", "<", ">",}

tabela_palavras_finais = {
    "int": "int_constant",
    "float": "float_constant",
    "string": "string_constant",
}

tabela_simbolos = dict()
lista_tokens = []

def isSimbUnico(caracter):
    return not caracter in simbolos_n_unicos 

def isSimbReservado(caracter):
    return caracter in simbolos_reservados

def isOutroUnico(caracter):
    return caracter in [";", "+", "-", "!", "%"]

def isEspaco(caracter):
    return caracter in [" ", "\n"]

def isReservado(palavra):
    return palavra in palavras_reservadas


i = 0
linha = 1
coluna = 1


while i < len(codigo_input):
    # diagrama letra
    if codigo_input[i].isalpha():
        i_inicial = i
        col_inicial = coluna
        i += 1
        coluna += 1

        while codigo_input[i].isalnum():
            i += 1
            coluna += 1

        if isSimbReservado(codigo_input[i]) or isEspaco(codigo_input[i]):
            palavra = codigo_input[i_inicial:i]

            if isReservado(palavra):
                lista_tokens.append(palavra)
            else:   
                lista_tokens.append("ident")
                try:
                    tabela_simbolos[palavra].append((linha, col_inicial))
                except:
                    tabela_simbolos[palavra] = [(linha, col_inicial)]
            continue

        raise ErroLexico("", linha, coluna)
    
    # diagrama int/float
    elif codigo_input[i].isnumeric():
        i += 1
        coluna += 1

        while codigo_input[i].isnumeric():
            i += 1
            coluna += 1

        if isSimbReservado(codigo_input[i]) or isEspaco(codigo_input[i]):
            lista_tokens.append(tabela_palavras_finais["int"])
            continue

        elif codigo_input[i] == ".":
            i += 1
            coluna += 1
            while codigo_input[i].isnumeric():
                i += 1
                coluna += 1
            if isSimbReservado(codigo_input[i]):
                lista_tokens.append(tabela_palavras_finais["float"])
                continue
        
        raise ErroLexico("", linha, coluna)

    # diagrama string
    elif codigo_input[i] in ['"', "'"]:
        i += 1
        coluna += 1
        while codigo_input[i].isalnum() or isSimbReservado(codigo_input[i]) or isEspaco(codigo_input[i]):
            i += 1
            coluna += 1

        if codigo_input[i] in ['"', "'"]:
            i += 1
            lista_tokens.append(tabela_palavras_finais["string"])
            continue

        raise ErroLexico("", linha, coluna)
    
    # diagrama simbolos
    elif isSimbReservado(codigo_input[i]):
        # if isSimbUnico(codigo_input[i]):
        lista_tokens.append(codigo_input[i])
        # else:
        #     if not parSimbValido(codigo_input[i], codigo_input[i+1]):
        #         raise ErroLexico()
        i += 1
        coluna += 1
        continue
    
    # diagrama espaço / quebra linha 
    elif isEspaco(codigo_input[i]):
        coluna += 1
        if codigo_input[i] == "\n":
            linha += 1
            coluna = 1

            #lista_tokens.append("\n")
        i += 1
        continue
    
    # fim
    elif codigo_input[i] == chr(3):
        break

    raise ErroLexico("Caracter nao reconhecido ", linha, coluna)


print(lista_tokens)
print(tabela_simbolos)