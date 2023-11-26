import sys

from Analisador_Lexico import AnalisadorLexico
from Analisador_Sintatico import AnalisadorSintatico

path = input("Forneca o path para o arquivo a ser lido: ")

codigo_input = open(path, "r", encoding="utf-8").read()
codigo_input += chr(3)

#Analisador sintático
analisador_sintatico = AnalisadorSintatico()

# Analisador léxico
analisador_lexico = AnalisadorLexico(codigo_input)

lista_tokens, tabela_simbolos, error = analisador_lexico.analisar()

# Se nao tem erros lexicos:
if (not error):
    analisador_sintatico.analisar("lcc-2023-2.txt", lista_tokens)