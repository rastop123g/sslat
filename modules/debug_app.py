from . import state_app

state = state_app.state

def app_end_stdin(va):
    """Добавление значения в stdin.txt"""
    global state
    file = open(state['new_path'] + 'stdin.txt', 'a')
    file.write(str(va) + '\n')
    file.close()