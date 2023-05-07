import argparse
import logging
import os
import re
import sys
from datetime import datetime
from easytithe import easytithe
from breeze import breeze
from breeze import breeze


@property
def date(self):
    formatted_date = datetime.strptime(self._contribution['Date'], '%m/%d/%Y')
    return formatted_date.strftime('%Y-%m-%d')
