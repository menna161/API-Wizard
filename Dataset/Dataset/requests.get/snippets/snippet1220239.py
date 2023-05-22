import json
import os
from multiprocessing import Pool
from pathlib import Path
from signal import SIG_IGN, SIGINT, signal
from typing import Any, Callable, List, Tuple
import requests
from tqdm import tqdm
from yarl import URL


def _crawl(self, url: URL, save: bool=True) -> Any:
    try:
        data = requests.get(url).json()
    except json.JSONDecodeError as err:
        tqdm.write(f'JSON decode failure: {url}')
        return None
    if save:
        out_data = json.dumps(data, indent=4, sort_keys=True)
        out_data = out_data.replace(str(self._src_url), '')
        file = self._dest_dir.joinpath((url / 'index.json').path[1:])
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(out_data)
    return data
