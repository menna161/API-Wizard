import argparse
import random as R


def gen_task2(upreds=None):
    'Variablised facts only: p(X).q(X,Y).'
    preds = r_preds(2, upreds)
    (ctx, targets) = (list(), list())
    if (R.random() < 0.5):
        v = r_vars(1)[0]
        rule = [(preds[0], [v, v])]
        if upreds:
            return rule
        ctx.append(rule)
        cs = r_consts(2)
        c = R.choice(cs)
        targets.append(((preds[0], [c, c]), 1))
        targets.append(((preds[0], cs), 0))
    else:
        argc = R.randint(1, 2)
        args = r_vars(argc)
        rule = [(preds[0], args)]
        if upreds:
            return rule
        ctx.append(rule)
        args = choices(r_consts(2), argc)
        targets.append(((preds[0], args), 1))
        targets.append(((preds[1], args), 0))
    gen_task(ctx, targets, preds)
