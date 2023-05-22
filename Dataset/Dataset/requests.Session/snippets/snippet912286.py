import pdb
import os
from functools import partial
from urllib.request import urlretrieve
import requests
from tqdm import tqdm
from torch.utils.data.dataloader import DataLoader
from torch.utils.data.sampler import BatchSampler, RandomSampler, SequentialSampler
from data.sampler import SequenceLengthSampler


def download_from_google_drive(filepath, url):
    '\n    Downloads a file from Google Drive.\n\n    Apparently Google Drive may issue a warning about scanning for viruses and require confirmation\n    to continue the download.\n    '
    confirmation_token = None
    session = requests.Session()
    response = session.get(url, stream=True)
    for (key, value) in response.cookies.items():
        if key.startswith('download_warning'):
            confirmation_token = value
    if confirmation_token:
        url = ((url + '&confirm=') + confirmation_token)
    response = session.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = (16 * 1024)
    filename = os.path.basename(filepath)
    with open(filepath, 'wb') as file:
        with DownloadProgressBar(filename) as progress:
            blocks = iter((file.write(block) for block in response.iter_content(block_size) if block))
            for (i, block) in enumerate(blocks):
                progress.update_to(i, block_size, total_size)
    return filepath
