import argparse
import random as R


def logical_or(negation=False, upreds=None):
    'Logical OR with optional negation: p(X):-q(X).p(X):-r(X).'
    preds = r_preds(3, upreds)
    argc = R.randint(1, 2)
    vs = r_vars(argc)
    swap = (R.random() < 0.5)
    prefix = ('-' if negation else '')
    rule = [(preds[0], vs), ((prefix + preds[1]), (vs[::(- 1)] if swap else vs))]
    if upreds:
        return rule
    ctx = list()
    ctx.append(rule)
    ctx.append([(preds[0], vs), (preds[2], vs)])
    args = r_consts(argc)
    ctx.append([(preds[0], args)])
    if (swap and (argc == 2)):
        args = r_consts(argc, args)
        add_pred(ctx, (preds[1], args), preds, args, 1.0)
        args = (args[::(- 1)] if swap else args)
        targets = [((preds[0], args), (1 - int(negation))), ((preds[0], args[::(- 1)]), int(negation))]
        gen_task(ctx, targets, preds)
    elif ((not negation) and (R.random() < 0.2)):
        targets = [((preds[0], args), 1)]
        gen_task(ctx, targets, preds)
        del ctx[(- 1)]
        targets = [((preds[0], args), 0)]
        gen_task(ctx, targets, preds)
    else:
        prems = [(preds[i], r_consts(argc, args)) for i in range(1, 3)]
        sidx = R.randrange(2)
        cctx = ctx.copy()
        if (negation and (sidx == 0)):
            add_pred(cctx, prems[0], preds, prems[0][1])
            add_pred(cctx, prems[1], preds, prems[1][1], 0.2)
        else:
            add_pred(cctx, prems[sidx], preds, prems[sidx][1], 1.0)
            add_pred(cctx, prems[(1 - sidx)], preds, prems[(1 - sidx)][1], 0.2)
        targets = [((preds[0], prems[sidx][1]), 1)]
        gen_task(cctx, targets, preds)
        add_pred(ctx, prems[0], preds, prems[0][1], int(negation))
        add_pred(ctx, prems[1], preds, prems[1][1])
        targets = [((preds[0], prems[sidx][1]), 0)]
        gen_task(ctx, targets, preds)
