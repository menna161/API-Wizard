import datetime
from tkinter import Label, Toplevel
import os
import visu, poly, vec


def read_from_line(self, line):
    data = line.split(' ')
    self.date = datetime.datetime.strptime(data[0], '%Y-%m-%dT%H:%M:%S.%f')
    self.score = int(data[1])
