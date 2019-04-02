import re
import logging as log
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
    elif re.search(r'^for \w+=\([\d,.]+\)\{\n?(?:.|\n)+\n?\}.*\n?', block) is not None:
        sobj = re.search(r'^for (\w+)=\(([\d,.\-]+)\)\{\n?((?:.|\n)+)\n?\}(.*)\n?', block)
        name, enum, exps, settings = sobj.group(1), sobj.group(2), sobj.group(3), sobj.group(4)
        if exps[-1] == '\n':
            exps = exps[0:-1]
        return BruteForceCollection(name, enum, exps, settings)
    elif re.search(r'^\{', block) is not None: # обработка формулы
        fobj = re.search(r'^\{\n?((?:.|\n)+)\n?\}(.*)\n?', block)
        exps = fobj.group(1)
        if exps[-1] == '\n':
            exps = exps[0:-1]
        settings = fobj.group(2)
        log.info('Обработка блока формул > ' + exps)
        return SimpleExpressions(exps, settings)
    elif re.search(r'^\s*\w+', block) is not None: # обработка простого текста 
        text = re.search(r'^\s*\w+(?:.|\n)*', block).group(0)
        rst = text_manipulation.var_in_text(text)
        result = rst + '\n\n'
        return result

def SimpleExpressions(exps, settings):
    """Обработка блока формул"""
    state_app.ChangeInst()
    result = ''
    sett_arr = settings.split('.')
    exp_arr = exps.split('\n')
    if is_settings('numeration', sett_arr):
        startenv = '\\begin{equation}\n'
        endenv = '\n\\label{eq:}\n\\end{equation}\n\n'
    else:
        startenv = '$$'
        endenv = '$$\n\n'
    for exp in exp_arr:
        result += startenv + calculate.entry_one_exp(exp) + endenv
    return result
    
def BruteForceCollection(name, collection, exps, settings):
    """Обработка блока перебора значений"""
    global state
    settings = settings.split('.')
    is_all = is_settings('all', settings)
    state_app.ChangeInst('sets', name=is_settings('name', settings))
    inst = state['instance']
    collection = collection.split(',')
    exps = exps.split('\n')
    result_eq = ''
    if is_settings('numeration', settings):
        startenv = '\\begin{equation}\n'
        endenv = '\n\\label{eq:}\n\\end{equation}\n\n'
    else:
        startenv = '$$'
        endenv = '$$\n\n'
    for i, val in enumerate(collection):
        state_app.putvalue(name, float(val))
        for exp in exps:
            if is_all:
                result_eq += startenv + calculate.entry_one_exp(exp) + endenv
            else:
                if i == 0:
                    result_eq += startenv + calculate.entry_one_exp(exp) + endenv
                else:
                    calculate.entry_one_exp(exp, latex_view=False)
    if is_settings('table', settings):
        count_collumn = len(collection) + 1
        tmp_list = [i for i in 'c'*count_collumn]
        name_t = '{' + str(is_settings('table', settings)) + '}'
        num_col = '|'.join(tmp_list)
        ltable_start = '\\begin{table}[h]\n' + '\\caption' + name_t + '\n' + '\\begin{center}\n\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill} } ' + num_col + '}\n' + '\\hline\n'
        table_content = ''
        for name_val in inst.keys():
            tmp_list = inst[name_val]['value'][1:]
            for i, item in enumerate(tmp_list):
                tmp_list[i] = '$' + view.numbertols(item) + '$'
            tb_val = ' & '.join(tmp_list)
            table_content += '$' + str(inst[name_val]['view']) + '$ ' + '&' + tb_val + '\\\\' + '\n\\hline\n'
        ltable_end = '\\end{tabular*}\n\\end{center}\n\\end{table}\n\n'
        result_table = ltable_start + table_content + ltable_end
    else:
        result_table = ''
    if is_settings('graph', settings):
        pass
    return str(result_eq + result_table)
    

def is_settings(name, settings):
    """Проверка есть ли данный флаг в настройках.
    
    Вернет True если есть, если флаг составной то вернет значение, иначе вернет False
    """
    if name in settings:
        return True
    else:
        for s in settings:
            if s.startswith(name):
                return s.split('=')[1]
            else:
                continue
    return False
