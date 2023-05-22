import argparse
import random as R


def gen_task(context, targets, upreds):
    'Fill context with random preds and output program.'
    ctx = context.copy()
    for _ in range(ARGS.noise_size):
        task = ('gen_task' + str(R.randint(1, max(1, ARGS.task))))
        ctx.append(globals()[task](upreds))
    output(ctx, targets)
