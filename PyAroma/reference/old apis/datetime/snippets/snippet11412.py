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


def get_last_logon_date(self):
    if ((self.last_logon != '') and (self.last_logon != '0') and (int(self.last_logon) != 0)):
        last_logon_int = int(self.last_logon)
        epoch_time = ((last_logon_int / 10000000) - 11644473600)
        last_logon_time = datetime.datetime.fromtimestamp(epoch_time)
        return last_logon_time.strftime('%m-%d-%y %H:%M:%S')
    return self.last_logon
