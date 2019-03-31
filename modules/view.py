import re
from . import state_app, calculate

state = state_app.state

def initview_of_sec(vsec):
    """Обработка view секции создание елементов state"""
    global state
    arr = vsec.split(',')
    for item in arr:
        name = item.split('=')[0].strip()
        elview = item.split('=')[1].strip().replace('"', '')
        state["views"].update({name : elview})

def view(name):
    """Обработка имен создание latex строки из имени переменной"""
    global state
    if name in state["views"].keys():
        return '{' + state["views"][name] + '}'
    else:
        searchobj = re.search(r'([a-zA-Zа-яА-Я0-9ёЁ]+)_?([a-zA-Zа-яА-Я0-9ёЁ]*)_?([a-zA-Zа-яА-Я0-9ёЁ]*)', name)
        result = '\\text{' + searchobj.group(1) + '}'
        if searchobj.group(3):
            if searchobj.group(3) == 'l':
                result +=  '^{\\prime}'
            elif searchobj.group(3) == 'll':
                result +=  '^{\\prime\\prime}'
            elif searchobj.group(3) == 'lll':
                result += '^{\\prime\\prime\\prime}'
            else:
                result +=  '^\\text{' + searchobj.group(3) + '}'
        if searchobj.group(2):
            result += '_\\text{' + searchobj.group(2) + '}'
        #print(result)
        return '{' + result + '}'

def exptolatex(exp, tmpdict):
    """Перевод формулы в latex формулу строку"""
    i = 0
    while True:
        if re.search(r'\w+\.?\d*\^\w+\.?\d*', exp) is not None: # степень
            rsobj = re.search(r'(\w+\.?\d*)\^(\w+\.?\d*)', exp)
            if re.search(r'exp\d+', rsobj.group(1)) is not None:
                onefr = '(' + tmpdict[rsobj.group(1)][1:-1] + ')'
            else:
                onefr = rsobj.group(1)
            if re.search(r'exp\d+', rsobj.group(2)) is not None:
                twofr = '(' + tmpdict[rsobj.group(2)][1:-1] + ')'
            else:
                twofr = rsobj.group(2)
            tmpdict['exp' + str(i)] = '{' + '{' + onefr + '}' + '^' + '{' + twofr + '}' + '}'
            exp = exp.replace(rsobj.group(1) + '^' + rsobj.group(2), 'exp' + str(i))
            i += 1
        elif re.search(r'sqrtexp\d+', exp) is not None: #корень
            rsobj = re.search(r'(sqrt)(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '{' + '\\sqrt{' + tmpdict[rsobj.group(2)][1:-1] + '}' + '}'
            exp = exp.replace(rsobj.group(0), 'exp' + str(i))
            i += 1
        elif re.search(r'lnexp\d+', exp) is not None: #ln
            rsobj = re.search(r'(ln)(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '{' + '\\ln{' + tmpdict[rsobj.group(2)][1:-1] + '}' + '}'
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
            tmpdict['exp' + str(i)] = '\\dfrac{' + onefr + '}{' + twofr + '}'
            exp = exp.replace(rsobj.group(1) + '/' + rsobj.group(2), 'exp' + str(i))
            i += 1
        else:
            break
    return exp

def finalstr(name, exp, unit):
    """Создание финальной строки вида name = exp = digit_exp = num unit"""
    global state
    inst = state['instance']
    tmpdict = {}
    exp = exp.replace('**', '^')
    exp = exptolatex(exp, tmpdict)
    while re.search(r'exp\d+', exp):
        rp = re.search(r'exp\d+', exp).group(0)
        exp = exp.replace(rp, tmpdict[rp])
    ltexp = exp
    for k in inst.keys():
        regexp = r'((?:[^t][^e][^x][^t][^\w\\]|[^e][^x][^t][^\w\\]|[^x][^t][^\w\\]|[^t][^\w\\]|[+\-*/=^]|^))(' + k + r')((?:\W|$))'
        while True:
            findstr = re.search(regexp, ltexp)
            if findstr is not None:
                ltexp = ltexp.replace(findstr.group(0), findstr.group(1) + inst[k]['view'] + findstr.group(3))
            else:
                break
    ltexp = ltexp.replace('*', '')
    numexp = exp
    for k in inst.keys():
        regexp = r'((?:[^t][^e][^x][^t][^\w\\]|[^e][^x][^t][^\w\\]|[^x][^t][^\w\\]|[^t][^\w\\]|[+\-*/=^]|^))(' + k + r')((?:\W|$))'
        obj_name = re.search(r'([a-zA-Zа-яА-Я0-9ёЁ]+)_?([a-zA-Zа-яА-Я0-9ёЁ]*)_?([a-zA-Zа-яА-Я0-9ёЁ]*)', k)
        if obj_name.group(2) is not '':
            plus_index = '_{ }'
        else:
            plus_index = ''
        while True:
            findstr = re.search(regexp, numexp)
            if findstr is not None:
                numexp = numexp.replace(findstr.group(0), findstr.group(1) + '{' + str(numbertols(state_app.getvalue(k))) + '}' + plus_index + findstr.group(3))
            else:
                break
    numexp = numexp.replace('*', ' \\cdot ')
    result = inst[name]['view'] + ' = ' + ltexp + \
        ' = ' + numexp + '=' + str(numbertols(state_app.getvalue(name))) + '\\text{ }' + unit
    result = fix(result)
    del tmpdict
    return result

def numbertols(num):
    """Перевод float числа в latex строку включая перевод больших чисел в простые вида num * 10^x"""
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
        st = str(result) + ' \\cdot 10^{' + str(n-1) + '}'
        return str(signed + st)
    elif n >= -1:
        result = round(num, 3 - n)
        if result.is_integer():
            return str(signed + str(int(result)))
        return str(signed + str(result))
    else:
        sm = num / (10 ** (n-1))
        result = round(sm, 2)
        st = str(result) + ' \\cdot 10^{' + str(n-1) + '}'
        return str(signed + st)

def fix(lat):
    """Фиксы: перевод степени 1/n в корень n степени, коректное отображение простого числа в степени"""
    while True:
        if re.search(r'\{\(\\dfrac\{.+?\}\{.+?\}\)\}\^\{\(\\dfrac\{.+?\}\{.+?\}\)\}', lat) is not None:
            searobj = re.search(r'\{\((\\dfrac\{.+?\}\{.+?\})\)\}\^\{\(\\dfrac\{(.+?)\}\{(.+?)\}\)\}', lat)
            if searobj.group(2) == '1':
                lat = lat.replace(searobj.group(0), '\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}')
            else: 
                lat = lat.replace(searobj.group(0), '{\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}' + '}^{' + searobj.group(2) + '}')
        elif re.search(r'\{(\{\d+\.?\d* \\cdot 10\^\{\d+\}\}_\{ \})\}\^', lat) is not None:
            searobj = re.search(r'\{(\{\d+\.?\d* \\cdot 10\^\{\d+\}\}_\{ \})\}\^', lat)
            lat = lat.replace(searobj.group(0), '{(' + searobj.group(1) + ')}^')
        else:
            break
    lat = lat.replace('(', '\\left(').replace(')', '\\right)')
    return lat

def text_to_unit_latex(unit):
    """Обработка едениц измерения в latex строку"""
    unit = unit.replace('**', '^')
    unit = unit.replace('*', '\\cdot')
    if re.search(r'[а-яА-Я]+', unit) is not None:
        arr = re.findall(r'[а-яА-Я]+', unit)
        for k in arr:
            unit = unit.replace(k, '\\text{' + k + '}')
    return unit