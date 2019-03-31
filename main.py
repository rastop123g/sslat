import re
import sys, os
import logging as log
from modules import state_app, view
from modules.block_processing import BlockProcessing

log.basicConfig(filename="message.log", filemode="w", level=log.INFO)

state = state_app.state
state['instance'] = state

dir_path = os.path.dirname(os.path.realpath(__file__))
cwd_path = os.getcwd()
new_path = cwd_path + '/' + sys.argv[2] + '/'

state['dir_path'], state['cwd_path'], state['new_path'] = dir_path, cwd_path, new_path

if not os.path.exists(new_path):
    os.makedirs(new_path)

with open(sys.argv[1], 'r') as file:
    block = file.read().split("\n\n")

try:
    with open(sys.argv[3], 'r') as file:
        state['input'] = file.read().split('\n')
except IndexError:
    state['input'] = []

try:
    views = re.search(r'view{(.+)}', block[len(block) - 1].replace('\n', '').replace('    ', '').replace('  ', '')).group(1)
    view.initview_of_sec(views)
except AttributeError:
    pass

result_text = ''
for s in block:
    log.info("block > " + s)
    try:
        result_text += BlockProcessing(s)
    except TypeError:
        pass
log.info('state > ' + str(state))
with open(dir_path + '/template.tex', 'r') as file:
    res = file.read()
with open(new_path + 'out.tex', 'w') as file:
    file.write(res.replace('$$content$$', result_text))
print('Mission complete!')