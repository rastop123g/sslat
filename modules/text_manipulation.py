import re
from . import state_app, view

state = state_app.state

def var_in_text(text):
    """Обработка выражений вида {var} в блоке простого текста"""
    global state
    inst = state['instance']
    while True:
        if re.search(r'{\w+=}', text) is not None:
            sp_exp = re.search(r'{(\w+=)}', text)
            if re.search(r'(\w+)=', sp_exp.group(1)) is not None:
                name = re.search(r'(\w+)=', sp_exp.group(1)).group(1)
                val = state_app.f_inp('Введите уточненный ', name)
                state['stdin'].append(val)
                state_app.putvalue(name, val)
                res_str = '$' + inst[name]['view'] + ' = ' + str(view.numbertols(val)) + '$'
                text = text.replace(sp_exp.group(0), res_str)
        else:
            break
    return text