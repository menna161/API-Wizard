import argparse
import random as R


def nstep_deduction(steps, negation=False, upreds=None):
    assert (steps >= 1), 'Need at least 1 step deduction.'
    preds = r_preds((2 if upreds else (3 + steps)), upreds)
    consts = r_consts(2)
    (ctx, targets) = (list(), list())
    prefix = ('-' if negation else '')
    if (R.random() < 0.5):
        vs = r_vars(2)
        rule = [(preds[0], vs), ((prefix + preds[1]), vs[::(- 1)])]
        if upreds:
            return rule
        ctx.append(rule)
        swapc = 1
        for j in range((steps - 1)):
            vs = r_vars(2)
            toswap = (R.random() < 0.5)
            args = (vs[::(- 1)] if toswap else vs)
            ctx.append([(preds[(j + 1)], vs), (preds[(j + 2)], args)])
            swapc += int(toswap)
        args = r_consts(2)
        add_pred(ctx, (preds[steps], args), preds, consts, 1.0)
        args = (args if ((swapc % 2) == 0) else args[::(- 1)])
        targets.append(((preds[0], args), (1 - int(negation))))
        targets.append(((preds[0], args[::(- 1)]), int(negation)))
        gen_task(ctx, targets, preds)
    else:
        argc = R.randint(1, 2)
        vs = r_vars(argc)
        rule = [(preds[0], vs), ((prefix + preds[1]), vs)]
        if upreds:
            return rule
        ctx.append(rule)
        for j in range((steps - 1)):
            vs = r_vars(argc)
            ctx.append([(preds[(j + 1)], vs), (preds[(j + 2)], vs)])
        args = choices(r_consts(2), argc)
        cctx = ctx.copy()
        spred = (preds[steps], args)
        add_pred(cctx, spred, preds, args, 1.0)
        targets = [((preds[0], args), (1 - int(negation)))]
        gen_task(cctx, targets, preds)
        if (R.random() < 0.5):
            p = r_preds(1, preds)[0]
            preds.append(p)
            add_pred(ctx, spred, preds, args, 1.0)
            ctx[0] = [(preds[0], vs), ((prefix + p), vs)]
        else:
            add_pred(ctx, spred, preds, args)
        targets = [((preds[0], args), int(negation))]
        gen_task(ctx, targets, preds)
