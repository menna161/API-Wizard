from pprint import pprint
import os, yaml, json, sys, argparse, logging, re, datetime
import pynetbox
from netaddr import *

if (__name__ == '__main__'):
    cache_file = ('/tmp/ansible_nb_%s.json' % os.getlogin())
    parser = argparse.ArgumentParser(add_help=True, description='A simple dynamic inventory for Ansible from Netbox')
    parser.add_argument('--list', action='store_true', default=False, dest='inventory_mode', help='Print JSON output')
    parser.add_argument('--flushcache', action='store_true', default=False, dest='flush_cache', help='Overwrite cache file')
    if parser.parse_args().flush_cache:
        cache_inventory(cache_file)
    elif parser.parse_args().inventory_mode:
        if os.path.isfile(cache_file):
            mtime = modification_date(cache_file)
            to_date = (datetime.datetime.now() - datetime.timedelta(hours=3))
            if (mtime >= to_date):
                load_cache(cache_file)
                exit(0)
        cache_inventory(cache_file)
    else:
        parser.print_help()
