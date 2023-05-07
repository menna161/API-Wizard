from __future__ import print_function
import sys
import os
import numpy as np
import hashlib
import random
import preprocess


def get_text_id(self, hashid, text, idtag='T'):
    hash_obj = hashlib.sha1(text.encode('utf8'))
    hex_dig = hash_obj.hexdigest()
    if (hex_dig in hashid):
        return hashid[hex_dig]
    else:
        tid = (idtag + str(len(hashid)))
        hashid[hex_dig] = tid
        return tid
