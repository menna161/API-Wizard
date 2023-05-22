import os
import zipfile
from datetime import datetime as dt
from typing import Dict, List, Tuple
import pandas as pd
import requests
from stable_baselines.common.base_class import ActorCriticRLModel
from . import RecoEnv


def download_data() -> None:
    '\n    Helper function to download MovieLens 100k data set and save to the `ml-100k`\n    directory within the `/data` folder.\n    '
    start_time = dt.now()
    print('Starting data download. Saving to {}'.format(CWD))
    if (not os.path.exists(CWD)):
        print('download_data() --> Making ./data/* directory...')
        os.mkdir(CWD)
    if (not os.path.exists(os.path.join(CWD, 'ml-100k'))):
        print('download_data() --> Making ./data/ml-100k/* directory...')
        os.mkdir(os.path.join(CWD, 'ml-100k'))
        url = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
        r = requests.get(url)
        if (r.status_code != 200):
            print('download_data() --> Error: could not download ml100k')
        zip_file_path = os.path.join(CWD, 'ml-100k.zip')
        with open(zip_file_path, 'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(zip_file_path, 'r') as f_zip:
            f_zip.extractall(path=CWD)
        elapsed = (dt.now() - start_time).seconds
        print('download_data() --> completed in {} seconds.'.format(elapsed))
    else:
        print('Using cached data located at {}.'.format(os.path.join(CWD, 'ml-100k')))
