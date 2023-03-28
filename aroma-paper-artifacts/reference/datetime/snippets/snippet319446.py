from subprocess import check_output
from pathlib import Path
import json
import uuid
import boto3
import pprint
import tarfile
import datetime


def compressApkIndex(path):
    print(f'Compressing {path}')
    tarpath = '/tmp/{}-{}'.format(uuid.uuid4(), 'APKINDEX.unsigned.tar.gz')
    despath = '/tmp/{}-{}'.format(uuid.uuid4(), 'APKINDEX.unsigned.tar.gz')
    description = open(despath, 'w')
    description.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    description.close()
    tarpath = '/tmp/{}-{}'.format(uuid.uuid4(), 'APKINDEX.unsigned.tar.gz')
    tar = tarfile.open(tarpath, 'w:gz')
    tar.add(path, arcname='APKINDEX')
    tar.add(despath, arcname='DESCRIPTION')
    tar.close()
    return tarpath
