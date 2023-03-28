from datetime import datetime
import backtrader as bt
from termcolor import colored
from config import DEVELOPMENT, COIN_TARGET, COIN_REFER, ENV, PRODUCTION, DEBUG
from utils import send_telegram_message


def log(self, txt, send_telegram=False, color=None):
    if (not DEBUG):
        return
    value = datetime.now()
    if (len(self) > 0):
        value = self.data0.datetime.datetime()
    if color:
        txt = colored(txt, color)
    print(('[%s] %s' % (value.strftime('%d-%m-%y %H:%M'), txt)))
    if send_telegram:
        send_telegram_message(txt)
