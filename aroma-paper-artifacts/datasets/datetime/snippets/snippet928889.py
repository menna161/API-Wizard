import sys
import time
import argparse
import telnetlib
import serial
from collections import deque


def get_time(self):
    t = str(self.eval('pyb.RTC().datetime()'), encoding='utf8')[1:(- 1)].split(', ')
    return (((int(t[4]) * 3600) + (int(t[5]) * 60)) + int(t[6]))
