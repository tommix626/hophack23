import re

s = 'jknkj}||20. *jij*-- "2,||*'

print(re.findall(r'\|\|([a-zA-Z0-9.,*"\-\s]+)\|\|', s))
