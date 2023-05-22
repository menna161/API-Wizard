import tarfile
import os
import requests
from . import pfpascal
from . import pfwillow
from . import caltech
from . import spair


def download_from_google(token_id, filename):
    'Download desired filename from Google drive'
    print(('Downloading %s ...' % os.path.basename(filename)))
    url = 'https://docs.google.com/uc?export=download'
    destination = (filename + '.tar.gz')
    session = requests.Session()
    response = session.get(url, params={'id': token_id, 'confirm': 't'}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': token_id, 'confirm': token}
        response = session.get(url, params=params, stream=True)
    save_response_content(response, destination)
    file = tarfile.open(destination, 'r:gz')
    print(('Extracting %s ...' % destination))
    file.extractall(filename)
    file.close()
    os.remove(destination)
    os.rename(filename, (filename + '_tmp'))
    os.rename(os.path.join((filename + '_tmp'), os.path.basename(filename)), filename)
    os.rmdir((filename + '_tmp'))
