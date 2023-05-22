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


def confirmvulnerableservices(path, key):
    vulnerableservices = ''
    try:
        getservices = requests.request('PUT', path)
        vulnerableservices = getservices.text
        print(colored(('Successfully get services from server: ' + path), 'green'))
        print('')
        print('Encrypted vulnerable services:')
        print(vulnerableservices)
        print('')
        print('Decyripting vulnerable services with key:', key)
        f = Fernet(key)
        i = 1
        decryiptedvulnerableservices = []
        print(colored('\nVerified vulnerable services: ', 'red'))
        for line in vulnerableservices.splitlines():
            print(colored(((str(i) + ':\t') + f.decrypt(line.encode()).decode()), 'red'))
            decryiptedvulnerableservices.append(f.decrypt(line.encode()).decode())
            i = (i + 1)
        unverifiedservices = Diff(services, decryiptedvulnerableservices)
        print(colored('\nUnverified  services: ', 'yellow'))
        i = 1
        for unverifiedservice in unverifiedservices:
            print(colored(((str(i) + ':\t') + unverifiedservice), 'yellow'))
            i = (i + 1)
    except:
        print(colored('Could not get services from server', path, ' for vulnerability confirmation', 'red'))
