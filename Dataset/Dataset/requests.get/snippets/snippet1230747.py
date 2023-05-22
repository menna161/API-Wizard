import requests
from torch import Tensor, device
from typing import Tuple, List
from tqdm import tqdm
import sys
import importlib


def http_get(url, path):
    with open(path, 'wb') as file_binary:
        req = requests.get(url, stream=True)
        if (req.status_code != 200):
            print('Exception when trying to download {}. Response {}'.format(url, req.status_code), file=sys.stderr)
            req.raise_for_status()
        content_length = req.headers.get('Content-Length')
        total = (int(content_length) if (content_length is not None) else None)
        progress = tqdm(unit='B', total=total, unit_scale=True)
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                progress.update(len(chunk))
                file_binary.write(chunk)
    progress.close()
