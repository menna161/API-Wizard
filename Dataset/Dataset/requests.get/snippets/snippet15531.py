import os
import re
import time
import stat
import subprocess
import platform
import requests
from lxml import html
from zipfile import ZipFile
from urllib.parse import urlparse, urlunparse


def download_chromedriver() -> None:
    'Download released chromedriver'
    version = check_system_chrome_version()
    print(f'''Installed Chrome version: {version}
''')
    release = get_latest_release(version)
    print(f'''Available Chrome release: {release}
''')
    sys_platform = platform.system()
    if (sys_platform == 'Linux'):
        filename = 'chromedriver_linux64.zip'
    elif (sys_platform == 'Windows'):
        filename = 'chromedriver_win32.zip'
    else:
        filename = 'chromedriver_mac64.zip'
    uri = urlparse(f'https://chromedriver.storage.googleapis.com/{release}/')
    uri = uri._replace(path=(uri.path + filename))
    url = urlunparse(uri)
    executable = ('chromedriver.exe' if (sys_platform == 'Windows') else 'chromedriver')
    if has_chromedriver():
        src = executable
        dst = f'backup_{int(time.time())}_{executable}'
        os.rename(src, dst)
    print(f'''Downloading: {url}
''')
    reply = requests.get(url)
    assert (reply.status_code == 200)
    open(filename, 'wb').write(reply.content)
    print('Download complete.\n')
    with ZipFile(filename, 'r') as zip:
        print(f'''Extracting: {filename}
''')
        zip.printdir()
        zip.extractall()
    if (sys_platform != 'Windows'):
        os.chmod(executable, ((stat.S_IRWXU | stat.S_IRWXG) | stat.S_IROTH))
    os.remove(filename)
    print('\nDone!\n')
