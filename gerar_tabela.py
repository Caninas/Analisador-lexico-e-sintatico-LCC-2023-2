import re
import pandas as pd
from pathlib import Path
from os import system, name
import os

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
        # first_set = set()
        # for ex in expression:
        #     first_set = first_set | first[ex]
        # print(first_set)
        first_set = first[nt]
        for element in (first_set - {'\\epsilon'}):
            #for symbol in expression:
                if element in first[expression[0]]:
                    table[nt, element] = (" ".join(expression)).strip()
        #for prod in expression:
        if '\\epsilon' in first[expression[0]]:
            for element in follow[nt]:
                table[nt, element] = expression[0]
        # if '\\epsilon' in first[nt] and '$' in follow[nt]:
        #     table[nt, '$'] = (" ".join(expression)).strip()
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

def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n

def criar_tabela(gramatica):
    gr = lerArquivo(gramatica)

    gramatica = Grammar(gr)
    terminais, nao_terminais, regras = gramatica.terminals, gramatica.nonterminals, gramatica.rules
    first, follow, epsilon = FirstAndFollow(terminais, nao_terminais, regras)
    tabela = LL1(first, follow, gramatica)

    df = pd.DataFrame()
    for (coluna, linha), valor in tabela.items():
        df.at[coluna, linha] = valor
    df.to_csv('tabela.csv')
    df.to_excel('tabela.xlsx')
    print("---- Tabela Gerada -----")

if __name__ == '__main__':
    criar_tabela('lcc-2023-2.txt')
