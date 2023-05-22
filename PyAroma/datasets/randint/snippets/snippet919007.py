import os
import sys
import time
import random
from PyQt5 import QtWidgets
from typing.ui import Ui_Form
from typing.crawl import crawl_main


def __init__(self):
    super(MyForm, self).__init__()
    self.setupUi(self)
    with open('text.txt', 'r', encoding='utf-8') as f:
        self.text_list = f.readlines()
    self.text_list = [i.strip() for i in self.text_list]
    self.text = self.text_list[random.randint(0, len(self.text_list))]
    self.used_list = [self.text]
    self.textBrowser.setText(self.text)
    self.hide_label()
    self.start_time = time.time()
    self.submit_btn.clicked.connect(self.click)
    self.next_btn.clicked.connect(self.next)
    self.submit_btn.setShortcut('ctrl+e')
    self.next_btn.setShortcut('ctrl+n')
