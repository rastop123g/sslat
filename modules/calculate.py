import re
from . import view

def strtolatex(f, state):
    name, exp = init(f,state)                               # создание элемента словаря если его нету
    #print(name + '\n' + exp)
    endresult = exp                                         # Вычисление формулы
    while True:                                             #
        if is_digit(endresult):                             #
            putvalue(name, float(endresult), state)         #
            break                                           #
        else:                                               #
            endresult = calc(endresult, state)              #
            print('endresult >' + str(endresult))           #
    retstr = finalstr(name, exp, state)
    return retstr



def checked(name, state):                                   # Функция проверки имени в словаре
    for k in state.keys():
        if name == k:
            return True
        else:
            continue
    return False

def getvalue(name, state, pos = 0):
    viewl = view.view(name)
    if not checked(name, state):
        state[name] = {
            'view' : str(viewl),
            'value' : [0]
        }
    lst = state[name]['value']
    if lst[0] == 0:
        val = float(input('Введите: ' + name + ' >'))
        lst[0] += 1
        lst.append(val)
        return val
    else:
        return lst[lst[0] + pos]

def putvalue(name, val, state):
    state[name]['value'][0] += 1
    state[name]['value'].append(val)

def init(f, state):
    f = str(f)
    arr = f.split('=')
    for i in range(len(arr)):
        arr[i] = arr[i].strip().replace(' ', '').replace('  ', '')
    name = arr[0]
    exp = arr[1]
    del arr
    viewl = view.view(name)
    if not checked(name, state):
        state[name] = {
            'view' : viewl,
            'value' : [0]
        }
    return (name, exp)

def calc(exp, state):
    if re.search(r'\W\([^()]+\)', exp) is not None: # скобки
        arr = re.findall(r'\W\(([^()]+)\)', exp)
        num = []
        for i, ilst in enumerate(arr):
            print(str(i) + '>' + ilst)
            num.append(calc(ilst, state))
            num[i] = num[i].strip()
            if is_digit(num[i]):
                return exp.replace('(' + arr[i] + ')', str(num[i]))
            else:
                return exp.replace('(' + arr[i] + ')', '(' + num[i] + ')')
        #print('tmp: ', arr)
        #print('exp:' + exp)
    elif re.search(r'sqrt\(.+\)', exp) is not None: # корень
        arr = re.findall(r'sqrt\(([^()]+)\)', exp)
        num = []
        for i, ilst in enumerate(arr):
            print(str(i) + '>' + ilst)
            num.append(calc(ilst, state))
            num[i] = num[i].strip()
            if is_digit(num[i]):
                sq = float(num[i]) ** 0.5
                return exp.replace('sqrt(' + arr[i] + ')', str(sq))
            else:
                return exp.replace('sqrt(' + arr[i] + ')', 'sqrt(' + num[i] + ')')
    elif re.search(r'\w+\.?\d*\*{2}\w+\.?\d*', exp) is not None: # степень
        s = re.search(r'(\w+\.?\d*\*{2}\w+\.?\d*)', exp).group(0)
        numsplit = s.split('**')
        print(s)
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        print(numsplit)
        val = numsplit[0] ** numsplit[1]
        return exp.replace(s, str(val))
    elif re.search(r'\w+\.?\d*/\w+\.?\d*', exp) is not None: # деление
        s = re.search(r'(\w+\.?\d*/\w+\.?\d*)', exp).group(0)
        print(s)
        numsplit = s.split('/')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        print(numsplit)
        val = numsplit[0] / numsplit[1]
        return exp.replace(s, str(val))
    elif re.search(r'\w+\.?\d*\*\w+\.?\d*', exp) is not None: # умножение
        s = re.search(r'(\w+\.?\d*\*\w+\.?\d*)', exp).group(0)
        print(s)
        numsplit = s.split('*')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        print(numsplit)
        val = numsplit[0] * numsplit[1]
        return exp.replace(s, str(val))
    elif re.search(r'\w+\.?\d*\+\w+\.?\d*', exp) is not None: # сложение
        s = re.search(r'(\w+\.?\d*\+\w+\.?\d*)', exp).group(0)
        print(s)
        numsplit = s.split('+')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        print(numsplit)
        val = numsplit[0] + numsplit[1]
        return exp.replace(s, str(val))
    elif re.search(r'\w+\.?\d*-\w+\.?\d*', exp) is not None: # вычитание
        s = re.search(r'(\w+\.?\d*-\w+\.?\d*)', exp).group(0)
        print(s)
        numsplit = s.split('-')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        print(numsplit)
        val = numsplit[0] - numsplit[1]
        return exp.replace(s, str(val))
    elif re.search(r'\w+\.?\d*', exp) is not None:
        s = re.search(r'\w+\.?\d*', exp)
        if is_digit(s):
            return exp
        else:
            return exp.replace(s, str(getvalue(s, state)))
    


def is_digit(string): # Является ли строка числом
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

def numbertols(num): # Перевод числа в latex с округлением до 3 значащих цифр
    num = float(num)
    steps = -30
    while True:
        chan = 10 ** steps
        if num > chan:
            steps += 1
            if steps > 50:
                break
            continue
        else:
            n = steps
            break
    if n >= 4:
        sm = num / (10 ** (n-1))
        result = round(sm, 2)
        st = str(result) + ' \cdot 10^{' + str(n-1) + '}'
        return st
    elif n >= -1:
        result = round(num, 3 - n)
        if result.is_integer():
            return str(int(result))
        return str(result)
    else:
        sm = num / (10 ** (n-1))
        result = round(sm, 2)
        st = str(result) + ' \cdot 10^{' + str(n-1) + '}'
        return st

def finalstr(name, exp, state):
    tmpdict = {
        'a' : 'srtoka'
    }
    exp = exptolatex(exp, tmpdict)
    print('jaja:' + exp)
    while re.search(r'exp\d+', exp):
        rp = re.search(r'exp\d+', exp).group(0)
        exp = exp.replace(rp, tmpdict[rp])
    ltexp = exp
    for k in state.keys():
        regexp = r'(\W)(' + k + r')(\W)'
        findstr = re.search(regexp, ltexp)
        if findstr is not None:
            ltexp = ltexp.replace(findstr.group(0), findstr.group(1) + state[k]['view'] + findstr.group(3))
    ltexp = ltexp.replace('*', '')
    numexp = exp
    for k in state.keys():
        regexp = r'(\W?)(' + k + r')(\W?)'
        findstr = re.search(regexp, numexp)
        if findstr is not None:
            numexp = numexp.replace(findstr.group(0), findstr.group(1) + str(numbertols(getvalue(k, state))) + findstr.group(3))
    numexp = numexp.replace('*', ' \cdot ')
    result = state[name]['view'] + ' = ' + ltexp + ' = ' + numexp + '=' + str(numbertols(getvalue(name, state)))
    del tmpdict
    return result

def exptolatex(exp, tmpdict): # надо сделать корень
    i = 0
    while True:
        if re.search(r'\*\*', exp) is not None:
            exp = exp.replace('**', '^')
        elif re.search(r'\([^()]+\)', exp) is not None:
            rsobj = re.search(r'\(([^()]+)\)', exp)
            tmpdict['exp' + str(i)] = '(' + rsobj.group(1) + ')'
            exp = exp.replace(tmpdict['exp' + str(i)], 'exp' + str(i))
            i += 1
        elif re.search(r'exp\d+/exp\d+', exp) is not None:
            rsobj = re.search(r'(exp\d+)/(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '\\frac{' + tmpdict[rsobj.group(1)][1:-1] + '}{' + tmpdict[rsobj.group(2)][1:-1] + '}'
            exp = exp.replace(rsobj.group(1) + '/' + rsobj.group(2), 'exp' + str(i))
            i += 1
        elif re.search(r'\w+/\w+', exp) is not None:
            rsobj = re.search(r'(\w+)/(\w+)', exp)
            tmpdict['exp' + str(i)] = '\\frac{' + rsobj.group(1) + '}{' + rsobj.group(2) + '}'
            exp = exp.replace(rsobj.group(1) + '/' + rsobj.group(2), 'exp' + str(i))
            i += 1
        else:
            break
    print('tmpdict: ', tmpdict)
    return exp