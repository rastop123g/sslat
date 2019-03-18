import re

def initview_of_sec(vsec, state):
    arr = vsec.split(',')
    for item in arr:
        name = item.split('=')[0].strip()
        elview = item.split('=')[1].strip().replace('"', '')
        state[name] = {
            'view' : elview,
            'value' : [0]
        }

def view(name):
    searchobj = re.search(r'([a-zA-Zа-яА-Я0-9ёЁ]+)_?([a-zA-Zа-яА-Я0-9ёЁ]*)_?([a-zA-Zа-яА-Я0-9ёЁ]*)', name)
    result = '\\text{' + searchobj.group(1) + '}'
    if searchobj.group(3):
        if searchobj.group(3) == 'l':
            result +=  '^{\\prime}'
        elif searchobj.group(3) == 'll':
            result +=  '^{\\prime\\prime}'
        else:
            result +=  '^\\text{' + searchobj.group(3) + '}'
    if searchobj.group(2):
        result += '_\\text{' + searchobj.group(2) + '}'
    #print(result)
    return '{' + result + '}'

def exptolatex(exp, tmpdict):
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
            tmpdict['exp' + str(i)] = '{' + onefr + '}' + '^' + '{' + twofr + '}'
            exp = exp.replace(rsobj.group(1) + '^' + rsobj.group(2), 'exp' + str(i))
            i += 1
        elif re.search(r'sqrtexp\d+', exp) is not None: #корень
            rsobj = re.search(r'(sqrt)(exp\d+)', exp)
            tmpdict['exp' + str(i)] = '\\sqrt{' + tmpdict[rsobj.group(2)][1:-1] + '}'
            exp = exp.replace(rsobj.group(0), 'exp' + str(i))
            i += 1
        elif re.search(r'lnexp\d+', exp) is not None: #ln
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

def fix(lat):
    while True:
        if re.search(r'\{\(\\frac\{.+?\}\{.+?\}\)\}\^\{\(\\frac\{.+?\}\{.+?\}\)\}', lat) is not None:
            searobj = re.search(r'\{\((\\frac\{.+?\}\{.+?\})\)\}\^\{\(\\frac\{(.+?)\}\{(.+?)\}\)\}', lat)
            if searobj.group(2) == '1':
                lat = lat.replace(searobj.group(0), '\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}')
            else: 
                lat = lat.replace(searobj.group(0), '{\\sqrt[' + searobj.group(3) + ']{' + searobj.group(1) + '}' + '}^{' + searobj.group(2) + '}')
        #elif re.search(r'\{\(.+\)\}\^\{\((?:-|)\d+\.?\d*\)\}', lat) is not None:
        #    searobj = re.search(r'\{\(.+\)\}\^\{\(((?:-|)\d+\.?\d*)\)\}', lat)
        #    lat = lat.replace(searobj.group(0), searobj.group(0).replace('(' + searobj.group(1) + ')', searobj.group(1)))
        elif re.search(r'\{(\{\d+\.\d* \\cdot 10\^\{\d+\}\})\}\^', lat) is not None:
            searobj = re.search(r'\{(\{\d+\.\d* \\cdot 10\^\{\d+\}\})\}\^', lat)
            lat = lat.replace(searobj.group(0), '{(' + searobj.group(1) + ')}^')
        else:
            break
    lat = lat.replace('(', '\\left(').replace(')', '\\right)')
    return lat