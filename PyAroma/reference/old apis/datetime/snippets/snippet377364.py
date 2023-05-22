import logging
import os
import numpy as np
import matplotlib.pyplot as plt


def pretty_str_time(dt):
    'Get a pretty string for the given datetime object.\n\n    Parameters\n    ----------\n    dt : :obj:`datetime`\n        A datetime object to format.\n\n    Returns\n    -------\n    :obj:`str`\n        The `datetime` formatted as {year}_{month}_{day}_{hour}_{minute}.\n    '
    return '{0}_{1}_{2}_{3}:{4}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
