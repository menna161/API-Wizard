from datetime import datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QFrame
import numpy as np
import time
from threading import Timer, Lock
import pytz
from tzlocal import get_localzone
from random import randint
import TradingBotConfig as theConfig
from UIWidgets import ButtonHoverStart
from UIWidgets import ButtonHoverStart
from UIWidgets import ButtonHoverPause
from UIWidgets import ButtonHoverSettings
from UIWidgets import ButtonHoverDonation
from UIWidgets import ButtonHoverInfo
from UIWidgets import RadioHoverSimulation
from UIWidgets import RadioHoverTrading
from UIWidgets import SliderHoverRiskLevel
from UIWidgets import SliderHoverSensitivityLevel
from UIWidgets import LabelClickable
from UISettings import UISettings
from UIDonation import UIDonation
from UIInfo import UIInfo


def tickStrings(self, values, scale, spacing):
    try:
        if (theConfig.CONFIG_INPUT_MODE_IS_REAL_MARKET == False):
            valuesToReturn = [datetime.fromtimestamp(value, self.localTimezone).strftime('%H:%M:%S\n%b%d') for value in values]
        else:
            valuesToReturn = [datetime.fromtimestamp(value, self.localTimezone).strftime('%H:%M:%S') for value in values]
    except BaseException as e:
        print(('UIGR - Exception in tick strings: %s' % str(e)))
    return valuesToReturn
