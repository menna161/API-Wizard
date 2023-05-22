import tensorflow as tf
import tensorflow.keras.backend as K
import numpy as np
import os
import time


def run_network(data, input_size, output_size, problem_type, net_kw, run_kw, num_workers=8, pin_memory=True, validate=True, val_patience=np.inf, test=False, ensemble=False, numepochs=100, wt_init=None, bias_init=None, verbose=True):
    "\n    ARGS:\n        data:\n            6-ary tuple (xtr,ytr, xva,yva, xte,yte) from get_data_mlp(), OR\n            Dict with keys 'train', 'val', 'test' from get_data_cnn()\n        input_size, output_size, net_kw : See Net()\n        run_kw:\n            lr: Initial learning rate\n            gamma: Learning rate decay coefficient\n            milestones: When to step decay learning rate, e.g. 0.5 will decay lr halfway through training\n            weight_decay: Default 0\n            batch_size: Default 256\n        num_workers, pin_memory: Only required if using Pytorch data loaders\n            Generally, set num_workers equal to number of threads (e.g. my Macbook pro has 4 cores x 2 = 8 threads)\n        validate: Whether to do validation at the end of every epoch.\n        val_patience: If best val acc doesn't increase for this many epochs, then stop training. Set as np.inf to never stop training (until numepochs)\n        test: True - Test at end, False - don't\n        ensemble: If True, return feedforward soft outputs to be later used for ensembling\n        numepochs: Self explanatory\n        wt_init, bias_init: Respective pytorch functions\n        verbose: Print messages\n    \n    RETURNS:\n        net: Complete net\n        recs: Dictionary with a key for each stat collected and corresponding value for all values of the stat\n    "
    net = Net(input_size=input_size, output_size=output_size, problem_type=problem_type, **net_kw)
    net.build(tuple((([None] + input_size[1:]) + [input_size[0]])))
    '\n    for i in range(len(net.mlp)):\n        if wt_init is not None:\n            wt_init(net.mlp[i].weight.data)\n        if bias_init is not None:\n            bias_init(net.mlp[i].bias.data)\n    '
    lr = (run_kw['lr'] if ('lr' in run_kw) else run_kws_defaults['lr'])
    gamma = (run_kw['gamma'] if ('gamma' in run_kw) else run_kws_defaults['gamma'])
    milestones = (run_kw['milestones'] if ('milestones' in run_kw) else run_kws_defaults['milestones'])
    weight_decay = (run_kw['weight_decay'] if ('weight_decay' in run_kw) else run_kws_defaults['weight_decay'])
    batch_size = (run_kw['batch_size'] if ('batch_size' in run_kw) else run_kws_defaults['batch_size'])
    if (not isinstance(batch_size, int)):
        batch_size = batch_size.item()
    if (problem_type == 'classification'):
        lossfunc = tf.keras.losses.SparseCategoricalCrossentropy()
    elif (problem_type == 'regression'):
        lossfunc = tf.keras.losses.MeanSquaredError()
    opt = tf.keras.optimizers.Adam(learning_rate=lr, decay=weight_decay)
    net.compile(optimizer=opt, loss=lossfunc, metrics=['accuracy'])
    trainable_count = np.sum([K.count_params(w) for w in net.trainable_weights])

    def multi_step_lr(epoch):
        LR_START = lr
        GAMMA = gamma
        NUMEPOCHS = numepochs
        step = 0
        for milestone in milestones:
            if (epoch >= int((milestone * NUMEPOCHS))):
                step += 1
        return (LR_START * (GAMMA ** step))
    lr_callback = tf.keras.callbacks.LearningRateScheduler(multi_step_lr, verbose=verbose)
    (xtr, ytr, xva, yva, xte, yte) = data
    recs = {}
    total_t = 0
    best_val_acc = (- np.inf)
    best_val_loss = np.inf

    class TimeHistory(tf.keras.callbacks.Callback):

        def on_train_begin(self, logs={}):
            self.times = []

        def on_epoch_begin(self, batch, logs={}):
            self.epoch_time_start = time.time()

        def on_epoch_end(self, batch, logs={}):
            self.times.append((time.time() - self.epoch_time_start))
    th_callback = TimeHistory()
    if (validate is True):
        if (problem_type == 'classification'):
            es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=val_patience, verbose=verbose, restore_best_weights=True)
        elif (problem_type == 'regression'):
            es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=val_patience, verbose=verbose, restore_best_weights=True)
        history = net.fit(x=xtr, y=ytr, verbose=verbose, validation_data=(xva, yva), batch_size=batch_size, epochs=numepochs, shuffle=True, use_multiprocessing=False, callbacks=[lr_callback, th_callback, es_callback])
        recs['val_accs'] = (np.array(history.history['val_accuracy']) * 100)
        recs['val_losses'] = history.history['val_loss']
    else:
        history = net.fit(x=xtr, y=ytr, verbose=verbose, batch_size=batch_size, epochs=numepochs, shuffle=True, use_multiprocessing=False, callbacks=[lr_callback, th_callback])
    recs['train_accs'] = (np.array(history.history['accuracy']) * 100)
    recs['train_losses'] = history.history['loss']
    total_t += np.sum(th_callback.times)
    if (validate is True):
        if (problem_type == 'classification'):
            print('\nBest validation accuracy = {0}% obtained in epoch {1}'.format(np.max(recs['val_accs']), (np.argmax(recs['val_accs']) + 1)))
        elif (problem_type == 'regression'):
            print('\nBest validation loss = {0} obtained in epoch {1}'.format(np.min(recs['val_losses']), (np.argmin(recs['val_losses']) + 1)))
    if (test is True):
        ret = net.evaluate(x=xte, y=yte, verbose=verbose, batch_size=batch_size, workers=1, use_multiprocessing=False)
        recs['test_acc'] = (ret[1] * 100)
        recs['test_loss'] = ret[0]
        print('Test accuracy = {0}%, Loss = {1}\n'.format(np.round(recs['test_acc'], 2), np.round(recs['test_loss'], 3)))
    recs['t_epoch'] = ((total_t / (numepochs - 1)) if (numepochs > 1) else total_t)
    print('Avg time taken per epoch = {0}'.format(recs['t_epoch']))
    return (net, recs)
