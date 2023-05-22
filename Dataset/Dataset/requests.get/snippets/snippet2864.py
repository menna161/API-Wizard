import os
import json
import shutil
import urllib3
from hashlib import md5
from socket import gethostbyname
from argparse import ArgumentParser
from xml.etree import ElementTree as eTree
from datetime import datetime, timedelta
import sqlite3
import requests


def query_xmlapi(url, sessionkey):
    '\n    Making HTTP(s) request to HP MSA XML API.\n\n    :param url: URL to make GET request.\n    :type url: str\n    :param sessionkey: Session key to authorize.\n    :type sessionkey: Union[str, None]\n    :return: Tuple with return code, return description and etree object <xml.etree.ElementTree.Element>.\n    :rtype: tuple\n    '
    ca_file = '/etc/pki/tls/certs/ca-bundle.crt'
    try:
        timeout = (3, 10)
        full_url = (('https://' + url) if USE_SSL else ('http://' + url))
        headers = ({'sessionKey': sessionkey} if (API_VERSION == 2) else {'Cookie': 'wbiusername={}; wbisessionkey={}'.format(MSA_USERNAME, sessionkey)})
        if USE_SSL:
            if VERIFY_SSL:
                response = requests.get(full_url, headers=headers, verify=ca_file, timeout=timeout)
            else:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(full_url, headers=headers, verify=False, timeout=timeout)
        else:
            response = requests.get(full_url, headers=headers, timeout=timeout)
    except requests.exceptions.SSLError:
        raise SystemExit('ERROR: Cannot verify storage SSL Certificate.')
    except requests.exceptions.ConnectTimeout:
        raise SystemExit('ERROR: Timeout occurred!')
    except requests.exceptions.ConnectionError as e:
        raise SystemExit('ERROR: Cannot connect to storage {}.'.format(e))
    try:
        if ((SAVE_XML is not None) and ('login' not in url)):
            try:
                with open(SAVE_XML[0], 'w') as xml_file:
                    xml_file.write(response.text)
            except PermissionError:
                raise SystemExit('ERROR: Cannot save XML file to "{}"'.format(args.savexml))
        response_xml = eTree.fromstring(response.content)
        return_code = response_xml.find("./OBJECT[@name='status']/PROPERTY[@name='return-code']").text
        return_response = response_xml.find("./OBJECT[@name='status']/PROPERTY[@name='response']").text
        return (return_code, return_response, response_xml)
    except (ValueError, AttributeError) as e:
        raise SystemExit('ERROR: Cannot parse XML. {}'.format(e))
