state = {
    'blablabla' : {
        'view' : 'Представление',
        'value' : [0]
    },
    'stdin': []
}

from . import debug_app, view
import math

def checked(name):
    """Проверка существует ли переменная в словаре"""
    global state
    for k in state.keys():
        if name == k:
            return True
        else:
            continue
    return False

def getvalue(name, pos = 0):
    """Получение значения из словаря по имени"""
    global state
    viewl = view.view(name)
    if name == "Pi":
        return math.pi
    if not checked(name):
        state[name] = {
            'view' : str(viewl),
            'value' : [0]
        }
    lst = state[name]['value']
    if lst[0] == 0:
        val = f_inp('Введите: ',name)
        state['stdin'].append(val)
        lst[0] += 1
        lst.append(val)
        return val
    else:
        return lst[lst[0] + pos]

def putvalue(name, val):
    """Добавить значение в словарь по имени, добавляет в конец списка 'value'"""
    global state
    viewl = view.view(name)
    if not checked(name):
        state[name] = {
            'view' : str(viewl),
            'value' : [0]
        }
    state[name]['value'][0] += 1
    state[name]['value'].append(val)

def f_inp(text, name):
    """Запрос неизвестного значения 
    
    Сначало проверяет есть ли значение в переданном файле в 3 арргументе,
    если нету то запрашивает у пользователя
    
    """
    global state
    print(state['input'])
    try:
        res = float(state['input'][0])
        print(name + ' > ' + str(res))
        del state['input'][0]
        debug_app.app_end_stdin(res)
        return res
    except IndexError:
        res = float(input(text + name + ' >'))
        debug_app.app_end_stdin(res)
        return res

def init(f):
    """Создание эллемента в state с view и списком value значением"""
    global state
    f = str(f)
    arr = f.split('=')
    for i in range(len(arr)):
        arr[i] = arr[i].strip().replace(' ', '').replace('  ', '')
    name = arr[0]
    exp = arr[1]
    del arr
    viewl = view.view(name)
    if not checked(name):
        state[name] = {
            'view' : viewl,
            'value' : [0]
        }
    return (name, exp)