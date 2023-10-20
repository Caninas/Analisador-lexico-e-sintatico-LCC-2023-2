import re

s = "def abc() {\n}"

s = open("./teste.txt", "r").read()
s = open("./exemplo1.lcc", "r").read()

palavras_reservadas = {"def", "int"}

# texto_final = ""
# def seila2(matchobj):
#     global texto_final
#     if matchobj.group(0) in palavras_reservadas or re.match("\w+\d", matchobj.group(0)):
#         texto_final += "IDENT"
    
#     texto_final += "OUTRO"

def substituir(matchobj):
    #print(s[matchobj.start(0)-1:matchobj.end(0)], end="")
    if matchobj.group(0) in palavras_reservadas or re.match("\w+|\d", matchobj.group(0)):
        return "IDENT"
    
    # if anterior primeiro != " ": " OUTRO" elif final != " " return "OUTRO " else return " OUTRO "

    if s[matchobj.start(0)-1] == " " and s[matchobj.end(0):matchobj.end(0)+1] == " ":
        return "OUTRO"
    
    elif s[matchobj.start(0)-1] == " " and s[matchobj.end(0):matchobj.end(0)+1] != " ":
        return "OUTRO "
    
    elif s[matchobj.end(0):matchobj.end(0)+1] == " " and s[matchobj.start(0)-1] != " ":
        return " OUTRO"
    
    elif s[matchobj.start(0)-1] in [ "\n"] :
        return "OUTRO"
    else:
        return " OUTRO "

comp = re.compile("\w+|\S", re.MULTILINE)
x = re.findall(comp, s)

j = re.sub(comp, substituir, s)

print(s)
print(j)