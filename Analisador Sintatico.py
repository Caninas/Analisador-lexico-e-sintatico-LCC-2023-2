import re


s = "def abc() {"
""
"}"


x = re.findall("\w*\S[^()]", s)
#re.sub

print(x)