import re
from . import state_app, calculate, text_manipulation, view

state = state_app.state

def BlockProcessing(block):
    """Обработка одного блока"""
    if re.search(r'^##\s*', block) is not None: # обработка заголовков на ##
        clearstr = re.search(r'^##\s*(.+)', block).group(1)
        result = r'\subsection{' + clearstr + '}\n\n'
        return result
    elif re.search(r'^#\s*', block) is not None: # обработка заголовков на #
        clearstr = re.search(r'^#\s*(.+)', block).group(1)
        result = r'\section{' + clearstr + '}\n\n'
        return result
    elif re.search(r'^view{', block) is not None: # блокировка view
        pass
    elif re.search(r'^\{', block) is not None: # обработка формулы
        fobj = re.search(r'^\{\n?(.+)\n?\}(.*)', block)
        exps = fobj.group(1)
        settings = fobj.group(2)
        return SimpleExpressions(exps, settings)
    elif re.search(r'^\s*\w+', block) is not None: # обработка простого текста 
        text = re.search(r'^\s*\w+.*', block).group(0)
        rst = text_manipulation.var_in_text(text)
        result = rst + '\n\n'
        return result

def SimpleExpressions(exps, settings):
    """Обработка блока формул"""
    global state
    state['instance'] = state
    result = ''
    sett_arr = settings.split('.')
    exp_arr = exps.split('\n')
    if 'numeration' in sett_arr:
        startenv = '\\begin{equation}\n'
        endenv = '\n\\label{eq:}\n\\end{equation}\n\n'
    else:
        startenv = '$$'
        endenv = '$$\n\n'
    for exp in exp_arr:
        result += startenv + calculate.entry_one_exp(exp) + endenv
    return result
    