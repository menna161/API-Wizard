import argparse
import random as R


def logical_and(negation=False, upreds=None):
    'Logical AND with optional negation: p(X):-q(X);r(X).'
    preds = r_preds(3, upreds)
    argc = R.randint(1, 2)
    vs = r_vars(argc)
    rule = [(preds[0], vs), (preds[1], vs[:1]), (preds[2], (vs[1:] or vs))]
    if upreds:
        return rule
    ctx = [rule]
    args = choices(r_consts(2), argc)
    prem1 = (preds[1], args[:1])
    prem2 = (preds[2], (args[1:] or args))
    prems = [prem1, prem2]
    if negation:
        ridx = R.randrange(2)
        (p, pargs) = ctx[(- 1)][(ridx + 1)]
        ctx[(- 1)][(ridx + 1)] = (('-' + p), pargs)
        cctx = ctx.copy()
        add_pred(cctx, prems[ridx], preds, args)
        cctx.append([prems[(1 - ridx)]])
        targets = [((preds[0], args), 1)]
        gen_task(cctx, targets, preds)
        fidx = R.randrange(2)
        if (ridx == fidx):
            ctx.append([prems[ridx]])
            add_pred(ctx, prems[(1 - ridx)], preds, args, 0.8)
        else:
            add_pred(ctx, prems[(1 - ridx)], preds, args)
            add_pred(ctx, prems[ridx], preds, args)
        targets = [((preds[0], args), 0)]
        gen_task(ctx, targets, preds)
    else:
        cctx = ctx.copy()
        add_pred(cctx, prems[0], preds, args, 1.0)
        add_pred(cctx, prems[1], preds, args, 1.0)
        targets = [((preds[0], args), 1)]
        gen_task(cctx, targets, preds)
        fidx = R.randrange(2)
        add_pred(ctx, prems[fidx], preds, args)
        add_pred(ctx, prems[(1 - fidx)], preds, args, 0.8)
        targets = [((preds[0], args), 0)]
        gen_task(ctx, targets, preds)
