import threading
import sys
from PyQt5 import QtWidgets
from updateServer.HotUpdate import myfunction
import redis
import random
import importlib
from updateServer.HotUpdate.HotFixSample import Ui_MainWindow


def runFunction(self):
    version = self.fun.AllFunction().version
    self.textBrowser.append(('功能运行，当前版本为：' + version))
    for i in range(4):
        x = random.randint((- 454), 994)
        y = random.randint((- 245), 437)
        self.textBrowser.append(((((str(x) + '\tfunction version {}\t'.format(version)) + str(y)) + ' = ') + str(self.fun.AllFunction().second(x, y))))
