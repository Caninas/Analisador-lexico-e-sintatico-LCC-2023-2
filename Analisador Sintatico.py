import re

s = "def abc() {\n}"

s = open("./teste.txt", "r").read()

palavras_reservadas = {"def", "int"}

# texto_final = ""
# def seila2(matchobj):
#     global texto_final
#     if matchobj.group(0) in palavras_reservadas or re.match("\w+\d", matchobj.group(0)):
#         texto_final += "IDENT"
    
#     texto_final += "OUTRO"

def substituir(matchobj):
    if matchobj.group(0) in palavras_reservadas or re.match("\w+\d", matchobj.group(0)):
        return "IDENT"
    
    return "OUTRO"

comp = re.compile("\w+|\S", re.MULTILINE)
x = re.findall(comp, s)

j = re.sub(comp, substituir, s)

print(x)
print(j)