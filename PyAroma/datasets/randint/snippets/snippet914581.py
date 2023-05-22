import argparse
import random as R


def gen_task8(upreds=None):
    'Transitive case: p(X,Y):-q(X,Z);r(Z,Y).'
    preds = r_preds(3, upreds)
    vs = r_vars(3)
    rule = [(preds[0], [vs[0], vs[2]]), (preds[1], vs[:2]), (preds[2], vs[1:])]
    if upreds:
        return rule
    ctx = [rule]
    args = r_consts(3)
    add_pred(ctx, (preds[1], args[:2]), preds, args, 1.0)
    add_pred(ctx, (preds[2], args[1:]), preds, args, 1.0)
    argso = r_consts(3)
    argso.insert(R.randint(1, 2), r_consts(1, argso)[0])
    add_pred(ctx, (preds[1], argso[:2]), preds, argso, 0.5)
    add_pred(ctx, (preds[2], argso[2:]), preds, argso, 0.5)
    targets = [((preds[0], [args[0], args[2]]), 1), ((preds[0], [argso[0], argso[3]]), 0)]
    gen_task(ctx, targets, preds)
