import sys

from Analisador_Lexico import AnalisadorLexico
import sint

path = input("Forneca o path para o arquivo a ser lido: ")

codigo_input = open(path, "r", encoding="utf-8").read()
codigo_input += chr(3)

# Analisador léxico
analisador_lexico = AnalisadorLexico(codigo_input)
lista_tokens, tabela_simbolos, error = analisador_lexico.analisar()

# Se nao tem erros lexicos: Analisador sintático
if (not error):
    sint.main("lcc-2023-2.txt", lista_tokens)