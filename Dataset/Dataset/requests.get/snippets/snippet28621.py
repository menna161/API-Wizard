import shlex
import subprocess
import os
import zipfile
import shutil
import logging
import sys
import requests


def build_darknet(download_path, darknet_url, branch_name):
    '\n    Utility method to download and build darknet\n    :param download_path: Path to download darknet sources\n    :param branch_name: Branch of darknet used.\n    :return:\n    '
    import requests
    logging.info(('Temp Path: ' + download_path))
    logging.info('Downloading darknet')
    os.makedirs(download_path, exist_ok=True)
    response = requests.get(darknet_url)
    logging.info('Extracting darknet')
    with open(os.path.join(download_path, 'darknet.zip'), 'wb') as f:
        f.write(response.content)
    zip_ref = zipfile.ZipFile(os.path.join(download_path, 'darknet.zip'), 'r')
    zip_ref.extractall(download_path)
    zip_ref.close()
    os.remove(os.path.join(download_path, 'darknet.zip'))
    logging.info('Building darknet')
    build_ret = subprocess.Popen('make', shell=True, stdout=subprocess.PIPE, cwd=os.path.join(download_path, ('darknet-' + branch_name)))
    for line in iter(build_ret.stdout.readline, ''):
        if (len(line) != 0):
            logging.info(line.rstrip())
        else:
            break
    if (build_ret.wait() == 0):
        logging.info('Darknet building successful')
    else:
        return False
    return True
