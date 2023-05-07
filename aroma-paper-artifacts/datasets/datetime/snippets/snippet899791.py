import os
import datetime


def write(text, no_timestamp=False):
    'Main logging funcion. Called if write function was set\n    \n    Parameters\n    ----------\n    text : str\n        debug text to print\n    no_timestamp=False : bool\n        a flag to disable timestamp printing when required\n    '
    global _LOG_FILE_POINTER
    global _LOG_ENABLED
    if (_LOG_ENABLED and (_LOG_FILE_POINTER is not None)):
        if no_timestamp:
            final_text = '{}\n'.format(text)
        else:
            final_text = '{} - {}\n'.format(datetime.datetime.now(), text)
        _LOG_FILE_POINTER.write(final_text)
