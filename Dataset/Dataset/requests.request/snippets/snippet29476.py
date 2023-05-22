import os
import sys, getopt
import upnpy
import requests
import uuid
import socket
import cryptography
import time
from cryptography.fernet import Fernet
from sys import platform
from termcolor import colored, cprint


def subscribe(URL, callbackURL):
    myheaders = {'User-Agent': 'Callstranger Vulnerability Checker', 'CALLBACK': (('<' + callbackURL) + '>'), 'NT': 'upnp:event', 'TIMEOUT': 'Second-300'}
    req = requests.request('SUBSCRIBE', URL, headers=myheaders)
    if (req.status_code == 200):
        print(colored((('Subscribe to ' + URL) + ' seems successfull'), 'green'))
        print(req.headers)
        print(req.text)
    else:
        print(colored(((('Subscribe to ' + URL) + ' failed with status code:') + str(req.status_code)), 'red'))
        print(req.headers)
        print(req.text)
