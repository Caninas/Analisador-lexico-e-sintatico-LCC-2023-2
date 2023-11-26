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


def verificar_palavra(tokens, tabela, grammar):
    rule = [(i, j.split()) for i, j in grammar.rules]
    nao_terminais = list(grammar.nonterminals)
    terminais = list(grammar.terminals)
    sentenca = tokens

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
            resultado.append([str(pilha), str(sentenca), "ERRO - String Recusada"])
            try:
                nt = pilha[0]
                te = sentenca[0]
                sent = fs + pilha
                sent_completa = " ".join(sent)
                ErroSintatico(sent_completa, nt, te)
            except Exception:
                pass
            return "ERRO - String Recusada", resultado
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

def verificar_sentenca(tokens, tabela, gramatica):

            verificador = verificar_palavra(
                tokens, tabela, gramatica)

            if type(verificador) == tuple:
                string, pilha = verificador

                col = "Pilha Entrada Ação".split()
                dados = pd.DataFrame(data=pilha, columns=col)

                print("\n")
                print(dados.set_index(['Pilha', 'Entrada']))
                print("\n")

def main(gramatica, tokens):

    #gramatica = 'lcc-2023-2.txt'
    #gramatica_teste = "grammar/a.txt"

    gr = lerArquivo(gramatica)

    # visualizar_grammar(gr)

    gramatica = Grammar(gr)

    terminais, nao_terminais, regras = gramatica.terminals, gramatica.nonterminals, gramatica.rules

    first, follow, epsilon = FirstAndFollow(terminais, nao_terminais, regras)

    tabela = {('PROGRAM', 'string_constant'): '--', ('PROGRAM', 'float_constant'): '--', ('PROGRAM', 'int_constant'): '--', ('PROGRAM', 'return'): 'STATEMENT', ('PROGRAM', 'ident('): '--', ('PROGRAM', 'ident,'): '--', ('PROGRAM', 'string'): 'STATEMENT', ('PROGRAM', 'print'): 'STATEMENT', ('PROGRAM', 'float'): 'STATEMENT', ('PROGRAM', 'break'): 'STATEMENT', ('PROGRAM', 'ident'): 'STATEMENT', ('PROGRAM', 'else'): '--', ('PROGRAM', 'null'): '--', ('PROGRAM', 'read'): 'STATEMENT', ('PROGRAM', 'for'): 'STATEMENT', ('PROGRAM', 'def'): 'FUNCLIST', ('PROGRAM', 'int'): 'STATEMENT', ('PROGRAM', 'new'): '--', ('PROGRAM', '!='): '--', ('PROGRAM', '>='): '--', ('PROGRAM', 'if'): 'STATEMENT', ('PROGRAM', '=='): '--', ('PROGRAM', '<='): '--', ('PROGRAM', '{'): 'STATEMENT', ('PROGRAM', '%'): '--', ('PROGRAM', ';'): 'STATEMENT', ('PROGRAM', '/'): '--', ('PROGRAM', '('): '--', ('PROGRAM', '='): '--', ('PROGRAM', '$'): '\\epsilon', ('PROGRAM', '['): '--', ('PROGRAM', '-'): '--', ('PROGRAM', '}'): '--', ('PROGRAM', '>'): '--', ('PROGRAM', ')'): '--', ('PROGRAM', '<'): '--', ('PROGRAM', ']'): '--', ('PROGRAM', '*'): '--', ('PROGRAM', '+'): '--', ('FUNCLIST', 'string_constant'): '--', ('FUNCLIST', 'float_constant'): '--', ('FUNCLIST', 'int_constant'): '--', ('FUNCLIST', 'return'): '--', ('FUNCLIST', 'ident('): '--', ('FUNCLIST', 'ident,'): '--', ('FUNCLIST', 'string'): '--', ('FUNCLIST', 'print'): '--', ('FUNCLIST', 'float'): '--', ('FUNCLIST', 'break'): '--', ('FUNCLIST', 'ident'): '--', ('FUNCLIST', 'else'): '--', ('FUNCLIST', 'null'): '--', ('FUNCLIST', 'read'): '--', ('FUNCLIST', 'for'): '--', ('FUNCLIST', 'def'): 'FUNCDEF F`', ('FUNCLIST', 'int'): '--', ('FUNCLIST', 'new'): '--', ('FUNCLIST', '!='): '--', ('FUNCLIST', '>='): '--', ('FUNCLIST', 'if'): '--', ('FUNCLIST', '=='): '--', ('FUNCLIST', '<='): '--', ('FUNCLIST', '{'): '--', ('FUNCLIST', '%'): '--', ('FUNCLIST', ';'): '--', ('FUNCLIST', '/'): '--', ('FUNCLIST', '('): '--', ('FUNCLIST', '='): 
                '--', ('FUNCLIST', '$'): '--', ('FUNCLIST', '['): '--', ('FUNCLIST', '-'): '--', ('FUNCLIST', '}'): '--', ('FUNCLIST', '>'): '--', ('FUNCLIST', ')'): '--', ('FUNCLIST', '<'): '--', ('FUNCLIST', ']'): '--', ('FUNCLIST', '*'): '--', ('FUNCLIST', '+'): '--', ('F`', 'string_constant'): '--', ('F`', 'float_constant'): '--', ('F`', 'int_constant'): '--', ('F`', 'return'): '--', ('F`', 'ident('): '--', ('F`', 'ident,'): '--', ('F`', 'string'): '--', ('F`', 'print'): '--', ('F`', 'float'): '--', ('F`', 'break'): '--', ('F`', 'ident'): '--', ('F`', 'else'): '--', ('F`', 'null'): '--', ('F`', 'read'): '--', ('F`', 'for'): '--', ('F`', 'def'): 'FUNCLIST', ('F`', 'int'): '--', ('F`', 'new'): '--', ('F`', '!='): '--', ('F`', '>='): '--', ('F`', 'if'): '--', ('F`', '=='): '--', ('F`', '<='): '--', ('F`', '{'): '--', ('F`', '%'): '--', ('F`', ';'): '--', ('F`', '/'): '--', ('F`', '('): '--', ('F`', '='): '--', ('F`', '$'): '\\epsilon', ('F`', '['): '--', ('F`', '-'): '--', ('F`', '}'): '--', ('F`', '>'): '--', ('F`', ')'): '--', ('F`', '<'): '--', ('F`', ']'): '--', ('F`', '*'): '--', ('F`', '+'): '--', ('FUNCDEF', 'string_constant'): '--', ('FUNCDEF', 'float_constant'): '--', ('FUNCDEF', 'int_constant'): '--', ('FUNCDEF', 'return'): '--', ('FUNCDEF', 'ident('): '--', ('FUNCDEF', 'ident,'): '--', ('FUNCDEF', 'string'): '--', ('FUNCDEF', 'print'): '--', ('FUNCDEF', 'float'): '--', ('FUNCDEF', 'break'): '--', ('FUNCDEF', 'ident'): '--', ('FUNCDEF', 'else'): '--', ('FUNCDEF', 'null'): '--', ('FUNCDEF', 'read'): '--', ('FUNCDEF', 'for'): '--', ('FUNCDEF', 'def'): 'def ident( PARAMLIST ) { STATELIST }', ('FUNCDEF', 'int'): '--', ('FUNCDEF', 'new'): '--', ('FUNCDEF', '!='): '--', ('FUNCDEF', '>='): '--', ('FUNCDEF', 'if'): '--', ('FUNCDEF', '=='): '--', ('FUNCDEF', '<='): '--', ('FUNCDEF', '{'): '--', ('FUNCDEF', '%'): '--', ('FUNCDEF', ';'): '--', ('FUNCDEF', '/'): '--', ('FUNCDEF', '('): '--', ('FUNCDEF', '='): '--', ('FUNCDEF', '$'): '--', ('FUNCDEF', '['): '--', ('FUNCDEF', '-'): '--', ('FUNCDEF', '}'): '--', ('FUNCDEF', '>'): '--', ('FUNCDEF', ')'): '--', ('FUNCDEF', '<'): '--', ('FUNCDEF', ']'): '--', ('FUNCDEF', '*'): '--', ('FUNCDEF', '+'): '--', ('PARAMLIST', 'string_constant'): '--', ('PARAMLIST', 'float_constant'): '--', ('PARAMLIST', 'int_constant'): '--', ('PARAMLIST', 'return'): '--', ('PARAMLIST', 'ident('): '--', ('PARAMLIST', 'ident,'): '--', ('PARAMLIST', 'string'): 'string G`', ('PARAMLIST', 'print'): '--', ('PARAMLIST', 'float'): 'float G`', ('PARAMLIST', 'break'): '--', ('PARAMLIST', 'ident'): '--', ('PARAMLIST', 'else'): '--', ('PARAMLIST', 'null'): '--', ('PARAMLIST', 'read'): '--', ('PARAMLIST', 'for'): '--', ('PARAMLIST', 'def'): '--', ('PARAMLIST', 'int'): 'int G`', ('PARAMLIST', 'new'): '--', ('PARAMLIST', '!='): '--', ('PARAMLIST', '>='): '--', ('PARAMLIST', 'if'): '--', ('PARAMLIST', '=='): '--', ('PARAMLIST', '<='): '--', ('PARAMLIST', '{'): '--', ('PARAMLIST', '%'): '--', ('PARAMLIST', ';'): '--', ('PARAMLIST', '/'): '--', ('PARAMLIST', '('): '--', ('PARAMLIST', '='): '--', ('PARAMLIST', '$'): '--', ('PARAMLIST', '['): '--', ('PARAMLIST', '-'): '--', ('PARAMLIST', '}'): '--', ('PARAMLIST', '>'): '--', ('PARAMLIST', ')'): '\\epsilon', ('PARAMLIST', '<'): '--', ('PARAMLIST', ']'): '--', ('PARAMLIST', '*'): '--', ('PARAMLIST', '+'): '--', ('G`', 'string_constant'): '--', ('G`', 'float_constant'): '--', ('G`', 'int_constant'): '--', ('G`', 'return'): '--', ('G`', 'ident('): '--', ('G`', 'ident,'): 'ident, PARAMLIST', ('G`', 'string'): '--', ('G`', 'print'): '--', ('G`', 'float'): '--', ('G`', 'break'): '--', ('G`', 'ident'): 'ident', ('G`', 'else'): '--', ('G`', 'null'): '--', ('G`', 'read'): '--', ('G`', 'for'): '--', ('G`', 'def'): '--', ('G`', 'int'): '--', ('G`', 'new'): '--', ('G`', '!='): '--', ('G`', '>='): '--', ('G`', 'if'): '--', ('G`', '=='): '--', ('G`', '<='): '--', ('G`', '{'): '--', ('G`', '%'): '--', ('G`', ';'): '--', ('G`', '/'): '--', ('G`', '('): '--', ('G`', '='): '--', ('G`', '$'): '--', ('G`', '['): '--', ('G`', '-'): '--', ('G`', '}'): '--', ('G`', '>'): '--', ('G`', ')'): '\\epsilon', ('G`', '<'): '--', ('G`', ']'): '--', ('G`', '*'): '--', ('G`', '+'): '--', ('STATEMENT', 'string_constant'): '--', ('STATEMENT', 'float_constant'): '--', ('STATEMENT', 'int_constant'): '--', ('STATEMENT', 'return'): 'RETURNSTAT ;', ('STATEMENT', 'ident('): '--', ('STATEMENT', 'ident,'): '--', ('STATEMENT', 'string'): 'VARDECL ;', ('STATEMENT', 'print'): 'PRINTSTAT ;', ('STATEMENT', 'float'): 'VARDECL ;', ('STATEMENT', 'break'): 'break ;', ('STATEMENT', 'ident'): 'ATRIBSTAT ;', ('STATEMENT', 'else'): '--', ('STATEMENT', 'null'): '--', ('STATEMENT', 'read'): 'READSTAT ;', ('STATEMENT', 'for'): 'FORSTAT', ('STATEMENT', 'def'): '--', ('STATEMENT', 'int'): 'VARDECL ;', ('STATEMENT', 'new'): '--', ('STATEMENT', '!='): '--', ('STATEMENT', '>='): '--', ('STATEMENT', 'if'): 'IFSTAT', ('STATEMENT', '=='): '--', ('STATEMENT', '<='): '--', ('STATEMENT', '{'): '{ STATELIST }', ('STATEMENT', '%'): '--', ('STATEMENT', ';'): ';', ('STATEMENT', '/'): '--', ('STATEMENT', '('): '--', ('STATEMENT', '='): '--', ('STATEMENT', '$'): '--', ('STATEMENT', '['): '--', ('STATEMENT', '-'): '--', ('STATEMENT', '}'): '--', ('STATEMENT', '>'): '--', ('STATEMENT', ')'): '--', ('STATEMENT', '<'): '--', ('STATEMENT', ']'): '--', ('STATEMENT', '*'): '--', ('STATEMENT', '+'): '--', ('VARDECL', 'string_constant'): '--', ('VARDECL', 'float_constant'): '--', ('VARDECL', 'int_constant'): '--', ('VARDECL', 'return'): '--', ('VARDECL', 'ident('): '--', ('VARDECL', 'ident,'): '--', ('VARDECL', 'string'): 'string ident E`', ('VARDECL', 'print'): '--', ('VARDECL', 'float'): 'float ident E`', ('VARDECL', 'break'): '--', ('VARDECL', 'ident'): '--', ('VARDECL', 'else'): '--', ('VARDECL', 'null'): '--', ('VARDECL', 'read'): '--', ('VARDECL', 'for'): '--', ('VARDECL', 'def'): '--', ('VARDECL', 'int'): 'int ident E`', ('VARDECL', 'new'): '--', ('VARDECL', '!='): '--', ('VARDECL', '>='): '--', ('VARDECL', 'if'): '--', ('VARDECL', '=='): '--', ('VARDECL', '<='): '--', ('VARDECL', '{'): '--', ('VARDECL', '%'): '--', ('VARDECL', ';'): '--', ('VARDECL', '/'): '--', ('VARDECL', '('): '--', ('VARDECL', '='): '--', ('VARDECL', '$'): '--', ('VARDECL', '['): '--', ('VARDECL', '-'): '--', ('VARDECL', '}'): '--', ('VARDECL', '>'): '--', ('VARDECL', ')'): '--', ('VARDECL', '<'): '--', ('VARDECL', ']'): '--', ('VARDECL', '*'): '--', ('VARDECL', '+'): '--', ('E`', 'string_constant'): '--', ('E`', 'float_constant'): '--', ('E`', 'int_constant'): '--', ('E`', 'return'): '--', ('E`', 'ident('): '--', ('E`', 'ident,'): '--', ('E`', 'string'): '--', ('E`', 'print'): '--', ('E`', 'float'): '--', ('E`', 'break'): '--', ('E`', 'ident'): '--', ('E`', 'else'): '--', ('E`', 'null'): '--', ('E`', 'read'): '--', ('E`', 'for'): '--', ('E`', 'def'): '--', ('E`', 'int'): '--', ('E`', 'new'): '--', ('E`', '!='): '--', ('E`', '>='): '--', ('E`', 'if'): '--', ('E`', '=='): '--', ('E`', '<='): '--', ('E`', '{'): '--', ('E`', '%'): '--', ('E`', ';'): '\\epsilon', ('E`', '/'): '--', ('E`', '('): '--', ('E`', '='): '--', ('E`', '$'): '--', ('E`', '['): '[ int_constant ] E`', ('E`', '-'): '--', ('E`', '}'): '--', ('E`', '>'): '--', ('E`', ')'): '--', ('E`', '<'): '--', ('E`', ']'): '--', ('E`', '*'): '--', ('E`', '+'): '--', ('ATRIBSTAT', 'string_constant'): '--', ('ATRIBSTAT', 'float_constant'): '--', ('ATRIBSTAT', 'int_constant'): '--', ('ATRIBSTAT', 'return'): '--', ('ATRIBSTAT', 'ident('): '--', ('ATRIBSTAT', 'ident,'): '--', ('ATRIBSTAT', 'string'): '--', ('ATRIBSTAT', 'print'): '--', ('ATRIBSTAT', 'float'): '--', ('ATRIBSTAT', 'break'): '--', ('ATRIBSTAT', 'ident'): 'LVALUE = H`', ('ATRIBSTAT', 'else'): '--', ('ATRIBSTAT', 'null'): '--', ('ATRIBSTAT', 'read'): '--', ('ATRIBSTAT', 'for'): '--', ('ATRIBSTAT', 'def'): '--', ('ATRIBSTAT', 
                'int'): '--', ('ATRIBSTAT', 'new'): '--', ('ATRIBSTAT', '!='): '--', ('ATRIBSTAT', '>='): '--', ('ATRIBSTAT', 'if'): '--', ('ATRIBSTAT', '=='): '--', ('ATRIBSTAT', '<='): '--', ('ATRIBSTAT', '{'): '--', ('ATRIBSTAT', '%'): '--', ('ATRIBSTAT', ';'): '--', ('ATRIBSTAT', '/'): '--', ('ATRIBSTAT', '('): '--', ('ATRIBSTAT', '='): '--', ('ATRIBSTAT', '$'): '--', ('ATRIBSTAT', '['): '--', ('ATRIBSTAT', '-'): '--', ('ATRIBSTAT', '}'): '--', ('ATRIBSTAT', '>'): '--', ('ATRIBSTAT', ')'): '--', ('ATRIBSTAT', '<'): '--', ('ATRIBSTAT', ']'): '--', ('ATRIBSTAT', '*'): '--', ('ATRIBSTAT', '+'): '--', ('H`', 'string_constant'): 'EXPRESSION', ('H`', 'float_constant'): 'EXPRESSION', ('H`', 'int_constant'): 'EXPRESSION', ('H`', 'return'): '--', ('H`', 'ident('): 'FUNCCALL', ('H`', 'ident,'): '--', ('H`', 'string'): '--', ('H`', 'print'): '--', 
                ('H`', 'float'): '--', ('H`', 'break'): '--', ('H`', 'ident'): 'EXPRESSION', ('H`', 'else'): '--', ('H`', 'null'): 'EXPRESSION', ('H`', 'read'): '--', ('H`', 'for'): '--', ('H`', 'def'): '--', ('H`', 'int'): '--', ('H`', 'new'): 'ALLOCEXPRESSION', ('H`', '!='): '--', ('H`', '>='): '--', ('H`', 'if'): '--', ('H`', '=='): '--', ('H`', '<='): '--', ('H`', '{'): '--', ('H`', '%'): '--', ('H`', ';'): '--', ('H`', '/'): '--', ('H`', '('): 'EXPRESSION', ('H`', '='): '--', ('H`', '$'): '--', ('H`', '['): '--', ('H`', '-'): 'EXPRESSION', ('H`', '}'): '--', ('H`', '>'): '--', ('H`', ')'): '--', ('H`', '<'): '--', ('H`', ']'): '--', ('H`', '*'): '--', ('H`', '+'): 'EXPRESSION', ('FUNCCALL', 'string_constant'): '--', ('FUNCCALL', 'float_constant'): '--', ('FUNCCALL', 'int_constant'): '--', ('FUNCCALL', 'return'): '--', ('FUNCCALL', 'ident('): 'ident( PARAMLISTCALL )', ('FUNCCALL', 'ident,'): '--', ('FUNCCALL', 'string'): '--', ('FUNCCALL', 'print'): '--', ('FUNCCALL', 'float'): '--', ('FUNCCALL', 'break'): '--', ('FUNCCALL', 'ident'): '--', ('FUNCCALL', 'else'): '--', ('FUNCCALL', 'null'): '--', ('FUNCCALL', 'read'): '--', ('FUNCCALL', 'for'): '--', ('FUNCCALL', 'def'): '--', ('FUNCCALL', 'int'): '--', ('FUNCCALL', 'new'): '--', ('FUNCCALL', '!='): '--', ('FUNCCALL', '>='): '--', ('FUNCCALL', 'if'): '--', ('FUNCCALL', '=='): '--', ('FUNCCALL', '<='): '--', ('FUNCCALL', '{'): '--', ('FUNCCALL', '%'): '--', ('FUNCCALL', ';'): '--', ('FUNCCALL', '/'): '--', ('FUNCCALL', '('): '--', ('FUNCCALL', '='): '--', ('FUNCCALL', '$'): '--', ('FUNCCALL', '['): '--', ('FUNCCALL', '-'): '--', ('FUNCCALL', '}'): '--', ('FUNCCALL', '>'): '--', ('FUNCCALL', ')'): '--', ('FUNCCALL', '<'): '--', ('FUNCCALL', ']'): '--', ('FUNCCALL', '*'): '--', ('FUNCCALL', '+'): '--', ('PARAMLISTCALL', 'string_constant'): '--', ('PARAMLISTCALL', 'float_constant'): '--', ('PARAMLISTCALL', 'int_constant'): '--', ('PARAMLISTCALL', 'return'): '--', ('PARAMLISTCALL', 'ident('): '--', ('PARAMLISTCALL', 'ident,'): 'I`', ('PARAMLISTCALL', 'string'): '--', ('PARAMLISTCALL', 'print'): '--', ('PARAMLISTCALL', 'float'): '--', ('PARAMLISTCALL', 'break'): '--', ('PARAMLISTCALL', 'ident'): 'I`', ('PARAMLISTCALL', 'else'): '--', ('PARAMLISTCALL', 'null'): '--', ('PARAMLISTCALL', 'read'): '--', ('PARAMLISTCALL', 'for'): '--', ('PARAMLISTCALL', 'def'): '--', ('PARAMLISTCALL', 'int'): '--', ('PARAMLISTCALL', 'new'): '--', ('PARAMLISTCALL', '!='): '--', ('PARAMLISTCALL', '>='): '--', ('PARAMLISTCALL', 'if'): '--', ('PARAMLISTCALL', '=='): '--', ('PARAMLISTCALL', '<='): '--', ('PARAMLISTCALL', '{'): '--', ('PARAMLISTCALL', '%'): '--', ('PARAMLISTCALL', ';'): '--', ('PARAMLISTCALL', '/'): '--', ('PARAMLISTCALL', '('): '--', ('PARAMLISTCALL', '='): '--', ('PARAMLISTCALL', '$'): '--', ('PARAMLISTCALL', '['): '--', ('PARAMLISTCALL', '-'): '--', ('PARAMLISTCALL', '}'): '--', ('PARAMLISTCALL', '>'): '--', ('PARAMLISTCALL', ')'): '\\epsilon', ('PARAMLISTCALL', '<'): '--', ('PARAMLISTCALL', ']'): '--', ('PARAMLISTCALL', '*'): '--', ('PARAMLISTCALL', '+'): '--', ('I`', 'string_constant'): '--', ('I`', 'float_constant'): '--', ('I`', 'int_constant'): '--', ('I`', 'return'): '--', ('I`', 'ident('): '--', ('I`', 'ident,'): 'ident, PARAMLISTCALL', ('I`', 'string'): '--', ('I`', 'print'): '--', ('I`', 'float'): '--', ('I`', 'break'): '--', ('I`', 'ident'): 'ident', ('I`', 'else'): '--', ('I`', 'null'): '--', ('I`', 'read'): '--', ('I`', 'for'): '--', ('I`', 'def'): '--', ('I`', 'int'): '--', ('I`', 'new'): '--', ('I`', '!='): '--', ('I`', '>='): '--', ('I`', 'if'): '--', ('I`', '=='): '--', ('I`', '<='): '--', ('I`', '{'): '--', ('I`', '%'): '--', ('I`', ';'): '--', ('I`', '/'): '--', ('I`', '('): '--', ('I`', '='): '--', ('I`', '$'): '--', ('I`', '['): '--', ('I`', '-'): '--', ('I`', '}'): '--', ('I`', '>'): '--', ('I`', ')'): '\\epsilon', ('I`', '<'): '--', ('I`', ']'): '--', ('I`', '*'): '--', ('I`', '+'): '--', ('PRINTSTAT', 'string_constant'): '--', ('PRINTSTAT', 'float_constant'): '--', ('PRINTSTAT', 'int_constant'): '--', ('PRINTSTAT', 'return'): '--', ('PRINTSTAT', 'ident('): '--', ('PRINTSTAT', 'ident,'): '--', ('PRINTSTAT', 'string'): '--', ('PRINTSTAT', 'print'): 'print EXPRESSION', ('PRINTSTAT', 'float'): '--', ('PRINTSTAT', 'break'): '--', ('PRINTSTAT', 'ident'): '--', ('PRINTSTAT', 'else'): '--', ('PRINTSTAT', 'null'): '--', ('PRINTSTAT', 'read'): '--', ('PRINTSTAT', 'for'): '--', ('PRINTSTAT', 'def'): '--', ('PRINTSTAT', 'int'): '--', ('PRINTSTAT', 
                'new'): '--', ('PRINTSTAT', '!='): '--', ('PRINTSTAT', '>='): '--', ('PRINTSTAT', 'if'): '--', ('PRINTSTAT', '=='): '--', ('PRINTSTAT', '<='): '--', ('PRINTSTAT', '{'): '--', ('PRINTSTAT', '%'): '--', ('PRINTSTAT', ';'): '--', ('PRINTSTAT', '/'): '--', ('PRINTSTAT', '('): '--', 
                ('PRINTSTAT', '='): '--', ('PRINTSTAT', '$'): '--', ('PRINTSTAT', '['): '--', ('PRINTSTAT', '-'): '--', ('PRINTSTAT', '}'): '--', ('PRINTSTAT', '>'): '--', ('PRINTSTAT', ')'): '--', ('PRINTSTAT', '<'): '--', ('PRINTSTAT', ']'): '--', ('PRINTSTAT', '*'): '--', ('PRINTSTAT', '+'): '--', ('READSTAT', 'string_constant'): '--', ('READSTAT', 'float_constant'): '--', ('READSTAT', 'int_constant'): '--', ('READSTAT', 'return'): '--', ('READSTAT', 'ident('): '--', ('READSTAT', 'ident,'): '--', ('READSTAT', 'string'): '--', ('READSTAT', 'print'): '--', ('READSTAT', 'float'): '--', ('READSTAT', 'break'): '--', ('READSTAT', 'ident'): '--', ('READSTAT', 'else'): '--', ('READSTAT', 'null'): '--', ('READSTAT', 'read'): 'read LVALUE', ('READSTAT', 'for'): '--', ('READSTAT', 'def'): '--', ('READSTAT', 'int'): '--', ('READSTAT', 'new'): '--', ('READSTAT', '!='): '--', ('READSTAT', '>='): '--', ('READSTAT', 'if'): '--', ('READSTAT', '=='): '--', ('READSTAT', '<='): '--', ('READSTAT', '{'): '--', ('READSTAT', '%'): '--', ('READSTAT', ';'): '--', ('READSTAT', '/'): '--', ('READSTAT', '('): '--', ('READSTAT', '='): '--', 
                ('READSTAT', '$'): '--', ('READSTAT', '['): '--', ('READSTAT', '-'): '--', ('READSTAT', '}'): '--', ('READSTAT', '>'): '--', ('READSTAT', ')'): '--', ('READSTAT', '<'): '--', ('READSTAT', ']'): '--', ('READSTAT', '*'): '--', ('READSTAT', '+'): '--', ('RETURNSTAT', 'string_constant'): '--', ('RETURNSTAT', 'float_constant'): '--', ('RETURNSTAT', 'int_constant'): '--', ('RETURNSTAT', 'return'): 'return', ('RETURNSTAT', 'ident('): '--', ('RETURNSTAT', 'ident,'): '--', ('RETURNSTAT', 'string'): '--', ('RETURNSTAT', 'print'): '--', ('RETURNSTAT', 'float'): '--', ('RETURNSTAT', 'break'): '--', ('RETURNSTAT', 'ident'): '--', ('RETURNSTAT', 'else'): '--', ('RETURNSTAT', 'null'): '--', ('RETURNSTAT', 'read'): '--', ('RETURNSTAT', 'for'): '--', ('RETURNSTAT', 'def'): '--', ('RETURNSTAT', 'int'): '--', ('RETURNSTAT', 'new'): '--', ('RETURNSTAT', '!='): '--', ('RETURNSTAT', '>='): '--', ('RETURNSTAT', 'if'): '--', ('RETURNSTAT', '=='): '--', ('RETURNSTAT', '<='): '--', ('RETURNSTAT', '{'): '--', ('RETURNSTAT', '%'): '--', ('RETURNSTAT', ';'): '--', ('RETURNSTAT', '/'): '--', ('RETURNSTAT', '('): '--', ('RETURNSTAT', '='): '--', ('RETURNSTAT', '$'): '--', ('RETURNSTAT', '['): '--', ('RETURNSTAT', '-'): '--', ('RETURNSTAT', '}'): '--', ('RETURNSTAT', '>'): '--', ('RETURNSTAT', ')'): '--', ('RETURNSTAT', '<'): '--', ('RETURNSTAT', ']'): '--', ('RETURNSTAT', '*'): '--', ('RETURNSTAT', '+'): '--', ('IFSTAT', 'string_constant'): '--', ('IFSTAT', 'float_constant'): '--', ('IFSTAT', 'int_constant'): '--', ('IFSTAT', 'return'): '--', ('IFSTAT', 'ident('): '--', ('IFSTAT', 'ident,'): '--', ('IFSTAT', 'string'): '--', ('IFSTAT', 'print'): '--', ('IFSTAT', 'float'): '--', ('IFSTAT', 'break'): '--', ('IFSTAT', 'ident'): '--', ('IFSTAT', 'else'): '--', ('IFSTAT', 'null'): '--', ('IFSTAT', 'read'): '--', ('IFSTAT', 'for'): '--', ('IFSTAT', 'def'): '--', ('IFSTAT', 'int'): '--', ('IFSTAT', 'new'): '--', ('IFSTAT', '!='): '--', ('IFSTAT', '>='): '--', ('IFSTAT', 'if'): 'if ( EXPRESSION ) STATEMENT J`', ('IFSTAT', '=='): '--', ('IFSTAT', '<='): '--', ('IFSTAT', '{'): '--', ('IFSTAT', '%'): '--', ('IFSTAT', ';'): '--', ('IFSTAT', '/'): '--', ('IFSTAT', '('): '--', ('IFSTAT', '='): '--', ('IFSTAT', '$'): '--', ('IFSTAT', '['): '--', ('IFSTAT', '-'): '--', ('IFSTAT', '}'): '--', ('IFSTAT', '>'): '--', ('IFSTAT', ')'): '--', ('IFSTAT', '<'): '--', ('IFSTAT', ']'): '--', ('IFSTAT', '*'): '--', ('IFSTAT', '+'): '--', ('J`', 'string_constant'): '--', ('J`', 'float_constant'): '--', ('J`', 'int_constant'): '--', ('J`', 'return'): '\\epsilon', ('J`', 'ident('): '--', ('J`', 'ident,'): '--', ('J`', 'string'): '\\epsilon', ('J`', 'print'): '\\epsilon', ('J`', 'float'): '\\epsilon', ('J`', 'break'): '\\epsilon', ('J`', 'ident'): '\\epsilon', ('J`', 'else'): 'else STATEMENT', ('J`', 
                'null'): '--', ('J`', 'read'): '\\epsilon', ('J`', 'for'): '\\epsilon', ('J`', 'def'): '--', ('J`', 'int'): '\\epsilon', ('J`', 'new'): '--', ('J`', '!='): '--', ('J`', '>='): '--', ('J`', 'if'): '\\epsilon', ('J`', '=='): '--', ('J`', '<='): '--', ('J`', '{'): '\\epsilon', ('J`', '%'): '--', ('J`', ';'): '\\epsilon', ('J`', '/'): '--', ('J`', '('): '--', ('J`', '='): '--', ('J`', '$'): '\\epsilon', ('J`', '['): '--', ('J`', '-'): '--', ('J`', '}'): '\\epsilon', ('J`', '>'): '--', ('J`', ')'): '--', ('J`', '<'): '--', ('J`', ']'): '--', ('J`', '*'): '--', ('J`', '+'): '--', ('FORSTAT', 'string_constant'): '--', ('FORSTAT', 'float_constant'): '--', ('FORSTAT', 'int_constant'): '--', ('FORSTAT', 'return'): '--', ('FORSTAT', 'ident('): '--', ('FORSTAT', 'ident,'): '--', ('FORSTAT', 'string'): '--', ('FORSTAT', 'print'): '--', ('FORSTAT', 'float'): '--', ('FORSTAT', 'break'): '--', ('FORSTAT', 'ident'): '--', ('FORSTAT', 'else'): '--', ('FORSTAT', 'null'): '--', ('FORSTAT', 'read'): '--', ('FORSTAT', 'for'): 'for ( ATRIBSTAT ; EXPRESSION ; ATRIBSTAT ) STATEMENT', ('FORSTAT', 'def'): '--', ('FORSTAT', 'int'): '--', ('FORSTAT', 'new'): '--', ('FORSTAT', '!='): '--', ('FORSTAT', '>='): '--', ('FORSTAT', 'if'): '--', ('FORSTAT', '=='): '--', ('FORSTAT', '<='): '--', ('FORSTAT', '{'): '--', ('FORSTAT', '%'): '--', ('FORSTAT', ';'): '--', ('FORSTAT', '/'): '--', ('FORSTAT', '('): '--', ('FORSTAT', '='): '--', ('FORSTAT', '$'): '--', ('FORSTAT', '['): '--', ('FORSTAT', '-'): '--', ('FORSTAT', '}'): '--', ('FORSTAT', '>'): '--', ('FORSTAT', ')'): '--', ('FORSTAT', '<'): '--', ('FORSTAT', ']'): '--', ('FORSTAT', '*'): '--', ('FORSTAT', '+'): '--', ('STATELIST', 'string_constant'): '--', ('STATELIST', 'float_constant'): '--', ('STATELIST', 'int_constant'): '--', ('STATELIST', 'return'): 'STATEMENT K`', ('STATELIST', 'ident('): '--', ('STATELIST', 'ident,'): '--', ('STATELIST', 'string'): 'STATEMENT K`', ('STATELIST', 'print'): 'STATEMENT K`', ('STATELIST', 'float'): 'STATEMENT K`', ('STATELIST', 'break'): 'STATEMENT K`', ('STATELIST', 'ident'): 'STATEMENT K`', ('STATELIST', 'else'): '--', ('STATELIST', 'null'): '--', ('STATELIST', 'read'): 'STATEMENT K`', ('STATELIST', 'for'): 'STATEMENT K`', ('STATELIST', 
                'def'): '--', ('STATELIST', 'int'): 'STATEMENT K`', ('STATELIST', 'new'): '--', ('STATELIST', '!='): '--', ('STATELIST', '>='): '--', ('STATELIST', 'if'): 'STATEMENT K`', ('STATELIST', '=='): '--', ('STATELIST', '<='): '--', ('STATELIST', '{'): 'STATEMENT K`', ('STATELIST', '%'): '--', ('STATELIST', ';'): 'STATEMENT K`', ('STATELIST', '/'): '--', ('STATELIST', '('): '--', ('STATELIST', '='): '--', ('STATELIST', '$'): '--', ('STATELIST', '['): '--', ('STATELIST', '-'): '--', ('STATELIST', '}'): '--', ('STATELIST', '>'): '--', ('STATELIST', ')'): '--', ('STATELIST', '<'): '--', ('STATELIST', ']'): '--', ('STATELIST', '*'): '--', ('STATELIST', '+'): '--', ('K`', 'string_constant'): '--', ('K`', 'float_constant'): '--', ('K`', 'int_constant'): '--', ('K`', 'return'): 'STATELIST', ('K`', 'ident('): '--', ('K`', 'ident,'): '--', ('K`', 'string'): 'STATELIST', ('K`', 'print'): 'STATELIST', ('K`', 'float'): 'STATELIST', ('K`', 'break'): 'STATELIST', ('K`', 'ident'): 'STATELIST', ('K`', 'else'): '--', ('K`', 'null'): '--', ('K`', 'read'): 'STATELIST', ('K`', 'for'): 'STATELIST', ('K`', 'def'): '--', ('K`', 'int'): 'STATELIST', ('K`', 'new'): '--', ('K`', '!='): '--', ('K`', '>='): '--', ('K`', 'if'): 'STATELIST', ('K`', '=='): '--', ('K`', '<='): '--', ('K`', '{'): 'STATELIST', ('K`', '%'): '--', ('K`', ';'): 'STATELIST', ('K`', '/'): '--', ('K`', '('): '--', ('K`', '='): '--', ('K`', '$'): '--', ('K`', '['): '--', ('K`', '-'): '--', ('K`', '}'): '\\epsilon', ('K`', '>'): '--', ('K`', ')'): '--', ('K`', '<'): '--', ('K`', ']'): '--', ('K`', '*'): '--', ('K`', '+'): '--', ('ALLOCEXPRESSION', 'string_constant'): '--', ('ALLOCEXPRESSION', 'float_constant'): 
                '--', ('ALLOCEXPRESSION', 'int_constant'): '--', ('ALLOCEXPRESSION', 'return'): '--', ('ALLOCEXPRESSION', 'ident('): '--', ('ALLOCEXPRESSION', 'ident,'): '--', ('ALLOCEXPRESSION', 'string'): '--', ('ALLOCEXPRESSION', 'print'): '--', ('ALLOCEXPRESSION', 'float'): '--', ('ALLOCEXPRESSION', 'break'): '--', ('ALLOCEXPRESSION', 'ident'): '--', ('ALLOCEXPRESSION', 'else'): '--', ('ALLOCEXPRESSION', 'null'): '--', ('ALLOCEXPRESSION', 'read'): '--', ('ALLOCEXPRESSION', 'for'): '--', ('ALLOCEXPRESSION', 'def'): '--', ('ALLOCEXPRESSION', 'int'): '--', ('ALLOCEXPRESSION', 'new'): 'new D`', ('ALLOCEXPRESSION', '!='): '--', ('ALLOCEXPRESSION', '>='): '--', ('ALLOCEXPRESSION', 'if'): '--', ('ALLOCEXPRESSION', '=='): '--', ('ALLOCEXPRESSION', '<='): '--', ('ALLOCEXPRESSION', '{'): '--', ('ALLOCEXPRESSION', '%'): '--', ('ALLOCEXPRESSION', ';'): '--', ('ALLOCEXPRESSION', '/'): '--', ('ALLOCEXPRESSION', '('): '--', ('ALLOCEXPRESSION', '='): '--', ('ALLOCEXPRESSION', '$'): '--', ('ALLOCEXPRESSION', '['): '--', ('ALLOCEXPRESSION', '-'): '--', ('ALLOCEXPRESSION', '}'): '--', ('ALLOCEXPRESSION', '>'): '--', ('ALLOCEXPRESSION', ')'): '--', ('ALLOCEXPRESSION', '<'): '--', ('ALLOCEXPRESSION', ']'): '--', ('ALLOCEXPRESSION', '*'): '--', ('ALLOCEXPRESSION', '+'): '--', ('D`', 'string_constant'): '--', ('D`', 'float_constant'): '--', ('D`', 'int_constant'): '--', ('D`', 'return'): '--', ('D`', 'ident('): '--', ('D`', 'ident,'): '--', ('D`', 'string'): 'string [ NUMEXPRESSION ] Z', ('D`', 'print'): '--', ('D`', 'float'): 'float [ NUMEXPRESSION ] Z', ('D`', 'break'): '--', ('D`', 'ident'): '--', ('D`', 'else'): '--', ('D`', 'null'): '--', ('D`', 'read'): '--', ('D`', 'for'): 
                '--', ('D`', 'def'): '--', ('D`', 'int'): 'int [ NUMEXPRESSION ] Z', ('D`', 'new'): '--', ('D`', '!='): '--', ('D`', '>='): '--', ('D`', 'if'): '--', ('D`', '=='): '--', ('D`', '<='): '--', ('D`', '{'): '--', ('D`', '%'): '--', ('D`', ';'): '--', ('D`', '/'): '--', ('D`', '('): 
                '--', ('D`', '='): '--', ('D`', '$'): '--', ('D`', '['): '--', ('D`', '-'): '--', ('D`', '}'): '--', ('D`', '>'): '--', ('D`', ')'): '--', ('D`', '<'): '--', ('D`', ']'): '--', ('D`', '*'): '--', ('D`', '+'): '--', ('Z', 'string_constant'): '--', ('Z', 'float_constant'): '--', ('Z', 'int_constant'): '--', ('Z', 'return'): '--', ('Z', 'ident('): '--', ('Z', 'ident,'): '--', ('Z', 'string'): '--', ('Z', 'print'): '--', ('Z', 'float'): '--', ('Z', 'break'): '--', ('Z', 'ident'): '--', ('Z', 'else'): '--', ('Z', 'null'): '--', ('Z', 'read'): '--', ('Z', 'for'): '--', ('Z', 'def'): '--', ('Z', 'int'): '--', ('Z', 'new'): '--', ('Z', '!='): '--', ('Z', '>='): '--', ('Z', 'if'): '--', ('Z', '=='): '--', ('Z', '<='): '--', ('Z', '{'): '--', ('Z', '%'): '--', ('Z', ';'): '\\epsilon', ('Z', '/'): '--', ('Z', '('): '--', ('Z', '='): '--', ('Z', '$'): '--', ('Z', '['): '[ NUMEXPRESSION ] Z', ('Z', '-'): '--', ('Z', '}'): '--', ('Z', '>'): '--', ('Z', ')'): '\\epsilon', ('Z', '<'): '--', ('Z', ']'): '--', ('Z', '*'): '--', ('Z', '+'): '--', ('EXPRESSION', 'string_constant'): 'NUMEXPRESSION L`', ('EXPRESSION', 'float_constant'): 'NUMEXPRESSION L`', ('EXPRESSION', 'int_constant'): 'NUMEXPRESSION L`', ('EXPRESSION', 'return'): '--', ('EXPRESSION', 'ident('): '--', ('EXPRESSION', 'ident,'): '--', ('EXPRESSION', 'string'): '--', ('EXPRESSION', 'print'): '--', ('EXPRESSION', 'float'): '--', 
                ('EXPRESSION', 'break'): '--', ('EXPRESSION', 'ident'): 'NUMEXPRESSION L`', ('EXPRESSION', 'else'): '--', ('EXPRESSION', 'null'): 'NUMEXPRESSION L`', ('EXPRESSION', 'read'): '--', ('EXPRESSION', 'for'): '--', ('EXPRESSION', 'def'): '--', ('EXPRESSION', 'int'): '--', ('EXPRESSION', 'new'): '--', ('EXPRESSION', '!='): '--', ('EXPRESSION', '>='): '--', ('EXPRESSION', 'if'): '--', ('EXPRESSION', '=='): '--', ('EXPRESSION', '<='): '--', ('EXPRESSION', '{'): '--', ('EXPRESSION', '%'): '--', ('EXPRESSION', ';'): '--', ('EXPRESSION', '/'): '--', ('EXPRESSION', '('): 'NUMEXPRESSION L`', ('EXPRESSION', '='): '--', ('EXPRESSION', '$'): '--', ('EXPRESSION', '['): '--', ('EXPRESSION', '-'): 'NUMEXPRESSION L`', ('EXPRESSION', '}'): '--', ('EXPRESSION', '>'): '--', ('EXPRESSION', ')'): '--', ('EXPRESSION', '<'): '--', ('EXPRESSION', ']'): '--', ('EXPRESSION', '*'): '--', ('EXPRESSION', '+'): 'NUMEXPRESSION L`', ('L`', 'string_constant'): '--', ('L`', 'float_constant'): '--', ('L`', 'int_constant'): '--', ('L`', 'return'): '--', ('L`', 'ident('): '--', ('L`', 'ident,'): '--', ('L`', 'string'): '--', ('L`', 'print'): '--', ('L`', 'float'): '--', ('L`', 'break'): '--', ('L`', 'ident'): '--', ('L`', 'else'): '--', ('L`', 'null'): '--', ('L`', 'read'): '--', ('L`', 'for'): '--', ('L`', 'def'): '--', ('L`', 'int'): '--', ('L`', 'new'): '--', ('L`', '!='): '!= NUMEXPRESSION', ('L`', '>='): '>= NUMEXPRESSION', ('L`', 'if'): '--', ('L`', '=='): '== NUMEXPRESSION', ('L`', '<='): '<= NUMEXPRESSION', ('L`', '{'): '--', ('L`', '%'): '--', ('L`', ';'): '\\epsilon', ('L`', '/'): '--', ('L`', '('): '--', ('L`', '='): '--', ('L`', '$'): '--', ('L`', '['): '--', ('L`', '-'): '--', ('L`', '}'): '--', ('L`', '>'): '> NUMEXPRESSION', ('L`', ')'): '\\epsilon', ('L`', '<'): '< NUMEXPRESSION', ('L`', ']'): '--', ('L`', '*'): '--', ('L`', '+'): '--', ('NUMEXPRESSION', 'string_constant'): 'TERM A`', ('NUMEXPRESSION', 'float_constant'): 'TERM A`', ('NUMEXPRESSION', 'int_constant'): 'TERM A`', ('NUMEXPRESSION', 'return'): '--', ('NUMEXPRESSION', 'ident('): '--', ('NUMEXPRESSION', 'ident,'): '--', ('NUMEXPRESSION', 'string'): '--', ('NUMEXPRESSION', 'print'): '--', ('NUMEXPRESSION', 'float'): '--', ('NUMEXPRESSION', 'break'): '--', ('NUMEXPRESSION', 'ident'): 'TERM A`', ('NUMEXPRESSION', 'else'): '--', ('NUMEXPRESSION', 'null'): 'TERM A`', ('NUMEXPRESSION', 'read'): '--', ('NUMEXPRESSION', 'for'): '--', ('NUMEXPRESSION', 'def'): '--', ('NUMEXPRESSION', 'int'): '--', ('NUMEXPRESSION', 'new'): '--', ('NUMEXPRESSION', '!='): '--', ('NUMEXPRESSION', '>='): '--', ('NUMEXPRESSION', 'if'): '--', ('NUMEXPRESSION', '=='): '--', ('NUMEXPRESSION', '<='): '--', ('NUMEXPRESSION', '{'): '--', ('NUMEXPRESSION', '%'): '--', ('NUMEXPRESSION', ';'): '--', ('NUMEXPRESSION', '/'): '--', ('NUMEXPRESSION', '('): 'TERM A`', ('NUMEXPRESSION', '='): '--', ('NUMEXPRESSION', '$'): '--', ('NUMEXPRESSION', '['): '--', ('NUMEXPRESSION', '-'): 'TERM A`', ('NUMEXPRESSION', '}'): '--', ('NUMEXPRESSION', '>'): '--', ('NUMEXPRESSION', ')'): '--', ('NUMEXPRESSION', '<'): '--', ('NUMEXPRESSION', ']'): '--', ('NUMEXPRESSION', '*'): '--', ('NUMEXPRESSION', '+'): 'TERM A`', ('A`', 'string_constant'): '--', ('A`', 'float_constant'): '--', ('A`', 'int_constant'): '--', ('A`', 'return'): '--', ('A`', 'ident('): '--', ('A`', 'ident,'): '--', ('A`', 'string'): '--', ('A`', 'print'): '--', ('A`', 'float'): '--', ('A`', 'break'): '--', ('A`', 'ident'): '--', ('A`', 'else'): '--', ('A`', 'null'): '--', ('A`', 'read'): '--', ('A`', 'for'): '--', ('A`', 'def'): '--', ('A`', 'int'): '--', ('A`', 'new'): '--', ('A`', '!='): '\\epsilon', ('A`', '>='): '\\epsilon', ('A`', 'if'): '--', ('A`', '=='): '\\epsilon', ('A`', '<='): '\\epsilon', ('A`', '{'): '--', ('A`', '%'): '--', ('A`', ';'): '\\epsilon', ('A`', '/'): '--', ('A`', '('): '--', ('A`', '='): '--', ('A`', '$'): '--', ('A`', '['): '--', ('A`', '-'): '- TERM A`', ('A`', '}'): '--', ('A`', '>'): '\\epsilon', ('A`', ')'): '\\epsilon', ('A`', '<'): '\\epsilon', ('A`', ']'): '\\epsilon', ('A`', '*'): '--', ('A`', '+'): '+ TERM A`', ('TERM', 'string_constant'): 'UNARYEXPR C`', ('TERM', 'float_constant'): 'UNARYEXPR C`', ('TERM', 'int_constant'): 'UNARYEXPR C`', ('TERM', 'return'): '--', ('TERM', 'ident('): '--', ('TERM', 'ident,'): '--', ('TERM', 'string'): '--', ('TERM', 'print'): '--', ('TERM', 'float'): '--', ('TERM', 'break'): '--', ('TERM', 'ident'): 'UNARYEXPR C`', ('TERM', 'else'): '--', ('TERM', 'null'): 'UNARYEXPR C`', ('TERM', 'read'): '--', ('TERM', 'for'): '--', ('TERM', 'def'): '--', ('TERM', 'int'): '--', ('TERM', 'new'): '--', ('TERM', '!='): '--', ('TERM', '>='): '--', ('TERM', 'if'): '--', ('TERM', '=='): '--', ('TERM', '<='): '--', ('TERM', '{'): '--', ('TERM', '%'): '--', ('TERM', 
                ';'): '--', ('TERM', '/'): '--', ('TERM', '('): 'UNARYEXPR C`', ('TERM', '='): '--', ('TERM', '$'): '--', ('TERM', '['): '--', ('TERM', '-'): 'UNARYEXPR C`', ('TERM', '}'): '--', ('TERM', '>'): '--', ('TERM', ')'): '--', ('TERM', '<'): '--', ('TERM', ']'): '--', ('TERM', '*'): '--', ('TERM', '+'): 'UNARYEXPR C`', ('C`', 'string_constant'): '--', ('C`', 'float_constant'): '--', ('C`', 'int_constant'): '--', ('C`', 'return'): '--', ('C`', 'ident('): '--', ('C`', 'ident,'): '--', ('C`', 'string'): '--', ('C`', 'print'): '--', ('C`', 'float'): '--', ('C`', 'break'): '--', ('C`', 'ident'): '--', ('C`', 'else'): '--', ('C`', 'null'): '--', ('C`', 'read'): '--', ('C`', 'for'): '--', ('C`', 'def'): '--', ('C`', 'int'): '--', ('C`', 'new'): '--', ('C`', '!='): '\\epsilon', ('C`', '>='): '\\epsilon', ('C`', 'if'): '--', ('C`', '=='): '\\epsilon', ('C`', '<='): '\\epsilon', ('C`', '{'): '--', ('C`', '%'): '% UNARYEXPR C`', ('C`', ';'): '\\epsilon', ('C`', '/'): '/ UNARYEXPR C`', ('C`', '('): '--', ('C`', '='): '--', ('C`', '$'): '--', ('C`', '['): '--', ('C`', '-'): '\\epsilon', ('C`', '}'): '--', ('C`', '>'): '\\epsilon', ('C`', ')'): '\\epsilon', ('C`', '<'): '\\epsilon', ('C`', ']'): '\\epsilon', ('C`', '*'): '* UNARYEXPR C`', ('C`', '+'): '\\epsilon', ('UNARYEXPR', 'string_constant'): 'FACTOR', ('UNARYEXPR', 'float_constant'): 'FACTOR', ('UNARYEXPR', 'int_constant'): 'FACTOR', ('UNARYEXPR', 'return'): '--', ('UNARYEXPR', 'ident('): '--', ('UNARYEXPR', 'ident,'): '--', ('UNARYEXPR', 'string'): '--', ('UNARYEXPR', 'print'): '--', ('UNARYEXPR', 'float'): '--', ('UNARYEXPR', 'break'): '--', ('UNARYEXPR', 'ident'): 'FACTOR', ('UNARYEXPR', 'else'): '--', ('UNARYEXPR', 'null'): 'FACTOR', ('UNARYEXPR', 'read'): '--', ('UNARYEXPR', 'for'): '--', ('UNARYEXPR', 'def'): '--', ('UNARYEXPR', 'int'): '--', ('UNARYEXPR', 'new'): '--', ('UNARYEXPR', '!='): '--', ('UNARYEXPR', '>='): '--', ('UNARYEXPR', 'if'): '--', ('UNARYEXPR', '=='): '--', ('UNARYEXPR', '<='): '--', ('UNARYEXPR', '{'): '--', ('UNARYEXPR', '%'): '--', ('UNARYEXPR', ';'): '--', ('UNARYEXPR', '/'): '--', ('UNARYEXPR', '('): 'FACTOR', ('UNARYEXPR', '='): '--', ('UNARYEXPR', '$'): '--', ('UNARYEXPR', '['): '--', ('UNARYEXPR', '-'): '- FACTOR', ('UNARYEXPR', '}'): '--', ('UNARYEXPR', '>'): '--', ('UNARYEXPR', ')'): '--', ('UNARYEXPR', '<'): '--', ('UNARYEXPR', ']'): '--', ('UNARYEXPR', '*'): '--', ('UNARYEXPR', '+'): '+ FACTOR', ('FACTOR', 'string_constant'): 'string_constant', ('FACTOR', 'float_constant'): 'float_constant', ('FACTOR', 'int_constant'): 'int_constant', ('FACTOR', 'return'): '--', ('FACTOR', 'ident('): '--', ('FACTOR', 'ident,'): '--', ('FACTOR', 'string'): '--', ('FACTOR', 'print'): '--', ('FACTOR', 'float'): '--', ('FACTOR', 'break'): '--', ('FACTOR', 'ident'): 'LVALUE', ('FACTOR', 'else'): '--', ('FACTOR', 'null'): 'null', ('FACTOR', 'read'): '--', ('FACTOR', 'for'): '--', ('FACTOR', 'def'): '--', ('FACTOR', 'int'): '--', ('FACTOR', 'new'): '--', ('FACTOR', '!='): '--', ('FACTOR', '>='): '--', ('FACTOR', 'if'): '--', ('FACTOR', '=='): '--', ('FACTOR', '<='): '--', ('FACTOR', '{'): '--', ('FACTOR', '%'): '--', ('FACTOR', ';'): '--', ('FACTOR', '/'): '--', ('FACTOR', '('): '( NUMEXPRESSION )', ('FACTOR', '='): '--', ('FACTOR', '$'): '--', ('FACTOR', '['): '--', ('FACTOR', '-'): '--', ('FACTOR', '}'): '--', ('FACTOR', '>'): '--', ('FACTOR', ')'): '--', ('FACTOR', '<'): '--', ('FACTOR', ']'): '--', ('FACTOR', '*'): '--', ('FACTOR', '+'): '--', ('LVALUE', 'string_constant'): '--', ('LVALUE', 'float_constant'): '--', ('LVALUE', 'int_constant'): '--', ('LVALUE', 'return'): '--', ('LVALUE', 'ident('): '--', ('LVALUE', 'ident,'): '--', ('LVALUE', 'string'): '--', ('LVALUE', 'print'): '--', ('LVALUE', 'float'): '--', ('LVALUE', 'break'): '--', ('LVALUE', 'ident'): 'ident B`', ('LVALUE', 'else'): '--', ('LVALUE', 'null'): '--', ('LVALUE', 'read'): '--', ('LVALUE', 'for'): '--', ('LVALUE', 'def'): '--', ('LVALUE', 'int'): '--', ('LVALUE', 'new'): '--', ('LVALUE', '!='): '--', ('LVALUE', '>='): '--', ('LVALUE', 'if'): '--', ('LVALUE', '=='): '--', ('LVALUE', '<='): '--', ('LVALUE', '{'): '--', ('LVALUE', '%'): '--', ('LVALUE', ';'): '--', ('LVALUE', '/'): '--', ('LVALUE', '('): '--', ('LVALUE', '='): '--', ('LVALUE', '$'): '--', ('LVALUE', '['): '--', ('LVALUE', '-'): '--', ('LVALUE', '}'): '--', ('LVALUE', '>'): '--', ('LVALUE', ')'): '--', ('LVALUE', '<'): '--', ('LVALUE', ']'): '--', ('LVALUE', '*'): '--', ('LVALUE', '+'): '--', ('B`', 'string_constant'): '--', ('B`', 'float_constant'): '--', ('B`', 'int_constant'): '--', ('B`', 'return'): '--', ('B`', 'ident('): '--', ('B`', 'ident,'): '--', ('B`', 'string'): '--', ('B`', 'print'): '--', ('B`', 'float'): '--', ('B`', 'break'): '--', ('B`', 'ident'): '--', ('B`', 'else'): '--', ('B`', 'null'): '--', ('B`', 'read'): '--', ('B`', 'for'): '--', ('B`', 'def'): '--', ('B`', 'int'): '--', ('B`', 'new'): '--', ('B`', '!='): '\\epsilon', ('B`', '>='): '\\epsilon', ('B`', 'if'): '--', ('B`', '=='): '\\epsilon', ('B`', '<='): '\\epsilon', ('B`', '{'): '--', ('B`', '%'): '\\epsilon', ('B`', ';'): '\\epsilon', ('B`', '/'): '\\epsilon', ('B`', '('): '--', ('B`', '='): '\\epsilon', ('B`', '$'): '--', ('B`', '['): '[ NUMEXPRESSION ] B`', ('B`', '-'): '\\epsilon', ('B`', '}'): '--', ('B`', '>'): '\\epsilon', ('B`', ')'): '\\epsilon', ('B`', '<'): '\\epsilon', ('B`', ']'): '\\epsilon', ('B`', '*'): '\\epsilon', ('B`', '+'): '\\epsilon'}#LL1(first, follow, gramatica)

    df = pd.DataFrame()

    for (coluna, linha), valor in tabela.items():
        df.at[coluna, linha] = valor
    if not os.path.exists('tabela.csv'):
        df.to_csv('tabela.csv')
    if not os.path.exists('tabela.xlsx'):
        df.to_excel('tabela.xlsx')


    verificar_sentenca(tokens, tabela, gramatica)

#main()