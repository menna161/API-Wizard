import os
import sys, getopt
import requests
import socket
import cryptography
import time
from cryptography.fernet import Fernet
from sys import platform
from urllib.parse import urlparse
from xml.dom import minidom
from termcolor import colored, cprint


def subscribe(URL, callbackURL):
    myheaders = {'User-Agent': 'Callstranger Vulnerability Checker', 'CALLBACK': (('<' + callbackURL) + '>'), 'NT': 'upnp:event', 'TIMEOUT': 'Second-300', 'Accept-Encoding': None, 'Accept': None, 'Connection': None}
    req = requests.request('SUBSCRIBE', URL, headers=myheaders)
    if (req.status_code == 200):
        print(colored((('Subscribe to ' + URL) + ' seems successfull'), 'green'))
        print(req.headers)
        print(req.text)
    else:
        print(colored(((('Subscribe to ' + URL) + ' failed with status code:') + str(req.status_code)), 'red'))
        print(req.headers)
        print(req.text)
