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


def geturl(path):
    document = ''
    try:
        getses = requests.request('GET', path)
        document = getses.text
        print(colored(('Successfully get device document: ' + path), 'green'))
    except:
        print(colored('Could not  contact server', path, 'red'))
    return document
