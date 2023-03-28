import os
import datetime
import logging
import inspect


def time_now_formate(self):
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')
