import requests
import pkg_resources


@staticmethod
def latest():
    res = requests.get(Version.PYPI_URL).json()
    return res['info']['version']
