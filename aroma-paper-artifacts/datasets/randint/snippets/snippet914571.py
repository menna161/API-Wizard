import argparse
import random as R


def gen_task1(upreds=None):
    'Ground instances only: p(a).q(c,b).'
    preds = r_preds(2, upreds)
    args = r_consts(R.randint(1, 2))
    rule = [(preds[0], args)]
    if upreds:
        return rule
    ctx = list()
    add_pred(ctx, rule[0], preds, args, 1.0)
    targets = [(rule[0], 1)]
    args = r_consts(R.randint(1, 2))
    fpred = (preds[1], args)
    add_pred(ctx, fpred, preds, args)
    targets.append((fpred, 0))
    gen_task(ctx, targets, preds)
