import re
import pandas as pd
from pathlib import Path
from os import system, name
import os

# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934)
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)
#------------------------------------
def ErroSintatico( fs, nt, te):
    # se houver erros sint´aticos → uma mensagem de insucesso indicando qual ´e a entrada
    # na tabela de reconhecimento sint´atico que est´a vazia (qual ´e a forma sentencial α,
    # qual ´e o s´ımbolo n˜ao-terminal mais `a esquerda de α e qual ´e o token da entrada).

    print(f"\n----------------------Erro Sintatico-------------------------")
    print(f"forma sentencial:({fs})")
    print(f"nao-terminal mais a esquerda:({nt})")
    print(f"token de entrada:({te})")
    print("---------------------------------------------------------------")

class Grammar:
    def __init__(self, rules):
        rules = tuple(rules)
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        temp_rule = [x.strip() for x in rule.split('->')]
        return tuple(temp_rule)

    @property
    def nonterminals(self):
        return set([nt for nt, _ in self.rules])

    @property
    def terminals(self):
        terminals = []
        nonterm = set([nt for nt, _ in self.rules])
        for _, expression in self.rules:
            prods = expression.split(" ")
            for prod in prods:
                if prod not in nonterm:
                    terminals.append(prod)
        return set(terminals)


def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def verificar_palavra(string, tabela, grammar):
    rule = [(i, j.split()) for i, j in grammar.rules]
    nao_terminais = list(grammar.nonterminals)
    terminais = list(grammar.terminals)
    sentenca = string.split()

    # if '^' in rule[0][0]:
    #     rule.pop(0)

    rule = tuple(rule)
    pilha = [rule[0][0]]
    pilha.append('$')
    sentenca.append('$')
    top = pilha[0]
    fs = []
    resultado = []
    #TODO ADICIONAR MSG DE ERRO ErroSintatico(fs, nt, te) fs= forma sentencial α,
    # nt= Nao-terminal mais a esquerda de α, te= token de entrada, ------  entrada
    # na tabela de reconhecimento sint´atico que est´a vazia

    while True:
        if top == '$' and sentenca[0] == '$':
            resultado.append([str(pilha), str(sentenca), "Sentença OK"])
            return "String Aceita", resultado
        if not (top == sentenca[0]) and pilha[0] in terminais:
            resultado.append([str(pilha), str(sentenca), "String Recusada"])
            return "String Recusada - Linguagem com erro?", resultado
            #TODO MELHORAR ERRO
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
                ErroSintatico(sent_completa, nt, te)
                return "ERRO - String Recusada Pela Tabela", resultado
            else:
                #fs.append(["{} -> {}".format(ant_top, consulta)])
                resultado.append([str(pilha), str(sentenca), "{} -> {}".format(ant_top, consulta)])
                itens = consulta.split()
                pilha.pop(0)
                pilha = itens + pilha
                if pilha[0] == '\\epsilon':
                    pilha.pop(0)
                top = pilha[0]


def LL1(first, follow, grammar):
    lista = sorted(
        (list(grammar.terminals) + list(grammar.nonterminals)), key=len, reverse=True)
    rule = [(i, j.split()) for i, j in grammar.rules]
    terminais = grammar.terminals - {'\\epsilon'}
    if not ('^' in rule[0][0]):
        valor = rule[0][0] + '$'
        rule.insert(0, ('^', valor))
        lista = list(lista) + list('$') + list('^')
        terminais |= {'$'}
    if '^' in rule[0][0]:
        rule.pop(0)
    rule = tuple(rule)
    terminais = sorted(terminais, key=len, reverse=True)

    table = {}
    for nt, expression in rule:
        for element in list(terminais):
            table[nt, element] = '--'
    for nt, expression in rule:
        first_set = first[nt]
        for element in (first_set - {'\\epsilon'}):
            #for symbol in expression:
                if element in first[expression[0]]:
                    if nt == "STATEMENT": print(nt, element, expression)
                    table[nt, element] = (" ".join(expression)).strip()
        if '\\epsilon' in first_set:
            for element in follow[nt]:
                table[nt, element] = "".join(expression)
        if '\\epsilon' in first[nt] and '$' in follow[nt]:
            table[nt, '$'] = "".join(expression)
    return table

def FirstAndFollow(terminais, nao_terminais, regras):

    rule = [(i , j.split()) for i, j in regras]

    valor = [rule[0][0], '$']
    rule.insert(0, ('^', valor))

    terminais |= {'$'}
    nao_terminais |= {'^'}
    rule = tuple(i for i in rule)
    first = {i: set() for i in nao_terminais}
    first.update((i, {i}) for i in terminais)
    follow = {i: set() for i in nao_terminais}
    epsilon = {'\\epsilon'}
    # epsilon = {'\\epsilon'}

    while True:
        updated = False
        for nt, expression in rule:
            for symbol in expression:
                updated |= union(first[nt], first[symbol])
                if symbol not in epsilon:
                    break
                else:
                    updated |= union(epsilon, {nt})
            aux = follow[nt]
            for symbol in reversed(expression):
                if symbol in follow:
                    updated |= union(follow[symbol], aux)
                if symbol in epsilon:
                    aux = aux.union(first[symbol])
                else:
                    aux = first[symbol]

        if not updated:
            for chave, valor in follow.items():
                if '\\epsilon' in follow[chave]:
                    follow[chave] = follow[chave] - {'\\epsilon'}
            cond1 = False
            cond2 = False
            for i in epsilon:
                if '^' in i:
                    cond1 = True
                if '\\epsilon' in i:
                    cond2 = True

            for i in nao_terminais:
                if '^' in i:
                    first.pop(i)
                    follow.pop(i)
                if cond1 and '^' in i:
                    epsilon.remove(i)

            for i in terminais:
                # first.pop(i)
                first['$'] = '$'
                if cond2 and '\\epsilon' in i:
                    epsilon.remove(i)
            for i in {'$'}:
                first.pop(i)

            return first, follow, epsilon

def tratarArq(lista):
    lista = " ".join(lista.split())
    lista = re.split(r' ', lista)
    return lista

def lerArquivo(dir):
    arquivo = []
    b = []
    inicio = ""
    fim = ""

    with open(dir, "r") as gramatica:
        for line in gramatica:
            arquivo.append(line.strip().split('\n'))
    arquivo = [i for j in arquivo for i in j]
    arquivo[0] = arquivo[0].replace('ï»¿', "")
    gramatica = []
    for i in range(0, len(arquivo)):
        temp = []
        temp = tratarArq(arquivo[i])
        prod_splited = arquivo[i].split('|')
        prod_splited[0] = re.sub(r'.*->', '', prod_splited[0])
        prod_splited = [x.strip() for x in prod_splited]
        for prod in prod_splited:
            gramatica.append(f"{temp[0]} {temp[1]} " + prod)

    return gramatica


def printArquivo(dir):
    with open(dir, "r", encoding="utf-8") as file:
        for line in file:
            print(line)
def salvar_tabela(tabela):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    tabela.to_excel(outpath+'/Tabela.xls')
def tr_terminais(terminais):
    return [i for j in [list(i) for i in terminais] for i in j]
def salvar_verificador(resultado):
    outpath = 'output'
    Path(outpath).mkdir(exist_ok=True)
    colunas = "Pilha Entrada Acão".split()
    dados = pd.DataFrame(data=resultado, columns=colunas)
    dados.to_excel(outpath+"/Verificador.xls")

def verificar_sentenca(tabela, gramatica):

            verificador = verificar_palavra(
                input("Escreva uma sentença: "), tabela, gramatica)

            if type(verificador) == tuple:
                string, pilha = verificador

                col = "Pilha Entrada Ação".split()
                dados = pd.DataFrame(data=pilha, columns=col)

                print("\n")
                print(dados.set_index(['Pilha', 'Entrada']))
                print("\n")

def main():

    gramatica = 'lcc-2023-2.txt'
    #gramatica_teste = "grammar/a.txt"

    gr = lerArquivo(gramatica)

    # visualizar_grammar(gr)

    gramatica = Grammar(gr)

    terminais, nao_terminais, regras = gramatica.terminals, gramatica.nonterminals, gramatica.rules

    first, follow, epsilon = FirstAndFollow(terminais, nao_terminais, regras)

    tabela = LL1(first, follow, gramatica)

    df = pd.DataFrame()

    for (coluna, linha), valor in tabela.items():
        df.at[coluna, linha] = valor
    if not os.path.exists('tabela.csv'):
        df.to_csv('tabela.csv')
    if not os.path.exists('tabela.xlsx'):
        df.to_excel('tabela.xlsx')


    verificar_sentenca(tabela, gramatica)

main()