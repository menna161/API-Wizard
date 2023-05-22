import datetime
import time
import threading


def print_status(message: str=None, color: str='\x1b[92m', status: str='OK'):
    output = ((((((('[' + color) + ' ') + status) + ' ') + bcolors.ENDC) + '] ') + datetime.datetime.now().strftime('%d.%b %Y %H:%M:%S'))
    thread_name = threading.current_thread().name
    if (thread_name is not None):
        output += ((((' [' + bcolors.OKBLUE) + thread_name) + bcolors.ENDC) + ']')
    if (message is not None):
        output += (' ' + message)
    print(output)
