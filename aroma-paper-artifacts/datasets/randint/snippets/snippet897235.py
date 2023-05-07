import math
import numpy as np
import torch
from typing import Dict, List, Tuple
from fairseq.data import FairseqDataset, data_utils
from fairseq.data import Dictionary
from fairseq.data.legacy.block_pair_dataset import BlockPairDataset
from fairseq.data.token_block_dataset import TokenBlockDataset
from fairseq.data.concat_dataset import ConcatDataset


def _mask_block(self, sentence: np.ndarray, mask_idx: int, pad_idx: int, dictionary_token_range: Tuple):
    "\n        Mask tokens for Masked Language Model training\n        Samples mask_ratio tokens that will be predicted by LM.\n\n        Note:This function may not be efficient enough since we had multiple\n        conversions between np and torch, we can replace them with torch\n        operators later.\n\n        Args:\n            sentence: 1d tensor to be masked\n            mask_idx: index to use for masking the sentence\n            pad_idx: index to use for masking the target for tokens we aren't\n                predicting\n            dictionary_token_range: range of indices in dictionary which can\n                be used for random word replacement\n                (e.g. without special characters)\n        Return:\n            masked_sent: masked sentence\n            target: target with words which we are not predicting replaced\n                by pad_idx\n        "
    masked_sent = np.copy(sentence)
    sent_length = len(sentence)
    mask_num = math.ceil((sent_length * self.masking_ratio))
    mask = np.random.choice(sent_length, mask_num, replace=False)
    target = np.copy(sentence)
    for i in range(sent_length):
        if (i in mask):
            rand = np.random.random()
            if (rand < self.masking_prob):
                masked_sent[i] = mask_idx
            elif (rand < (self.masking_prob + self.random_token_prob)):
                masked_sent[i] = np.random.randint(dictionary_token_range[0], dictionary_token_range[1])
        else:
            target[i] = pad_idx
    return (masked_sent, target)
