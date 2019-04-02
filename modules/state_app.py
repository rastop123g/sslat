state = {
    'blablabla' : {
        'view' : 'Представление',
        'value' : [0]
    },
    'stdin': [],
    'sets': {
        'namesets' : {
            'xadasd' : {
                'view' : 'Представление',
                'value' : [0]
            },
            'ysdgsbst' : {}
        },
        'countsets' : 0
    },
    'views' : {}
}

from . import debug_app, view
import math

def checked(name):
    """Проверка существует ли переменная в словаре"""
    global state
    inst = state['instance']
    for k in inst.keys():
        if name == k:
            return True
        else:
            continue
    return False

def getvalue(name, pos = 0):
    """Получение значения из словаря по имени"""
    global state
    inst = state['instance']
    viewl = view.view(name)
    if name == "Pi":
        return math.pi
    if not checked(name):
        if inst == state:
            inst[name] = {
                'view' : str(viewl),
                'value' : [0]
            }
    try:
        lst = inst[name]['value']
    except KeyError:
        try:
            lst = state[name]['value']
        except KeyError:
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
    inst = state['instance']
    viewl = view.view(name)
    if not checked(name):
        inst[name] = {
            'view' : str(viewl),
            'value' : [0]
        }
    inst[name]['value'][0] += 1
    inst[name]['value'].append(val)

def f_inp(text, name):
    """Запрос неизвестного значения 
    
    Сначало проверяет есть ли значение в переданном файле в 3 арргументе,
    если нету то запрашивает у пользователя
    
    """
    global state
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
    inst = state['instance']
    f = str(f)
    arr = f.split('=')
    for i in range(len(arr)):
        arr[i] = arr[i].strip().replace(' ', '').replace('  ', '')
    name = arr[0]
    exp = arr[1]
    del arr
    viewl = view.view(name)
    if not checked(name):
        inst[name] = {
            'view' : viewl,
            'value' : [0]
        }
    return (name, exp)

def ChangeInst(inst='state', *, name=False):
    """Меняет инстанс расчета"""
    global state
    if inst == 'state':
        state['instance'] = state
    elif inst == 'sets':
        if name == False:
            state['sets']['countsets'] += 1
            name = str(state['sets']['countsets'])
        try:
            if type(state['sets'][name]) == dict:
                state['instance'] = state['sets'][name]
        except KeyError:
            state['sets'][name] = {}
            state['instance'] = state['sets'][name]