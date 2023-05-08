from os.path import join, dirname, abspath
import sys
import copy
import random
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from gensim.models import KeyedVectors
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from evidence_inference.models.utils import PaddedSequence
from evidence_inference.models.attention_distributions import TokenAttention, evaluate_model_attention_distribution
import pdb
import pdb
import pdb


def train(ev_inf: InferenceNet, train_Xy, val_Xy, test_Xy, inference_vectorizer, epochs=10, batch_size=16, shuffle=True):
    if (not shuffle):
        train_Xy.sort(key=(lambda x: len(x['article'])))
        val_Xy.sort(key=(lambda x: len(x['article'])))
        test_Xy.sort(key=(lambda x: len(x['article'])))
    print('Using {} training examples, {} validation examples, {} testing examples'.format(len(train_Xy), len(val_Xy), len(test_Xy)))
    most_common = stats.mode([_get_majority_label(inst) for inst in train_Xy])[0][0]
    best_val_model = None
    best_val_f1 = float('-inf')
    if USE_CUDA:
        ev_inf = ev_inf.cuda()
    optimizer = optim.Adam(ev_inf.parameters())
    criterion = nn.CrossEntropyLoss(reduction='sum')
    epochs_since_improvement = 0
    val_metrics = {'val_acc': [], 'val_p': [], 'val_r': [], 'val_f1': [], 'val_loss': [], 'train_loss': [], 'val_aucs': [], 'train_aucs': [], 'val_entropies': [], 'val_evidence_token_mass': [], 'val_evidence_token_err': [], 'train_entropies': [], 'train_evidence_token_mass': [], 'train_evidence_token_err': []}
    for epoch in range(epochs):
        if (epochs_since_improvement > 10):
            print('Exiting early due to no improvement on validation after 10 epochs.')
            break
        if shuffle:
            random.shuffle(train_Xy)
        epoch_loss = 0
        for i in range(0, len(train_Xy), batch_size):
            instances = train_Xy[i:(i + batch_size)]
            ys = torch.cat([_get_y_vec(inst['y'], as_vec=False) for inst in instances], dim=0)
            unk_idx = int(inference_vectorizer.str_to_idx[SimpleInferenceVectorizer.PAD])
            (articles, Is, Cs, Os) = [PaddedSequence.autopad([torch.LongTensor(inst[x]) for inst in instances], batch_first=True, padding_value=unk_idx) for x in ['article', 'I', 'C', 'O']]
            optimizer.zero_grad()
            if USE_CUDA:
                (articles, Is, Cs, Os) = (articles.cuda(), Is.cuda(), Cs.cuda(), Os.cuda())
                ys = ys.cuda()
            verbose_attn = (((epoch == (epochs - 1)) and (i == 0)) or ((epoch == 0) and (i == 0)))
            if verbose_attn:
                print('Training attentions:')
            tags = ev_inf(articles, Is, Cs, Os, batch_size=len(instances), verbose_attn=verbose_attn)
            loss = criterion(tags, ys)
            epoch_loss += loss.item()
            loss.backward()
            optimizer.step()
        val_metrics['train_loss'].append(epoch_loss)
        with torch.no_grad():
            verbose_attn_to_batches = (set([0, 1, 2, 3, 4]) if ((epoch == (epochs - 1)) or (epoch == 0)) else False)
            if verbose_attn_to_batches:
                print('Validation attention:')
            (val_y, val_y_hat) = make_preds(ev_inf, val_Xy, batch_size, inference_vectorizer, verbose_attn_to_batches=verbose_attn_to_batches)
            val_loss = criterion(val_y_hat, val_y.squeeze())
            y_hat = to_int_preds(val_y_hat)
            if (epoch == 0):
                dummy_preds = ([most_common] * len(val_y))
                dummy_acc = accuracy_score(val_y.cpu(), dummy_preds)
                val_metrics['baseline_val_acc'] = dummy_acc
                (p, r, f1, _) = precision_recall_fscore_support(val_y.cpu(), dummy_preds, labels=None, beta=1, average='macro', pos_label=1, warn_for=('f-score',), sample_weight=None)
                val_metrics['p_dummy'] = p
                val_metrics['r_dummy'] = r
                val_metrics['f_dummy'] = f1
                print('val dummy accuracy: {:.3f}'.format(dummy_acc))
                print('classification report for dummy on val: ')
                print(classification_report(val_y.cpu(), dummy_preds))
                print('\n\n')
            acc = accuracy_score(val_y.cpu(), y_hat)
            val_metrics['val_acc'].append(acc)
            val_loss = val_loss.cpu().item()
            val_metrics['val_loss'].append(val_loss)
            (p, r, f1, _) = precision_recall_fscore_support(val_y.cpu(), y_hat, labels=None, beta=1, average='macro', pos_label=1, warn_for=('f-score',), sample_weight=None)
            val_metrics['val_f1'].append(f1)
            val_metrics['val_p'].append(p)
            val_metrics['val_r'].append(r)
            if ev_inf.article_encoder.use_attention:
                (train_auc, train_entropies, train_evidence_token_masses, train_evidence_token_err) = evaluate_model_attention_distribution(ev_inf, train_Xy, cuda=USE_CUDA, compute_attention_diagnostics=True)
                (val_auc, val_entropies, val_evidence_token_masses, val_evidence_token_err) = evaluate_model_attention_distribution(ev_inf, val_Xy, cuda=USE_CUDA, compute_attention_diagnostics=True)
                print('train auc: {:.3f}, entropy: {:.3f}, evidence mass: {:.3f}, err: {:.3f}'.format(train_auc, train_entropies, train_evidence_token_masses, train_evidence_token_err))
                print('val auc: {:.3f}, entropy: {:.3f}, evidence mass: {:.3f}, err: {:.3f}'.format(val_auc, val_entropies, val_evidence_token_masses, val_evidence_token_err))
            else:
                (train_auc, train_entropies, train_evidence_token_masses, train_evidence_token_err) = ('', '', '', '')
                (val_auc, val_entropies, val_evidence_token_masses, val_evidence_token_err) = ('', '', '', '')
            val_metrics['train_aucs'].append(train_auc)
            val_metrics['train_entropies'].append(train_entropies)
            val_metrics['train_evidence_token_mass'].append(train_evidence_token_masses)
            val_metrics['train_evidence_token_err'].append(train_evidence_token_err)
            val_metrics['val_aucs'].append(val_auc)
            val_metrics['val_entropies'].append(val_entropies)
            val_metrics['val_evidence_token_mass'].append(val_evidence_token_masses)
            val_metrics['val_evidence_token_err'].append(val_evidence_token_err)
            if (f1 > best_val_f1):
                print('New best model at {} with val f1 {:.3f}'.format(epoch, f1))
                best_val_f1 = f1
                best_val_model = copy.deepcopy(ev_inf)
                epochs_since_improvement = 0
            else:
                epochs_since_improvement += 1
            print('epoch {}. train loss: {}; val loss: {}; val acc: {:.3f}'.format(epoch, epoch_loss, val_loss, acc))
            print(classification_report(val_y.cpu(), y_hat))
            print('val macro f1: {0:.3f}'.format(f1))
            print('\n\n')
    val_metrics['best_val_f1'] = best_val_f1
    with torch.no_grad():
        print('Test attentions:')
        verbose_attn_to_batches = set([0, 1, 2, 3, 4])
        (test_y, test_y_hat) = make_preds(best_val_model, test_Xy, batch_size, inference_vectorizer, verbose_attn_to_batches=verbose_attn_to_batches)
        test_loss = criterion(test_y_hat, test_y.squeeze())
        y_hat = to_int_preds(test_y_hat)
        final_test_preds = zip([t['a_id'] for t in test_Xy], [t['p_id'] for t in test_Xy], y_hat)
        acc = accuracy_score(test_y.cpu(), y_hat)
        val_metrics['test_acc'] = acc
        test_loss = test_loss.cpu().item()
        val_metrics['test_loss'] = test_loss
        (p, r, f1, _) = precision_recall_fscore_support(test_y.cpu(), y_hat, labels=None, beta=1, average='macro', pos_label=1, warn_for=('f-score',), sample_weight=None)
        val_metrics['test_f1'] = f1
        val_metrics['test_p'] = p
        val_metrics['test_r'] = r
        if ev_inf.article_encoder.use_attention:
            (test_auc, test_entropies, test_evidence_token_masses, test_evidence_token_err) = evaluate_model_attention_distribution(best_val_model, test_Xy, cuda=USE_CUDA, compute_attention_diagnostics=True)
            print('test auc: {:.3f}, , entropy: {:.3f}, kl_to_uniform {:.3f}'.format(test_auc, test_entropies, test_evidence_token_masses))
        else:
            (test_auc, test_entropies, test_evidence_token_masses, test_evidence_token_err) = ('', '', '', '')
        val_metrics['test_auc'] = test_auc
        val_metrics['test_entropy'] = test_entropies
        val_metrics['test_evidence_token_mass'] = test_evidence_token_masses
        val_metrics['test_evidence_token_err'] = test_evidence_token_err
        print('test loss: {}; test acc: {:.3f}'.format(test_loss, acc))
        print(classification_report(test_y.cpu(), y_hat))
        print('test macro f1: {}'.format(f1))
        print('\n\n')
    return (best_val_model, inference_vectorizer, train_Xy, val_Xy, val_metrics, final_test_preds)
