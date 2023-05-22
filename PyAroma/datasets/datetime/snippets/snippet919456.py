import requests
import gzip
from datetime import datetime
import pendulum
from zipfile import ZipFile
import base64
import tldextract
from pathlib import Path
from StringIO import BytesIO
from io import BytesIO


def latest(self):
    latest_list = []
    past = datetime.strftime(self.date, '%Y-%m-%d')
    filename = '{}.zip'.format(past)
    encoded_filename = base64.b64encode(filename.encode('utf-8'))
    response = requests.get('{}/{}/nrd'.format('https://whoisds.com//whois-database/newly-registered-domains', encoded_filename.decode('ascii')))
    try:
        with BytesIO(response.content) as zip_file:
            with ZipFile(zip_file) as zip_file:
                for zip_info in zip_file.infolist():
                    with zip_file.open(zip_info) as ffile:
                        for line in ffile.readlines():
                            latest_list.append(line.decode('utf-8', errors='ignore').strip())
    except Exception as e:
        print('Unable to Unzip WhoisDs zone data -- date is likely out of range.  {}'.format(e))
        print(response.content)
    return latest_list
