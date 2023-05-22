from collections import OrderedDict, Counter, Iterable, defaultdict
from dataclasses import dataclass, field
from warnings import warn
import json
import regex as re
from unidecode import unidecode
import time
import requests
import shelve
import xmltodict
from elasticsearch import ConflictError
from joblib import Parallel, delayed
from pathlib import Path
import diskcache as dc
from axcell import config
from axcell.data.elastic import Reference2, ID_LIMIT


def _post(self, data):
    tries = 0
    while (tries < self.max_tries):
        with requests.Session() as s:
            r = s.post(f'http://{self.host}:{self.port}/api/processCitation', data=data, headers={'Connection': 'close'})
        if (r.status_code in [200, 204]):
            return r.content.decode('utf-8')
        if (r.status_code != 503):
            raise RuntimeError(f'''{r.status_code} {r.reason}
{r.content}''')
        tries += 1
        if (tries < self.max_tries):
            time.sleep(self.retry_wait)
    raise ConnectionRefusedError(r.reason)
