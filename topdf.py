import sys
import subprocess
import re

out_lt = str(subprocess.check_output(['xelatex', sys.argv[1]]))
arr_line = re.findall(r'Overfull .+? line (\d+)', out_lt)
f = open(sys.argv[1], 'r')
file_str_arr = f.read().split('\n')
f.close()
for i in arr_line:
    a_s = file_str_arr[int(i)-1].split('=')
    s = a_s[0] + '=' + a_s[1] + '=$$\n$$=' + a_s[2] + '=' + a_s[3]
    file_str_arr[int(i)-1] = s
final_s = ''
for j, k in enumerate(file_str_arr):
    if j is not len(file_str_arr) - 1: 
        final_s = final_s + k + '\n'
    else:
        final_s = final_s + k
f = open(sys.argv[1], 'w')
f.write(final_s)
f.close()
out_lt = str(subprocess.check_output(['xelatex', sys.argv[1]]))
del out_lt
