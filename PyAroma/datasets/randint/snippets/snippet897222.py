import math
import numpy as np
import torch
from fairseq.data import FairseqDataset


def _generate_sentence_pair(self, doc, doc_id, max_num_tokens, sizes):
    '\n        Go through a single document and genrate sentence paris from it\n        '
    current_chunk = []
    current_length = 0
    curr = 0
    target_seq_length = max_num_tokens
    if (np.random.random() < self.short_seq_prob):
        target_seq_length = np.random.randint(2, max_num_tokens)
    while (curr < len(doc)):
        sent_id = doc[curr]
        current_chunk.append(sent_id)
        current_length = sum(sizes[current_chunk])
        if ((curr == (len(doc) - 1)) or (current_length >= target_seq_length)):
            a_end = 1
            if (len(current_chunk) > 2):
                a_end = np.random.randint(1, (len(current_chunk) - 1))
            sent_a = current_chunk[:a_end]
            len_a = sum(sizes[sent_a])
            next_sent_label = (1 if ((np.random.rand() > 0.5) and (len(current_chunk) != 1)) else 0)
            if (not next_sent_label):
                target_b_length = (target_seq_length - len_a)
                rand_doc_id = self._skip_sampling(len(self.block_indices), [doc_id])
                random_doc = self.block_indices[rand_doc_id]
                random_start = np.random.randint(0, len(random_doc))
                sent_b = []
                len_b = 0
                for j in range(random_start, len(random_doc)):
                    sent_b.append(random_doc[j])
                    len_b = sum(sizes[sent_b])
                    if (len_b >= target_b_length):
                        break
                num_unused_segments = (len(current_chunk) - a_end)
                curr -= num_unused_segments
            else:
                sent_b = current_chunk[a_end:]
                len_b = sum(sizes[sent_b])
            (sent_a, sent_b) = self._truncate_sentences(sent_a, sent_b, max_num_tokens)
            self.sent_pairs.append((sent_a, sent_b, next_sent_label))
            self.sizes.append(((3 + sent_a[3]) + sent_b[3]))
            current_chunk = []
        curr += 1
