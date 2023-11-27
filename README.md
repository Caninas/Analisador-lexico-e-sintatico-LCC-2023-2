# Analisadores Léxico e Sintático

Trabalho da disciplina de INE5622-20232 (Introdução a Compiladores), do curso de Sistemas de informação, da Universisade Federal de Santa Catarina. A atividade consiste no desenvolvimento de um Analisador Léxico e um Analisador Sintático, para a linguagem LCC-2023-2 (demonstrada no arquivo "lcc-2023-2.txt").

## Equipe

- João Zaniboni 		(21100505)
- José Carlos Zambon 	(21104934)
- Pedro Caninas 		(21100509)
- Pedro Schiavinatto 		(21104935)

## Estrutura do código

Os analisadores foram desenvolvidos em Python (3.9.12) 64bits e estruturados em classes.

## Arquivos:

- `Analisador_Lexico.py/` refere-se ao analisador léxico;
- `Analisador_Sintatico.py/` refere-se ao analisador sintático;
- `lcc-2023-2.txt/` refere-se à linguagem LCC-2023-2
- `codigo1.lcc/`, `codigo2.lcc/` e `codigo3.lcc/` são os três códigos .lcc

## Execução

Basta abrir a pasta que contém o makefile no terminal e exercutar o comando 'make install' para instalar as bibliotecas necessárias. Em seguida execute 'make'. O Analisador Léxico será executado, printando erros encontrados. Caso não tenha erro léxico ele continua com a execução do Analisador Sintático.

O makefile executa o arquivo main.py que se encarrega de pegar o path do código a ser analisado e executar o Analisador_Lexico.py e Analisador_Sintatico.py. Além disso make install instala as dependências descrita no arquivo requirements.txt
