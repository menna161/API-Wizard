import argparse
import csv
import datetime
import json
import os
import sys
import xml.etree.ElementTree as ET


def display(message, verbose=False, exit_code=0):
    global show_time, show_verbose
    if show_time:
        now = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(now, '%Y/%m/%d %H:%M:%S')
        message = '{} {}'.format(timestamp, message)
    out = sys.stdout
    if (exit_code > 0):
        out = sys.stderr
    if (verbose and show_verbose):
        out.write((message.rstrip() + '\n'))
    elif (not verbose):
        out.write((message.rstrip() + '\n'))
    out.flush()
    if (exit_code > 0):
        sys.exit(exit_code)
