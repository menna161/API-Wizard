import datetime
from tkinter import Label, Toplevel
import os
import visu, poly, vec


def __init__(self, date, score=None):
    if (type(date) == str):
        self.read_from_line(date)
    elif ((type(date) is datetime.datetime) and (type(score) is int)):
        self.date = date
        self.score = score
    else:
        raise ValueError(((('wrong parameters: ' + str(date)) + ', ') + str(score)))
