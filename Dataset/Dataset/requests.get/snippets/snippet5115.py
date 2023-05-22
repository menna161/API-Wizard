import argparse
import logging as log
import os
import socket
import CloudFlare
import requests
import tldextract
from CloudFlare.exceptions import CloudFlareAPIError
from .__about__ import __version__


def get_public_ip():
    log.debug('Getting public IP from an external service')
    return requests.get('https://ident.me').text
