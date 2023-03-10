import re

str = '15DF1G5E1SD5F1E'
print(re.sub(r'[0-9]*', '*', str))
print(str.replace(r'[0-9]*', '*'))