# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934) 
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)

import sys

# class ErroLexico(Exception):
#     def __init__(self, char, linha=None, coluna=None, msg="erro não especificado"):
#         self.msg = f"Erro léxico (linha {linha}, coluna {coluna}): " + f"caractere '{char}' não reconhecido " #+ f"(linha {linha}, coluna {coluna})"
#         super().__init__(self.msg)

def ErroLexico( char, linha=None, coluna=None, msg="erro não especificado"):
    print(f"Erro léxico (linha {linha}, coluna {coluna}): " + f"caractere '{char}' não reconhecido")#+ f"(linha {linha}, coluna {coluna})"


# if len(sys.argv) == 1:
#     print("Forneca o path para o arquivo a ser lido")
#     exit(0)
# sys.argv[1]

codigo_input = open("./exemplo1.lcc", "r", encoding="utf-8").read()
# simbolo final
codigo_input += chr(3)

palavras_reservadas = {"def", "if", "else", "for", "break", "print", "read", 
                       "return", "new", "int", "float", "string", "null"}
simbolos_reservados = {";", "(", ")", "{", "}", "[", "]", "%", "+", "-", "*", 
                       "/", "<", ">", "=", "!", ","}
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

def isEspaco(caracter):
    return caracter in [" ", "\n"]

def isReservado(palavra):
    return palavra in palavras_reservadas

def parSimbValido(par_simbolos):
    return par_simbolos in ["<=", ">=", "==", "!="]


i = 0
linha = 1
coluna = 1


while i < len(codigo_input):
    # diagrama letra
    if codigo_input[i].isalpha() or codigo_input[i] == "_":
        i_inicial = i
        col_inicial = coluna
        i += 1
        coluna += 1

        while codigo_input[i].isalnum() or codigo_input[i] == "_":
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

        ErroLexico(codigo_input[i], linha, coluna)
        continue
    
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
        
        ErroLexico(codigo_input[i], linha, coluna)
        continue

    # diagrama string
    elif codigo_input[i] in ['"', "'"]:
        i += 1
        coluna += 1
        
        while codigo_input[i] not in ['"', "'"]:   #codigo_input[i].isalnum() or isSimbReservado(codigo_input[i]) or isEspaco(codigo_input[i] + codigo_input[i+1]):
            i += 1
            coluna += 1

        if codigo_input[i] in ['"', "'"]:
            i += 1
            coluna += 1
            lista_tokens.append(tabela_palavras_finais["string"])
            continue
        
        ErroLexico(codigo_input[i], linha, coluna)
        continue
    
    # diagrama simbolos
    elif isSimbReservado(codigo_input[i]):
        if not isSimbUnico(codigo_input[i]) and not isSimbUnico(codigo_input[i+1]):
            if parSimbValido(codigo_input[i] + codigo_input[i+1]):
                lista_tokens.append(codigo_input[i] + codigo_input[i+1])
                i += 2     
                coluna += 2
                continue
            else:
                ErroLexico(codigo_input[i] + codigo_input[i+1], linha, coluna)
                continue
        
        lista_tokens.append(codigo_input[i])
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

    ErroLexico(codigo_input[i], linha, coluna)
    i += 1


print(lista_tokens)
print(tabela_simbolos)