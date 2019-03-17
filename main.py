import re
import sys
from modules import calculate, view

file = open(sys.argv[1], 'r')
block = file.read().split("\n\n")
file.close()
del file
state = {
    'blablabla' : {
        'view' : 'Представление',
        'value' : [0]
    },
    'stdin': []
}
views = re.search(r'view{(.+)}', block[len(block) - 1].replace('\n', '').replace('    ', '').replace('  ', '')).group(1)
view.initview_of_sec(views, state)
result_text = []
for s in block:
    rst = s.replace('\n', '').replace('    ', '').replace('  ', '')
    #rst = s.replace('    ', '').replace('  ', '')
    if re.match(r'^#\s*', rst) is not None: # обработка заголовков на #
        clearstr = re.findall(r'^#\s*(.+)', rst)
        result_string = r'\section{' + clearstr[0] + '}\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.match(r'^view{', rst) is not None: # блокировка view
        continue
    elif re.match(r'^##\s*', rst) is not None: # обработка заголовков на ##
        clearstr = re.findall(r'^##\s*(.+)', rst)
        result_string = r'\subsection{' + clearstr[0] + '}\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.match(r'^\{', rst) is not None: # обработка формулы
        clearstr = re.findall(r'^\{\n*(.+)\n*\}', rst)
        result_string = '$$' + calculate.strtolatex(clearstr[0], state) + '$$' + '\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.match(r'^\s*\w+', rst) is not None: # обработка простого текста 
        text = re.search(r'^\s*\w+.*', rst).group(0)
        rst = calculate.var_in_text(text, state)
        result_string = rst + '\n\n'
        result_text.append(result_string)
        del result_string

    del rst
# del block
# block = k
# del k
prstr = ''
for i in result_text:
    prstr += i
prstr = fix(prstr)
file = open('stdin.txt', 'w')
for va in state['stdin']:
    file.write(str(va) + '\n')
file.close()
file = open('template.tex', 'r')
res = file.read()
file.close()
del file
file = open(sys.argv[2], 'w')
file.write(res.replace('$$content$$', prstr))
file.close()
print('Mission complete!')

def fix(lat):
    while True:
        if re.search(r'\^\d+\.?\d*',lat) is not None:
            searobj = re.search('\^(\d+\.?\d*)',lat)
            lat = lat.replace(searobj.group(0), '^{' + searobj.group(1) + '}')
        elif re.search(r'\d+\.?\d* \cdot 10\^\{\d+\}\^\{\d+\.?\d*\}', lat) is not None:
            searobj = re.search(r'(\d+\.?\d* \cdot 10\^\{\d+\})\^\{\d+\.?\d*\}', lat)
            lat = lat.replace(searobj.group(0), searobj.group(0).replace(searobj.group(1), '{' + searobj.group(1) + '}'))
        elif re.search(r'\(\\frac\{.+\}\{.+\}\)\^\(\\frac\{.+\}\{.+\}\)', lat) is not None:
            searobj = re.search(r'\((\\frac\{.+\}\{.+\})\)\^\(\\frac\{(.+)\}\{(.+)\}\)', lat)
            if searobj.group(2) == '1':
                lat = lat.replace(searobj.group(0), '\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}')
            else: 
                lat = lat.replace(searobj.group(0), '{\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}' + '}^{' + searobj.group(2) + '}')
        else:
            break
    return lat