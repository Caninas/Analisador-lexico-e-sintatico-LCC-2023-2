# Pedro Guimaraes Caninas (21100509)
# Jose Carlos Zambon de Carvalho (21104934) 
# Joao Victor Neves Zaniboni (21100505)
# Pedro Henrique Leao Schiavinatto (21104935)


class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo_input = codigo
        self.error = False

        self.palavras_reservadas = {"def", "if", "else", "for", "break", "print", "read", 
                            "return", "new", "int", "float", "string", "null"}
        self.simbolos_reservados = {";", "(", ")", "{", "}", "[", "]", "%", "+", "-", "*", 
                            "/", "<", ">", "=", "!"}
        self.simbolos_n_unicos = {"=", "!", "<", ">",}

        self.tabela_palavras_finais = {
            "int": "int_constant",
            "float": "float_constant",
            "string": "string_constant",
        }

        self.tabela_simbolos = dict()
        self.lista_tokens = []


    def ErroLexico(self, char, linha=None, coluna=None, msg="erro não especificado"):
        self.error = True
        print(f"Erro léxico (linha {linha}, coluna {coluna}): " + f"caractere '{char}' não reconhecido")#+ f"(linha {linha}, coluna {coluna})"

    def isSimbUnico(self, caracter):
        return not caracter in self.simbolos_n_unicos 

    def isSimbReservado(self, caracter):
        return caracter in self.simbolos_reservados

    def isEspaco(self, caracter):
        return caracter in [" ", "\n"]

    def isReservado(self, palavra):
        return palavra in self.palavras_reservadas

    def parSimbValido(self, par_simbolos):
        return par_simbolos in ["<=", ">=", "==", "!="]
    
    def analisar(self):
        i = 0
        linha = 1
        coluna = 1

        while i < len(self.codigo_input):       # ler caracter por caracter
            # diagrama letra
            if self.codigo_input[i].isalpha() or self.codigo_input[i] == "_":
                i_inicial = i
                col_inicial = coluna
                i += 1
                coluna += 1

                while self.codigo_input[i].isalnum() or self.codigo_input[i] == "_":
                    i += 1
                    coluna += 1

                if self.isSimbReservado(self.codigo_input[i]) or self.isEspaco(self.codigo_input[i]) or self.codigo_input[i] == ",":
                    palavra = self.codigo_input[i_inicial:i]

                    if self.isReservado(palavra):            # terminal palavra reservada
                        self.lista_tokens.append(palavra)
                    else:
                        if self.codigo_input[i] in [",", "("]:      # terminal ident( e ident,
                            self.lista_tokens.append("ident" + self.codigo_input[i])
                            i += 1
                            coluna += 1
                        else:                                       # terminal ident
                            self.lista_tokens.append("ident")
                        try:
                            self.tabela_simbolos[palavra].append((linha, col_inicial))
                        except:
                            self.tabela_simbolos[palavra] = [(linha, col_inicial)]
                    continue

                self.ErroLexico(self.codigo_input[i], linha, coluna)
                continue
            
            # diagrama int/float
            elif self.codigo_input[i].isnumeric():
                i += 1
                coluna += 1

                while self.codigo_input[i].isnumeric():
                    i += 1
                    coluna += 1

                if self.isSimbReservado(self.codigo_input[i]) or self.isEspaco(self.codigo_input[i]):    # int
                    self.lista_tokens.append(self.tabela_palavras_finais["int"])
                    continue

                elif self.codigo_input[i] == ".":    # se atual == ponto, entao é float
                    i += 1
                    coluna += 1
                    while self.codigo_input[i].isnumeric():
                        i += 1
                        coluna += 1
                    if self.isSimbReservado(self.codigo_input[i]):
                        self.lista_tokens.append(self.tabela_palavras_finais["float"])
                        continue
                
                self.ErroLexico(self.codigo_input[i], linha, coluna)
                continue

            # diagrama string
            elif self.codigo_input[i] in ['"', "'"]:
                i += 1
                coluna += 1
                
                while self.codigo_input[i] not in ['"', "'"]:
                    i += 1
                    coluna += 1

                if self.codigo_input[i] in ['"', "'"]:     # fechamento da string
                    i += 1
                    coluna += 1
                    self.lista_tokens.append(self.tabela_palavras_finais["string"])
                    continue
                
                self.ErroLexico(self.codigo_input[i], linha, coluna)
                continue
            
            # diagrama simbolos
            elif self.isSimbReservado(self.codigo_input[i]):
                if not self.isSimbUnico(self.codigo_input[i]) and not self.isSimbUnico(self.codigo_input[i+1]): # simbolos que podem ter pares (== etc...)
                    if self.parSimbValido(self.codigo_input[i] + self.codigo_input[i+1]):           
                        self.lista_tokens.append(self.codigo_input[i] + self.codigo_input[i+1])
                        i += 2     
                        coluna += 2
                        continue
                    else:
                        self.ErroLexico(self.codigo_input[i] + self.codigo_input[i+1], linha, coluna)
                        continue
                
                self.lista_tokens.append(self.codigo_input[i])         # simbolos unicos
                i += 1
                coluna += 1
                continue
            
            # diagrama espaço / quebra linha 
            elif self.isEspaco(self.codigo_input[i]):
                coluna += 1
                if self.codigo_input[i] == "\n":    # quebra linha reseta coluna e aumenta linha
                    linha += 1
                    coluna = 1

                i += 1
                continue
            
            # fim do texto
            elif self.codigo_input[i] == chr(3):
                break
            
            self.lista_tokens.append(self.codigo_input[i])
            self.ErroLexico(self.codigo_input[i], linha, coluna)
            i += 1

        return self.lista_tokens, self.tabela_simbolos, self.error

