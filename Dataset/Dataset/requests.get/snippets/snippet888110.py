import re
import requests


def get_package_information(index_url, package_name):
    index_url = index_url.rstrip('/')
    response = requests.get(('%s/%s/json' % (index_url, package_name)))
    if (response.status_code == 200):
        return response.json()
