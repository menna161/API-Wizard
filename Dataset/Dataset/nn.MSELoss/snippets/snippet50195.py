from collections import defaultdict
from os.path import join, dirname, abspath
import copy
import sys
import random
import torch
import torch.nn as nn
import numpy as np
from scipy.stats import entropy, sem
from sklearn.metrics import roc_auc_score
from evidence_inference.models.utils import PaddedSequence
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer
import pdb


def pretrain_attention_with_random_spans(train_Xy, val_Xy, model, epochs=10, batch_size=16, cuda=True, tokenwise_attention=False, attention_acceptance='auc'):
    " A pretraining variants that is balanced. This is similar to pretrain_tokenwise_attention_balanced\n    \n    The primary difference between this and pretrain_tokenwise_attention_balanced\n    is that the loss function here is an MSELoss, so it uses the squared error\n    between the attention mechanism's output (unnormalized if tokenwise) instead\n    of using a BCELoss.\n    "

    def _prepare_random_matched_spans(model, batch_instances, cuda):
        unk_idx = int(model.vectorizer.str_to_idx[SimpleInferenceVectorizer.PAD])
        (Is, Cs, Os) = [PaddedSequence.autopad([torch.LongTensor(inst[x]) for inst in batch_instances], batch_first=True, padding_value=unk_idx) for x in ['I', 'C', 'O']]
        target_spans = [inst['evidence_spans'] for inst in batch_instances]
        target = []
        articles = []
        for (article, evidence_spans) in zip((x['article'] for x in batch_instances), target_spans):
            tgt = torch.zeros(len(article))
            for (start, end) in evidence_spans:
                tgt[start:end] = 1
            (start, end) = random.choice(evidence_spans)
            random_matched_span_start = random.randint(0, len(article))
            random_matched_span_end = ((random_matched_span_start + end) - start)
            tgt_pos = tgt[start:end]
            tgt_neg = tgt[random_matched_span_start:random_matched_span_end]
            article_pos = torch.LongTensor(article[start:end])
            article_neg = torch.LongTensor(article[random_matched_span_start:random_matched_span_end])
            if (random.random() > 0.5):
                articles.append(torch.cat([article_pos, article_neg]))
                target.append(torch.cat([tgt_pos, tgt_neg]))
            else:
                articles.append(torch.cat([article_neg, article_pos]))
                target.append(torch.cat([tgt_neg, tgt_pos]))
        target = PaddedSequence.autopad(target, batch_first=True, padding_value=0)
        articles = PaddedSequence.autopad(articles, batch_first=True, padding_value=unk_idx)
        if cuda:
            (articles, Is, Cs, Os, target) = (articles.cuda(), Is.cuda(), Cs.cuda(), Os.cuda(), target.cuda())
        return (articles, Is, Cs, Os, target)
    return pretrain_attention(train_Xy, val_Xy, model, prepare=_prepare_random_matched_spans, get_attention_weights=get_article_attention_weights, criterion=torch.nn.MSELoss(reduction='sum'), epochs=epochs, batch_size=batch_size, cuda=cuda, tokenwise_attention=tokenwise_attention, attention_acceptance=attention_acceptance)
