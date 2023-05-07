import os
from datetime import datetime


def __init__(self, use=True, gui=False):
    self.dst = None
    self.use = use
    self.gui = gui
    self.items = []
    self._print = print
    self.add('PDF Watermarker', datetime.now().strftime('%Y-%m-%d %H:%M'))
