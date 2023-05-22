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


def getsession(path):
    session = ''
    try:
        getses = requests.request('PUT', path)
        session = getses.text
        print(colored(('Successfully get session:' + session), 'green'))
    except:
        print(colored('Could not  contact server', path, ' for vulnerability confirmation', 'red'))
    return session
