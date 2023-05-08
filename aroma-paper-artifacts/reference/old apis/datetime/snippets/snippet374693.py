import argparse
import datetime
import os
import re
import sys
import xml.etree.ElementTree as ET


def unixtime(date):
    epoch = datetime.datetime(1970, 1, 1)
    return (date - epoch).total_seconds()
