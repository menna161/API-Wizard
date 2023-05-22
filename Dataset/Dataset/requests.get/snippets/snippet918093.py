import shutil
import tempfile
from urllib.request import urlopen
from nnunet.paths import network_training_output_dir
from subprocess import call
import requests
import http.client
import http.client
import argparse
import argparse
import argparse
import argparse


def download_and_install_from_url2(url):
    assert (network_training_output_dir is not None), 'Cannot install model because network_training_output_dir is not set (RESULTS_FOLDER missing as environment variable, see Installation instructions)'
    import http.client
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    with tempfile.NamedTemporaryFile() as f:
        fname = f.name
        print('Downloading pretrained model', url)
        r = requests.get(url)
        f.write(r.content)
        print('Download finished. Extracting...')
        install_model_from_zip_file(fname)
        print('Done')
