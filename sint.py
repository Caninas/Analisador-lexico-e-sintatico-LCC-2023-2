import re
import pandas as pd
from pathlib import Path
from os import system, name
import os
from gerar_tabela import *

# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934)
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)
#------------------------------------
def ErroSintatico( fs, nt, te):

    print(f"\n----------------------Erro Sintatico-------------------------")
    print(f"forma sentencial:({fs})")
    print(f"nao-terminal mais a esquerda:({nt})")
    print(f"token de entrada:({te})")
    print("---------------------------------------------------------------")


def verificar_palavra(tokens, tabela,terminais, nao_terminais):
    sentenca = tokens

    pilha = [nao_terminais[0]]
    pilha.append('$')
    sentenca.append('$')
    top = pilha[0]
    fs = []
    resultado = []

    while True:
        if top == '$' and sentenca[0] == '$':
            resultado.append([str(pilha), str(sentenca), "Sentença OK"])
            return "String Aceita", resultado
        if not (top == sentenca[0]) and pilha[0] in terminais:
            resultado.append([str(pilha), str(sentenca), "ERRO - String Recusada"])
            try:
                nt = pilha[0]
                te = sentenca[0]
                sent = fs + pilha
                sent_completa = " ".join(sent)
                erro_info = (sent_completa, nt, te)
                return "ERRO - String Recusada", resultado, erro_info
            except Exception:
                return "ERRO - String Recusada", resultado
        if top == sentenca[0]:
            fs.append(pilha[0])
            resultado.append([str(pilha), str(sentenca), "Desempilha {}".format(pilha[0])])
            pilha.pop(0)
            sentenca.pop(0)
            top = pilha[0]
        if top in nao_terminais:
            ant_top = top
            consulta = tabela[(top, sentenca[0])]
            if consulta == '--':
                resultado.append([str(pilha), str(sentenca), "ERRO - String Recusada Pela Tabela"])
                nt = pilha[0]
                te = sentenca[0]
                sent = fs + pilha
                sent_completa = " ".join(sent)
                erro_info = (sent_completa, nt, te)
                return "ERRO - String Recusada Pela Tabela", resultado, erro_info
            else:
                resultado.append([str(pilha), str(sentenca), "{} -> {}".format(ant_top, consulta)])
                itens = consulta.split()
                pilha.pop(0)
                pilha = itens + pilha
                if pilha[0] == '\\epsilon':
                    pilha.pop(0)
                top = pilha[0]




def verificar_sentenca(tokens, tabela,  terminais, n_terminais):

            verificador = verificar_palavra(
                tokens, tabela, terminais, n_terminais)

            if len(verificador) == 3:
                string, pilha, erro_info = verificador

                col = "Pilha Entrada Ação".split()
                dados = pd.DataFrame(data=pilha, columns=col)

                print("\n")
                print(dados.set_index(['Pilha', 'Entrada']))
                print("\n")
                sent_completa, nt, te = erro_info
                ErroSintatico(sent_completa, nt, te)
            else:
                string, pilha = verificador

                col = "Pilha Entrada Ação".split()
                dados = pd.DataFrame(data=pilha, columns=col)

                print("\n")
                print(dados.set_index(['Pilha', 'Entrada']))
                print("\n")

def main(gramatica, tokens):

    if not os.path.exists('tabela.csv'):
       criar_tabela(gramatica)
    else:
        print("---- Tabelas ja geradas ----- ")
    df = pd.read_csv("tabela.csv", index_col=0)
    tabela = {(index, col): value for index, row in df.iterrows() for col, value in row.items()}
    terminais = df.columns.tolist()
    n_terminais = df.index.tolist()

    verificar_sentenca(tokens, tabela, terminais, n_terminais)

#main()