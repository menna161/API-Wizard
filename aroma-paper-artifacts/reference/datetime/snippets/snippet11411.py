import traceback
import ldap3
from ldap3.utils.log import set_library_log_detail_level, OFF, ERROR, BASIC, PROTOCOL, NETWORK, EXTENDED
import datetime
from time import gmtime
import logging
import argparse
from getpass import getpass
import argcomplete
import ssl
from openpyxl import Workbook, load_workbook
import csv
from os.path import isfile


def get_password_last_set_date(self):
    if ((self.password_last_set != '') and (self.password_last_set != '0') and (int(self.password_last_set) != 0)):
        last_set_int = int(self.password_last_set)
        epoch_time = ((last_set_int / 10000000) - 11644473600)
        last_set_time = datetime.datetime.fromtimestamp(epoch_time)
        return last_set_time.strftime('%m-%d-%y %H:%M:%S')
    return self.password_last_set
