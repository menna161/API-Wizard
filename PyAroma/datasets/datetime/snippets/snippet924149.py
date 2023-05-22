import logging
import random
import threading
from datetime import datetime
import numpy as np
from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from .utils import Indexer, create_sparse, timestamp_delta_generator


def generate_indexer(usr_dataset, usr_bm_tg, feature_begin, feature_end):
    logging.info('generating indexer ...')
    indexer = Indexer(['user', 'tag', 'bookmark'])
    min_time = 1e+30
    max_time = (- 1)
    for line in usr_dataset[1:]:
        line_items = line.split('\t')
        contact_timestamp = (float(line_items[2]) / 1000)
        min_time = min(min_time, contact_timestamp)
        max_time = max(max_time, contact_timestamp)
        if (feature_begin < contact_timestamp <= feature_end):
            indexer.index('user', line_items[0])
            indexer.index('user', line_items[1])
    for line in usr_bm_tg[1:]:
        line_items = line.split('\t')
        tag_timestamp = (float(line_items[3]) / 1000)
        if (feature_begin < tag_timestamp <= feature_end):
            indexer.index('user', line_items[0])
            indexer.index('bookmark', line_items[1])
            indexer.index('tag', line_items[2])
    with open('data/delicious/metadata.txt', 'w') as output:
        output.write('Nodes:\n')
        output.write('-----------------------------\n')
        output.write(('#Users: %d\n' % indexer.indices['user']))
        output.write(('#Tags: %d\n' % indexer.indices['tag']))
        output.write(('#Bookmarks: %d\n' % indexer.indices['bookmark']))
        output.write('\nEdges:\n')
        output.write('-----------------------------\n')
        output.write(('#Contact: %d\n' % len(usr_dataset)))
        output.write(('#Save : %d\n' % len(usr_bm_tg)))
        output.write(('#Attach: %d\n' % len(usr_bm_tg)))
        output.write('\nTime Span:\n')
        output.write('-----------------------------\n')
        output.write(('From: %s\n' % datetime.fromtimestamp(min_time)))
        output.write(('To: %s\n' % datetime.fromtimestamp(max_time)))
    return indexer
