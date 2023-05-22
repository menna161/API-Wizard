import copy
import csv
import datetime
import json
import logging
import os
import time
from typing import Dict
import git


def close(self, successful: bool=True) -> None:
    self.metadata['date_end'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    self.metadata['successful'] = successful
    self._save_metadata()
    for f in [self._logfile, self._fieldfile]:
        f.close()
