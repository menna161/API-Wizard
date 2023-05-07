import os, sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import cPickle as pickle
import _pickle as pickle


def plotting(exp_dir):
    train_dict = pickle.load(open(os.path.join(exp_dir, 'log.pkl'), 'rb'))
    plt.plot(np.asarray(train_dict['train_loss']), label='train_loss')
    plt.plot(np.asarray(train_dict['test_loss']), label='test_loss')
    plt.xlabel('evaluation step')
    plt.ylabel('metrics')
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(exp_dir, 'loss.png'))
    plt.clf()
    plt.plot(np.asarray(train_dict['train_acc']), label='train_acc')
    plt.plot(np.asarray(train_dict['test_acc']), label='test_acc')
    plt.xlabel('evaluation step')
    plt.ylabel('metrics')
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(exp_dir, 'acc.png'))
    plt.clf()
