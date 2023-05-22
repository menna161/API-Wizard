import tkinter as TK
import types
import math
import time
import inspect
import sys
from os.path import isfile, split, join
from copy import deepcopy
from tkinter import simpledialog
import re
import re


def _rescale(self, xscalefactor, yscalefactor):
    items = self.cv.find_all()
    for item in items:
        coordinates = list(self.cv.coords(item))
        newcoordlist = []
        while coordinates:
            (x, y) = coordinates[:2]
            newcoordlist.append((x * xscalefactor))
            newcoordlist.append((y * yscalefactor))
            coordinates = coordinates[2:]
        self.cv.coords(item, *newcoordlist)
