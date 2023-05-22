import argparse
import numpy as np
import keras.callbacks as C
from data_gen import CHAR_IDX, IDX_CHAR
from utils import LogicSeq, StatefulCheckpoint, ThresholdStop
from models import build_model
import readline


def ilp(training=True):
    'Run the ILP task using the ILP model.'
    (goals, vgoals) = (['f(X)'], list())
    for g in goals:
        v = np.zeros((1, 1, 4, (len(CHAR_IDX) + 1)))
        for (i, c) in enumerate(g):
            v[(0, 0, i, CHAR_IDX[c])] = 1
        vgoals.append(v)
    model = build_model('ilp', 'weights/ilp.h5', char_size=(len(CHAR_IDX) + 1), training=training, goals=vgoals, num_preds=1, pred_len=4)
    model.summary()
    traind = LogicSeq.from_file('data/ilp_train.txt', ARGS.batch_size, pad=ARGS.pad)
    testd = LogicSeq.from_file('data/ilp_test.txt', ARGS.batch_size, pad=ARGS.pad)
    if training:
        callbacks = [C.ModelCheckpoint(filepath='weights/ilp.h5', verbose=1, save_best_only=True, save_weights_only=True), C.TerminateOnNaN()]
        model.fit_generator(traind, epochs=200, callbacks=callbacks, validation_data=testd, shuffle=True)
    else:
        ctx = 'b(h).v(O):-c(O).c(a).'
        ctx = ctx.split('.')[:(- 1)]
        ctx = [(r + '.') for r in ctx]
        dgen = LogicSeq([[(ctx, 'f(h).', 0)]], 1, False, False)
        print('TEMPLATES:')
        outs = model.predict_on_batch(dgen[0])
        (ts, out) = (outs[0], outs[(- 1)])
        print(ts)
        ts = np.argmax(ts[0], axis=(- 1))
        ts = np.vectorize((lambda i: IDX_CHAR[i]))(ts)
        print(ts)
        print('CTX:', ctx)
        for o in outs[1:(- 1)]:
            print(o)
        print('OUT:', out)
