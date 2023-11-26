import sys

from Analisador_Lexico import AnalisadorLexico
import sint

path = input("Forneca o path para o arquivo a ser lido: ")

# if len(sys.argv) == 1:
#     exit(0)
    
# path = sys.argv[1]

codigo_input = open(path, "r", encoding="utf-8").read()
codigo_input += chr(3)


analisador_lexico = AnalisadorLexico(codigo_input)
lista_tokens, tabela_simbolos, error = analisador_lexico.analisar()

if (not error):
    sint.main("lcc-2023-2.txt", lista_tokens)