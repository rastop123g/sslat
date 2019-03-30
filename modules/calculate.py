import re
import math
from . import view, state_app

state = state_app.state

def entry_one_exp(f):
    """Начало обработки блока формулы"""
    global state
    arr_form = f.split('%')
    try:
        unit = arr_form[1]
        unit = view.text_to_unit_latex(unit)
    except IndexError:
        unit = ''
    name, exp = state_app.init(arr_form[0])
    computed = exp
    while True:
        if is_digit(computed):
            print(name + ' > ' + computed)
            state_app.putvalue(name, float(computed))
            break
        else:
            computed = calc(computed)
    retstr = view.finalstr(name, exp, unit)
    return retstr

def calc(exp):
    """Вычесление выражения"""
    global state
    if re.search(r'(?:\W|^)\([^()]+\)', exp) is not None: # скобки
        s = re.search(r'(?:\W|^)(\(([^()]+)\))', exp)
        val = calc(s.group(2)).strip()
        if is_digit(val):
            return exp.replace(s.group(1), str(val))
        else:
            return exp.replace(s.group(1), '(' + str(val) + ')')
    elif re.search(r'sqrt\([^()]+\)', exp) is not None: # корень
        s = re.search(r'sqrt\(([^()]+)\)', exp)
        val = calc(s.group(1)).strip()
        if is_digit(val):
            sq = float(val) ** 0.5
            return exp.replace(s.group(0), str(sq))
        else:
            return exp.replace(s.group(0), 'sqrt(' + str(val) + ')')
    elif re.search(r'ln\([^()]+\)', exp) is not None: # ln
        s = re.search(r'ln\(([^()]+)\)', exp)
        val = calc(s.group(1)).strip()
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
                numsplit[i] = float(state_app.getvalue(var))
        val = numsplit[0] ** numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*/(?:-|)\w+\.?\d*', exp) is not None: # деление
        s = re.search(r'((?:-|^|)\w+\.?\d*/(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('/')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(state_app.getvalue(var))
        val = numsplit[0] / numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*\*(?:-|)\w+\.?\d*', exp) is not None: # умножение
        s = re.search(r'((?:-|^|)\w+\.?\d*\*(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('*')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(state_app.getvalue(var))
        val = numsplit[0] * numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*\+(?:-|)\w+\.?\d*', exp) is not None: # сложение
        s = re.search(r'((?:-|^|)\w+\.?\d*\+(?:-|)\w+\.?\d*)', exp).group(0)
        numsplit = s.split('+')
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(state_app.getvalue(var))
        val = numsplit[0] + numsplit[1]
        return exp.replace(s, str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*-(?:-|)\w+\.?\d*', exp) is not None: # вычитание
        s = re.search(r'((?:-|^|)\w+\.?\d*)-((?:-|)\w+\.?\d*)', exp)
        numsplit = [s.group(1), s.group(2)]
        for i, var in enumerate(numsplit):
            if is_digit(var):
                numsplit[i] = float(var)
            else:
                numsplit[i] = float(state_app.getvalue(var))
        val = numsplit[0] - numsplit[1]
        return exp.replace(s.group(0), str('{:.15f}').format(float(val)))
    elif re.search(r'(?:-|^|)\w+\.?\d*', exp) is not None:
        s = re.search(r'(?:-|^|)\w+\.?\d*', exp).group(0)
        if is_digit(s):
            return exp
        else:
            return exp.replace(s, str('{:.15f}').format(float(state_app.getvalue(s))))
    


def is_digit(string):
    """Проверка является ли строка числом"""
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False
