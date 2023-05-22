import requests
import argparse
import shutil
import os
import re
import json


def download_file(url, dest):
    r = requests.get(url, headers=headers)
    with open(dest, 'wb') as f:
        f.write(r.content)
