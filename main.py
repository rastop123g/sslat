import re
import sys
import os
from modules import state_app, calculate, view, text_manipulation

state = state_app.state

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd_path = os.getcwd()
new_path = cwd_path + '/' + sys.argv[2] + '/'

state['dir_path'], state['cwd_path'], state['new_path'] = dir_path, cwd_path, new_path

if not os.path.exists(new_path):
    os.makedirs(new_path)

file = open(sys.argv[1], 'r')
block = file.read().split("\n\n")
file.close()
del file

try:
    file = open(sys.argv[3], 'r')
    state['input'] = file.read().split('\n')
except IndexError:
    state['input'] = []

try:
    views = re.search(r'view{(.+)}', block[len(block) - 1].replace('\n', '').replace('    ', '').replace('  ', '')).group(1)
    view.initview_of_sec(views)
except AttributeError:
    pass

result_text = []
for s in block:
    rst = s.replace('\n', '').replace('    ', '').replace('  ', '')
    if re.search(r'^##\s*', rst) is not None: # обработка заголовков на ##
        clearstr = re.search(r'^##\s*(.+)', rst).group(1)
        result_string = r'\subsection{' + clearstr + '}\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.search(r'^#\s*', rst) is not None: # обработка заголовков на #
        clearstr = re.search(r'^#\s*(.+)', rst).group(1)
        result_string = r'\section{' + clearstr + '}\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.search(r'^view{', rst) is not None: # блокировка view
        continue
    elif re.search(r'^\{', rst) is not None: # обработка формулы
        clearstr = re.search(r'^\{\n*(.+)\n*\}', rst).group(1)
        result_string = '$$' + calculate.entry_one_exp(clearstr) + '$$' + '\n\n'
        result_text.append(result_string)
        del clearstr, result_string
    elif re.search(r'^\s*\w+', rst) is not None: # обработка простого текста 
        text = re.search(r'^\s*\w+.*', rst).group(0)
        rst = text_manipulation.var_in_text(text)
        result_string = rst + '\n\n'
        result_text.append(result_string)
        del result_string
    del rst
prstr = ''
for i in result_text:
    prstr += i
file = open(dir_path + '/template.tex', 'r')
res = file.read()
file.close()
del file
file = open(new_path + 'out.tex', 'w')
file.write(res.replace('$$content$$', prstr))
file.close()
print('Mission complete!')