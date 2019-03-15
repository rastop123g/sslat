import re
import math
from . import view

def strtolatex(f, state):
    name, exp = init(f,state)                               # создание элемента словаря если его нету
    endresult = exp                                         # Вычисление формулы
    while True:                                             #
        print('en > ' + endresult)
        if is_digit(endresult):                             #
            print(name + ' > ' + endresult)
            putvalue(name, float(endresult), state)         #
            break                                           #
        else:                                               #
            endresult = calc(endresult, state)              #
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
    if re.search(r'(?:\W|^)\([^()]+\)', exp) is not None: # скобки
        s = re.search(r'(?:\W|^)(\(([^()]+)\))', exp)
        val = calc(s.group(2), state).strip()
        if is_digit(val):
            return exp.replace(s.group(1), str(val))
        else:
            return exp.replace(s.group(1), '(' + str(val) + ')')
    elif re.search(r'sqrt\([^()]+\)', exp) is not None: # корень
        s = re.search(r'sqrt\(([^()]+)\)', exp)
        val = calc(s.group(1), state).strip()
        if is_digit(val):
            sq = float(val) ** 0.5
            return exp.replace(s.group(0), str(sq))
        else:
            return exp.replace(s.group(0), 'sqrt(' + str(val) + ')')
    elif re.search(r'ln\([^()]+\)', exp) is not None: # ln
        s = re.search(r'ln\(([^()]+)\)', exp)
        val = calc(s.group(1), state).strip()
        if is_digit(val):
            sq = math.log(float(val))
            return exp.replace(s.group(0), str(sq))
        else:
            return exp.replace(s.group(0), 'ln(' + str(val) + ')')
    elif re.search(r'(?:-|^|)\w+\.?\d*\*{2}(?:-|)\w+\.?\d*', exp) is not None: # степень
        s = re.search(r'((?:-|^|)\w+\.?\d*\*{2}(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('**')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        val = numsplit[0] ** numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*/(?:-|)\w+\.?\d*', exp) is not None: # деление
        s = re.search(r'((?:-|^|)\w+\.?\d*/(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('/')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        val = numsplit[0] / numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*\*(?:-|)\w+\.?\d*', exp) is not None: # умножение
        s = re.search(r'((?:-|^|)\w+\.?\d*\*(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('*')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        val = numsplit[0] * numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*\+(?:-|)\w+\.?\d*', exp) is not None: # сложение
        s = re.search(r'((?:-|^|)\w+\.?\d*\+(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('+')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        val = numsplit[0] + numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*-(?:-|)\w+\.?\d*', exp) is not None: # вычитание
        s = re.search(r'((?:-|^|)\w+\.?\d*)-((?:-|)\w+\.?\d*)', exp)
        numsplit = [s.group(1), s.group(2)]
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(getvalue(var, state))
        val = numsplit[0] - numsplit[1]
        return exp.replace(s.group(0), str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*', exp) is not None:
        s = re.search(r'(?:-|^|)\w+\.?\d*', exp).group(0)
        if is_digit(s):
            return exp
        else:
            return exp.replace(s, str('{:.15f}').format(float(getvalue(s, state))))
    


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
    signed = re.search(r'((?:-|))\d+\.?\d*', str(num)).group(1)
    num = str(num).replace(signed, '')
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
        return str(signed + st)
    elif n >= -1:
        result = round(num, 3 - n)
        if result.is_integer():
            return str(signed + str(int(result)))
        return str(signed + str(result))
    else:
        sm = num / (10 ** (n-1))
        result = round(sm, 2)
        st = str(result) + ' \cdot 10^{' + str(n-1) + '}'
        return str(signed + st)

def finalstr(name, exp, state):
    tmpdict = {}
    exp = exptolatex(exp, tmpdict)
    while re.search(r'exp\d+', exp):
        rp = re.search(r'exp\d+', exp).group(0)
        exp = exp.replace(rp, tmpdict[rp])
    ltexp = exp
    for k in state.keys():
        regexp = r'((?:\W|^))(' + k + r')((?:\W|$))'
        findstr = re.search(regexp, ltexp)
        if findstr is not None:
            ltexp = ltexp.replace(findstr.group(0), findstr.group(1) + state[k]['view'] + findstr.group(3))
    ltexp = ltexp.replace('*', '')
    numexp = exp
    for k in state.keys():
        regexp = r'((?:\W|^))(' + k + r')((?:\W|$))'
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
        if re.search(r'\*\*', exp) is not None: # степень
            exp = exp.replace('**', '^')
        elif re.search(r'sqrtexp\d+', exp) is not None: #корень
            rsobj = re.search(r'(sqrt)(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '\\sqrt{' + tmpdict[rsobj.group(2)][1:-1] + '}'
            exp = exp.replace(rsobj.group(0), 'exp' + str(i))
            i += 1
        elif re.search(r'lnexp\d+', exp) is not None: #корень
            rsobj = re.search(r'(ln)(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '\\ln{' + tmpdict[rsobj.group(2)][1:-1] + '}'
            exp = exp.replace(rsobj.group(0), 'exp' + str(i))
            i += 1
        elif re.search(r'\([^()/]+\)', exp) is not None: # скобки
            rsobj = re.search(r'\(([^()]+)\)', exp)
            tmpdict['exp' + str(i)] = '(' + rsobj.group(1) + ')'
            exp = exp.replace(tmpdict['exp' + str(i)], 'exp' + str(i))
            i += 1
        elif re.search(r'\w+\.?\d*/\w+\.?\d*', exp) is not None: # тоже деление
            rsobj = re.search(r'(\w+\.?\d*)/(\w+\.?\d*)', exp)
            if re.search(r'exp\d+', rsobj.group(1)) is not None:
                onefr = tmpdict[rsobj.group(1)][1:-1]
            else:
                onefr = rsobj.group(1)
            if re.search(r'exp\d+', rsobj.group(2)) is not None:
                twofr = tmpdict[rsobj.group(2)][1:-1]
            else:
                twofr = rsobj.group(2)
            tmpdict['exp' + str(i)] = '\\frac{' + onefr + '}{' + twofr + '}'
            exp = exp.replace(rsobj.group(1) + '/' + rsobj.group(2), 'exp' + str(i))
            i += 1
        else:
            break
    return exp

def var_in_text(text,state):
    while True:
        if re.search(r'{\w+=}', text) is not None:
            sp_exp = re.search(r'{(\w+=)}', text)
            if re.search(r'(\w+)=', sp_exp.group(1)) is not None:
                name = re.search(r'(\w+)=', sp_exp.group(1)).group(1)
                val = float(input('Введите уточненный '+ name + ' > '))
                putvalue(name, val, state)
                res_str = state[name]['view'] + ' = ' + str(numbertols(val))
                text = text.replace(sp_exp.group(0), res_str)
        else:
            break
    return text