import os
import sys
import time
import random
from PyQt5 import QtWidgets
from typing.ui import Ui_Form
from typing.crawl import crawl_main


def next(self):
    while 1:
        text = self.text_list[random.randint(0, len(self.text_list))]
        if (text not in self.used_list):
            self.used_list.append(text)
            self.text = text
            self.textBrowser.setText(text)
            self.textEdit.clear()
            self.hide_label()
            self.start_time = time.time()
            break
