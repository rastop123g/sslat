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