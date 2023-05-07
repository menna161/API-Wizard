import json
import sys
from tqdm import tqdm
from my.corenlp_interface import CoreNLPInterface


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if (start == (- 1)):
            return
        (yield start)
        start += len(sub)
