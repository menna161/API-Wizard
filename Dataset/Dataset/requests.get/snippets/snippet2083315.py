import requests
import argparse
import os, sys
import time
import hashlib
import json
from vtscan import __title__, __description__, __version__
from colorama import Fore, Style


def scan(hash, log_output=False, is_file=False):
    if (cfg['api_key'] == ''):
        raise Exception('api key is missing')
        return
    (params, files) = ({}, {})
    if is_file:
        params = {'apikey': cfg['api_key']}
        files = {'file': (os.path.split(hash)[1], open(hash, 'rb'))}
        print('Uploading file...')
        url = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', params=params, files=files)
        json_response = url.json()
        if ('sha256' in json_response.keys()):
            print("Performing scan. If it doesn't work, restart the program again")
            scan(json_response.get('sha256'), log_output, False)
        return
    else:
        params = {'apikey': cfg['api_key'], 'resource': hash}
        url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    json_response = url.json()
    if log_output:
        ss = json.dumps(json_response, indent=4)
        open('output.json', 'w').write(ss)
        print('Logged output to output.json')
    response = int(json_response.get('response_code'))
    if (response == 0):
        print(((Fore.YELLOW + 'Not found in VT Database') + Fore.RESET))
        return 'not_found'
    elif (response == 1):
        print('Found in VT Database')
        print('permalink: ', json_response.get('permalink'))
        positives = int(json_response.get('positives'))
        total = int(json_response.get('total'))
        print(('Number of positives: %d (out of %d scanners applied)' % (positives, total)))
        print(('verbose_msg: %s' % json_response.get('verbose_msg')))
        if (positives == 0):
            print((((Fore.GREEN + hash) + ' is not malicious') + Fore.RESET))
        else:
            print((((Fore.RED + hash) + ' is malicious') + Fore.RESET))
            print('')
        scans = json_response.get('scans')
        for key in scans:
            if scans[key]['detected']:
                print((Fore.RED + key), 'v', scans[key]['version'], ': ', str(scans[key]['result']), Fore.RESET)
    else:
        print((hash + ' could not be searched. Please try again later.'))
    print('')
