import argparse
from itertools import chain
import sys
import random
import numpy as np
from sacrebleu import compute_bleu, corpus_bleu as _corpus_bleu


def multi_ref(refs, hypos):
    (_ref, _hypo) = ([], [])
    ref_cnt = 0
    assert (len(refs) == len(hypos))
    for (rs, hs) in zip(refs, hypos):
        a = set()
        for h in hs:
            s = [sentence_bleu(h, r) for r in rs]
            j = np.argmax(s)
            _ref.append(rs[j])
            _hypo.append(h)
            best = [k for k in range(len(rs)) if (s[k] == s[j])]
            a.add(random.choice(best))
        ref_cnt += len(a)
    print(('#refs covered: %.2f' % (ref_cnt / len(refs))))
    refs = list(zip(*refs))
    hypos = list(zip(*hypos))
    k = len(hypos)
    m = len(refs)
    flat_hypos = [hypos[j][i] for i in range(len(hypos[0])) for j in range(k)]
    duplicated_refs = [[ref for ref in refs_i for _ in range(k)] for refs_i in refs]
    loo_bleus = []
    for held_out_ref in range(m):
        remaining_refs = (duplicated_refs[:held_out_ref] + duplicated_refs[(held_out_ref + 1):])
        assert (len(remaining_refs) == (m - 1))
        loo_bleus.append(corpus_bleu(flat_hypos, remaining_refs))
    print(('average multi-reference BLEU (leave-one-out): %.2f' % np.mean(loo_bleus)))
