import torch
from torch.autograd import Variable
import numpy as np
import os
import argparse
import random
import copy
from tqdm import tqdm
import pickle
from scorer.data_helper.json_reader import read_sorted_scores, read_articles, read_processed_scores, read_scores
from scipy.stats import spearmanr, pearsonr, kendalltau
import math
from resources import MODEL_WEIGHT_DIR

if (__name__ == '__main__'):
    (epoch_num, batch_size, train_type, train_percent, dev_percent, learn_rate, model_type, device) = parse_args()
    print('\n=====Arguments====')
    print('epoch num {}'.format(epoch_num))
    print('batch size {}'.format(batch_size))
    print('train type {}'.format(train_type))
    print('train percent {}'.format(train_percent))
    print('dev percent {}'.format(dev_percent))
    print('learn rate {}'.format(learn_rate))
    print('model type {}'.format(model_type))
    print('device {}'.format(device))
    print('=====Arguments====\n')
    if ((train_percent + dev_percent) >= 1.0):
        print('ERROR! Train data percentage plus dev data percentage is {}! Make sure the sum is below 1.0!'.format((train_percent + dev_percent)))
        exit(1)
    BERT_VEC_LENGTH = 1024
    (deep_model, optimiser) = build_model(model_type, (BERT_VEC_LENGTH * 2), learn_rate)
    if ('gpu' in device):
        deep_model.to('cuda')
    sorted_scores = read_sorted_scores()
    (train, dev, test, all) = parse_split_data(sorted_scores, train_percent, dev_percent)
    train_pairs = build_pairs(train)
    dev_pairs = build_pairs(dev)
    test_pairs = build_pairs(test)
    print(len(train_pairs), len(dev_pairs), len(test_pairs))
    with open('data/doc_summ_bert_vectors.pkl', 'rb') as ff:
        all_vec_dic = pickle.load(ff)
    pcc_list = []
    weights_list = []
    for ii in range(epoch_num):
        print('\n=====EPOCH {}====='.format(ii))
        loss = pair_train_rewarder(all_vec_dic, train_pairs, deep_model, optimiser, batch_size, device)
        print('--> loss', loss)
        results = test_rewarder(all_vec_dic, dev, deep_model, device)
        for metric in results:
            print('{}\t{}'.format(metric, np.mean(results[metric])))
        pcc_list.append(np.mean(results['pcc']))
        weights_list.append(copy.deepcopy(deep_model.state_dict()))
    idx = np.argmax(pcc_list)
    best_result = pcc_list[idx]
    print('\n======Best results come from epoch no. {}====='.format(idx))
    deep_model.load_state_dict(weights_list[idx])
    test_results = test_rewarder(all_vec_dic, test, deep_model, device)
    print('Its performance on the test set is:')
    for metric in test_results:
        print('{}\t{}'.format(metric, np.mean(test_results[metric])))
    model_weight_name = 'pcc{0:.4f}_'.format(np.mean(test_results['pcc']))
    model_weight_name += 'epoch{}_batch{}_{}_trainPercent{}_lrate{}_{}.model'.format(epoch_num, batch_size, train_type, train_percent, learn_rate, model_type)
    torch.save(weights_list[idx], os.path.join(MODEL_WEIGHT_DIR, model_weight_name))
    print('\nbest model weight saved to: {}'.format(os.path.join(MODEL_WEIGHT_DIR, model_weight_name)))
