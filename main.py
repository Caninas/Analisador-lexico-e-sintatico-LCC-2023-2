import sys

from Analisador_Lexico import AnalisadorLexico
import sint

# if len(sys.argv) == 1:
#     print("Forneca o path para o arquivo a ser lido")
#     exit(0)
# sys.argv[1]

codigo_input = open("./exemplo1.lcc", "r", encoding="utf-8").read()
codigo_input += chr(3)


analisador_lexico = AnalisadorLexico(codigo_input)
lista_tokens, tabela_simbolos, error = analisador_lexico.analisar()
# print(lista_tokens)
# print(tabela_simbolos)
if (not error):
    sint.main("lcc-2023-2.txt", lista_tokens)