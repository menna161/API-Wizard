import argparse
import random as R


def generate(depth=0, context=None, target=None, success=None, upreds=None, uconsts=None, stats=None):
    'Generate tree based logic program.'
    ctx = (context or list())
    args = (target[1:] if target else [r_consts(1)[0] for _ in range(ARGS.arity)])
    t = (target or ([r_preds(1)[0]] + [R.choice(args) for _ in range(R.randint(1, ARGS.arity))]))
    arity = len(t[1:])
    succ = (success if (success is not None) else R.choice((True, False)))
    upreds = (upreds or set([t[0]]))
    uconsts = (uconsts or set(t[1:]))
    stats = (stats or dict())
    num_rules = R.randint(1, ARGS.max_or_branch)
    stats.setdefault('or_num', list()).append(num_rules)
    succs = ([R.choice((True, False)) for _ in range(num_rules)] if succ else ([False] * num_rules))
    if (succ and (not any(succs))):
        succs[R.randrange(len(succs))] = True
    depths = [R.randint(0, depth) for _ in range(num_rules)]
    if (max(depths) != depth):
        depths[R.randrange(num_rules)] = depth
    is_tadded = False
    for (child_depth, child_succ) in zip(depths, succs):
        if (child_depth == 0):
            if (R.random() < 0.2):
                args = t[1:]
                args[R.randrange(len(args))] = r_consts(1, uconsts)[0]
                uconsts.update(args)
                ctx.append([([t[0]] + args)])
            if (R.random() < 0.2):
                p = r_preds(1, upreds)[0]
                upreds.add(p)
                ctx.append([([p] + t[1:])])
            if (R.random() < 0.2):
                ctx.append([(([t[0]] + t[1:]) + [R.choice((t[1:] + r_consts(arity)))])])
            if (R.random() < 0.2):
                vs = cv_mismatch(t[1:])
                if vs:
                    ctx.append([([t[0]] + vs)])
            if child_succ:
                if (R.random() < 0.5):
                    ctx.append([([t[0]] + cv_match(t[1:]))])
                elif (not is_tadded):
                    ctx.append([t])
                    is_tadded = True
            continue
        num_body = R.randint(1, ARGS.max_and_branch)
        stats.setdefault('body_num', list()).append(num_body)
        negation = ([R.choice((True, False)) for _ in range(num_body)] if ARGS.negation else ([False] * num_body))
        succ_targets = ([R.choice((True, False)) for _ in range(num_body)] if (not child_succ) else [(not n) for n in negation])
        if (not child_succ):
            ri = R.randrange(len(succ_targets))
            succ_targets[ri] = negation[ri]
        body_preds = r_preds(num_body, upreds)
        upreds.update(body_preds)
        lit_vars = cv_match(t[1:])
        if ((not child_succ) and (R.random() < 0.5)):
            vs = cv_mismatch(t[1:])
            if vs:
                lit_vars = vs
                succ_targets = [R.choice((True, False)) for _ in range(num_body)]
        lit_vars.extend([r_vars(1)[0] for _ in range(ARGS.unbound_vars)])
        rule = [([t[0]] + lit_vars[:arity])]
        vcmap = {lit_vars[i]: t[(i + 1)] for i in range(arity)}
        child_targets = list()
        for i in range(num_body):
            R.shuffle(lit_vars)
            child_arity = R.randint(1, arity)
            pred = ([body_preds[i]] + lit_vars[:child_arity])
            rule.append(([((NEG_PREFIX if negation[i] else '') + pred[0])] + pred[1:]))
            vs = [vcmap.get(v, r_consts(1, uconsts)[0]) for v in lit_vars[:child_arity]]
            child_targets.append(([pred[0]] + vs))
        ctx.append(rule)
        for (child_t, s) in zip(child_targets, succ_targets):
            generate((child_depth - 1), ctx, child_t, s, upreds, uconsts, stats)
    return (ctx, [(t, int(succ))], stats)
