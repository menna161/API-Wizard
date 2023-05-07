import pandas as pd
import numpy as np
from utils import pkl_utils
from optparse import OptionParser
import config
from utils.data_utils import load_dict_from_txt


def group(input_data, output_data, if_sample=False):
    df = pd.read_csv(input_data, sep='\t', names=['r', 'e1', 'x1', 'y1', 'e2', 'x2', 'y2', 's'])
    grouped = df.groupby(['r', 'e1', 'e2'])
    words = []
    positions = []
    heads = []
    tails = []
    labels = []
    cnt = 0
    for (name, group) in grouped:
        if (if_sample and (cnt > 10000)):
            break
        cnt += 1
        if ((cnt % 1000) == 0):
            print(cnt)
        group = group.reset_index(drop=True)
        label = name[0]
        head = name[1]
        tail = name[2]
        size = group.shape[0]
        tmp_words = []
        tmp_positions = []
        for i in range(size):
            tmp_words.append(group.s[i])
            tmp_positions.append([group.x1[i], group.y1[i], group.x2[i], group.y2[i]])
        if (size < config.BAG_SIZE):
            tmp = size
            ans_words = tmp_words[:]
            ans_positions = tmp_positions[:]
            while ((tmp + size) < config.BAG_SIZE):
                tmp += size
                ans_words += tmp_words
                ans_positions += tmp_positions
            ans_words += tmp_words[:(config.BAG_SIZE - tmp)]
            ans_positions += tmp_positions[:(config.BAG_SIZE - tmp)]
            words.append(ans_words)
            positions.append(ans_positions)
            heads.append(head)
            tails.append(tail)
            labels.append(label)
        else:
            tmp = 0
            while ((tmp + config.BAG_SIZE) < size):
                words.append(tmp_words[tmp:(tmp + config.BAG_SIZE)])
                positions.append(tmp_positions[tmp:(tmp + config.BAG_SIZE)])
                heads.append(head)
                tails.append(tail)
                labels.append(label)
                tmp += config.BAG_SIZE
            words.append(tmp_words[(- config.BAG_SIZE):])
            positions.append(tmp_positions[(- config.BAG_SIZE):])
            heads.append(head)
            tails.append(tail)
            labels.append(label)
    heads = np.array(heads)
    tails = np.array(tails)
    labels = np.array(labels)
    pkl_utils._save(output_data, (words, positions, heads, tails, labels))
