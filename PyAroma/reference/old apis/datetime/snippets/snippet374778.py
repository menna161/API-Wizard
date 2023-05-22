import argparse
import datetime
import re
import sys


def display(message, verbose=False, exit=0):
    global show_time, show_verbose
    if show_time:
        now = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(now, '%Y/%m/%d %H:%M:%S')
        message = '{} {}'.format(timestamp, message)
    out = sys.stdout
    if (exit > 0):
        out = sys.stderr
    if (verbose and show_verbose):
        out.write((message.rstrip() + '\n'))
    elif (not verbose):
        out.write((message.rstrip() + '\n'))
    if (exit > 0):
        sys.exit(exit)
