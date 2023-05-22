import random
import requests


@staticmethod
def getHomePage():
    random.shuffle(urls)
    for i in urls:
        r = requests.get((i + 'news'))
        try:
            return r.json()
        except ValueError:
            continue
