import argparse
import os
import time
import numpy as np
import tinynn as tn


def main():
    if (args.seed >= 0):
        tn.seeder.random_seed(args.seed)
    mnist = tn.dataset.MNIST(args.data_dir, one_hot=True)
    (train_x, train_y) = mnist.train_set
    (test_x, test_y) = mnist.test_set
    if (args.model_type == 'mlp'):
        net = tn.net.Net([tn.layer.Dense(200), tn.layer.ReLU(), tn.layer.Dense(100), tn.layer.ReLU(), tn.layer.Dense(70), tn.layer.ReLU(), tn.layer.Dense(30), tn.layer.ReLU(), tn.layer.Dense(10)])
    elif (args.model_type == 'cnn'):
        train_x = train_x.reshape(((- 1), 28, 28, 1))
        test_x = test_x.reshape(((- 1), 28, 28, 1))
        net = tn.net.Net([tn.layer.Conv2D(kernel=[5, 5, 1, 6], stride=[1, 1]), tn.layer.ReLU(), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Conv2D(kernel=[5, 5, 6, 16], stride=[1, 1]), tn.layer.ReLU(), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Flatten(), tn.layer.Dense(120), tn.layer.ReLU(), tn.layer.Dense(84), tn.layer.ReLU(), tn.layer.Dense(10)])
    elif (args.model_type == 'rnn'):
        train_x = train_x.reshape(((- 1), 28, 28))
        test_x = test_x.reshape(((- 1), 28, 28))
        net = tn.net.Net([tn.layer.RNN(num_hidden=30), tn.layer.Dense(10)])
    elif (args.model_type == 'lstm'):
        train_x = train_x.reshape(((- 1), 28, 28))
        test_x = test_x.reshape(((- 1), 28, 28))
        net = tn.net.Net([tn.layer.LSTM(num_hidden=30), tn.layer.Dense(10)])
    else:
        raise ValueError('Invalid argument: model_type')
    loss = tn.loss.SoftmaxCrossEntropy()
    optimizer = tn.optimizer.Adam(lr=args.lr)
    model = tn.model.Model(net=net, loss=loss, optimizer=optimizer)
    if (args.model_path is not None):
        model.load(args.model_path)
        evaluate(model, test_x, test_y)
    else:
        iterator = tn.data_iterator.BatchIterator(batch_size=args.batch_size)
        for epoch in range(args.num_ep):
            t_start = time.time()
            for batch in iterator(train_x, train_y):
                pred = model.forward(batch.inputs)
                (loss, grads) = model.backward(pred, batch.targets)
                model.apply_grads(grads)
            print(f'Epoch {epoch} time cost: {(time.time() - t_start)}')
            evaluate(model, test_x, test_y)
        if (not os.path.isdir(args.model_dir)):
            os.makedirs(args.model_dir)
        model_name = f'mnist-{args.model_type}-epoch{args.num_ep}.pkl'
        model_path = os.path.join(args.model_dir, model_name)
        model.save(model_path)
        print(f'Model saved in {model_path}')
