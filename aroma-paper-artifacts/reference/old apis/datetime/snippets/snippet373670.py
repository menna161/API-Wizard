import argparse
import datetime
import logging
import os
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.tensorboard import SummaryWriter
from transformers import AdamW, get_linear_schedule_with_warmup, get_cosine_with_hard_restarts_schedule_with_warmup
from data_loader import get_ARSC_data_loader, get_general_data_loader
from encoder_module import AttBiLSTMEncoder, BERTEncoder
from relation_module import NeuralTensorNetwork, BiLinear, Linear, L2Distance, CosineDistance
from att_induction import AttentionInductionNetwork
from induction import InductionNetwork
from matching import MatchingNetwork
from prototype import PrototypeNetwork
from relation import RelationNetwork
from apex import amp


def main():
    parser = argparse.ArgumentParser('Train or test a FSL model.')
    parser.add_argument('--train_data', default=None, type=str, help='File name of training data.')
    parser.add_argument('--val_data', default=None, type=str, help='File name of validation data.')
    parser.add_argument('--test_data', action='append', type=str, help='File names of testing data.')
    parser.add_argument('-N', default=5, type=int, help='N way')
    parser.add_argument('-K', default=5, type=int, help='K shot.')
    parser.add_argument('-Q', default=10, type=int, help='Number of query instances per class.')
    parser.add_argument('--encoder', default='bert-base', type=str, choices=('att-bi-lstm', 'att-bi-lstm-zh', 'bert-base', 'bert-chinese'), help="Encoder: 'att-bi-lstm', 'att-bi-lstm-zh', 'bert-base' or 'bert-chinese'.")
    parser.add_argument('--model', default='att-induction', type=str, choices=('att-induction', 'induction', 'matching', 'prototype', 'relation'), help="Models: 'att-induction', 'induction', 'matching', 'prototype' or 'relation'.")
    parser.add_argument('--optim', default='adamw', type=str, choices=('sgd', 'adam', 'adamw'), help="Optimizer: 'sgd', 'adam' or 'adamw'.")
    parser.add_argument('--train_episodes', default=5000, type=int, help='Number of training episodes. (train_episodes*=batch_size)')
    parser.add_argument('--val_episodes', default=3000, type=int, help='Number of validation episodes. (val_episodes*=batch_size)')
    parser.add_argument('--val_steps', default=100, type=int, help='Validate after x train_episodes.')
    parser.add_argument('--test_episodes', default=5000, type=int, help='Number of testing episodes. test_episodes*=batch_size')
    parser.add_argument('--max_length', default=512, type=int, help='Maximum length of sentences.')
    parser.add_argument('--hidden_size', default=768, type=int, help='Hidden size.')
    parser.add_argument('--att_dim', default=None, type=int, help='Attention dimension of Self-Attention Bi-LSTM encoder.')
    parser.add_argument('--induction_iters', default=None, type=int, help='Number of iterations in capsule network.')
    parser.add_argument('--n_heads', default=None, type=int, help='Number of heads in self-attention.')
    parser.add_argument('--dropout', default=None, type=float, help='Dropout rate.')
    parser.add_argument('-H', '--relation_size', default=130, type=int, help='Size of neural tensor network.')
    parser.add_argument('-B', '--batch_size', default=4, type=int, help='Batch size.')
    parser.add_argument('--grad_steps', default=1, type=int, help='Accumulate gradient update every x iterations.')
    parser.add_argument('--lr', default=1e-05, type=float, help='Learning rate.')
    parser.add_argument('--warmup', default=0.06, type=float, help='Warmup ratio.')
    parser.add_argument('--weight_decay', default=0.01, type=float, help='Weight decay.')
    parser.add_argument('--pretrain_path', default='../resource/pretrain/', type=str, help='Path to pretraind models.')
    parser.add_argument('--output_path', default='../log/', type=str, help='Save log and results.')
    parser.add_argument('--load_checkpoint', default=None, type=str, help='Path of checkpoint file.')
    parser.add_argument('--only_test', action='store_true')
    args = parser.parse_args()
    if ('ARSC' in args.train_data):
        data_name = 'ARSC'
    elif ('20news' in args.train_data):
        data_name = '20news'
    elif ('HuffPost' in args.train_data):
        data_name = 'HuffPost'
    elif ('M' == args.train_data[0]):
        data_name = 'controversial_issues'
    else:
        raise ValueError
    if (not args.only_test):
        log_path = os.path.join(args.output_path, args.train_data, ((((args.encoder + f'-maxlen{args.max_length}-hidden{args.hidden_size}+') + args.model) + f'-iters{args.induction_iters}-nheads{args.n_heads}-dropout{args.dropout}+') + f'-H{args.relation_size}'))
        prefix = ('-'.join(str(datetime.datetime.now())[:(- 10)].split()) + f'+episodes{args.train_episodes}+N{args.N}+K{args.K}+Q{args.Q}+B{args.batch_size}+grad{args.grad_steps}+lr{args.lr}+warmup{args.warmup}+weightdecay{args.weight_decay}')
        output_path = os.path.join(log_path, prefix)
        save_checkpoint = os.path.join(output_path, 'checkpoint.pt')
        writer = SummaryWriter(log_dir=os.path.join(output_path, 'tensorboard/'))
    else:
        output_path = os.path.join(os.path.dirname(args.load_checkpoint), 'test', '-'.join(str(datetime.datetime.now())[:(- 7)].split()))
        writer = None
    if (not os.path.exists(output_path)):
        os.makedirs(output_path)
    logging.basicConfig(filename=os.path.join(output_path, 'run.log'), level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('All parameters: {}'.format(vars(args)))
    if torch.cuda.is_available():
        logging.info('CUDA is available!')
        current_cuda = True
        current_device = torch.device('cuda')
    else:
        logging.warning('CUDA is not available. Using CPU!')
        current_cuda = False
        current_device = torch.device('cpu')
    if (args.encoder == 'att-bi-lstm'):
        encoder = AttBiLSTMEncoder(args.pretrain_path, args.max_length, args.hidden_size, args.att_dim)
        args.hidden_size *= 2
    elif (args.encoder == 'att-bi-lstm-zh'):
        encoder = AttBiLSTMEncoder(args.pretrain_path, args.max_length, args.hidden_size, args.att_dim, is_zh=True)
        args.hidden_size *= 2
    elif (args.encoder == 'bert-base'):
        encoder = BERTEncoder('bert-base-uncased', args.pretrain_path, args.max_length)
    elif (args.encoder == 'bert-chinese'):
        encoder = BERTEncoder('bert-base-chinese', args.pretrain_path, args.max_length)
    else:
        raise NotImplementedError
    tokenizer = encoder.tokenize
    if (args.model == 'att-induction'):
        relation_module = NeuralTensorNetwork(args.hidden_size, args.relation_size)
        model = AttentionInductionNetwork(encoder, relation_module, args.hidden_size, args.max_length, args.induction_iters, args.n_heads, args.dropout, current_device=current_device)
    elif (args.model == 'induction'):
        relation_module = BiLinear(args.hidden_size, args.relation_size)
        model = InductionNetwork(encoder, relation_module, args.hidden_size, args.max_length, args.induction_iters, current_device=current_device)
    elif (args.model == 'matching'):
        relation_module = CosineDistance()
        model = MatchingNetwork(encoder, relation_module, args.hidden_size, args.max_length, current_device=current_device)
    elif (args.model == 'prototype'):
        relation_module = L2Distance()
        model = PrototypeNetwork(encoder, relation_module, args.hidden_size, args.max_length, current_device=current_device)
    elif (args.model == 'relation'):
        relation_module = Linear(args.hidden_size, args.relation_size)
        model = RelationNetwork(encoder, relation_module, args.hidden_size, args.max_length, current_device=current_device)
    else:
        raise NotImplementedError
    if (args.optim == 'adamw'):
        optimizer = AdamW
    elif (args.optim == 'adam'):
        optimizer = torch.optim.Adam
    elif (args.optim == 'sgd'):
        optimizer = torch.optim.SGD
    else:
        raise NotImplementedError
    if (data_name == 'ARSC'):
        val_data = args.test_data
        test_data = args.test_data
    else:
        val_data = args.val_data
        test_data = args.test_data[0]
    if (not args.only_test):
        best_val_acc = train(data_name, args.train_data, val_data, tokenizer, model, args.batch_size, args.N, args.K, args.Q, optimizer, args.train_episodes, args.val_episodes, args.val_steps, args.grad_steps, args.lr, args.warmup, args.weight_decay, writer, save_checkpoint, cuda=current_cuda, fp16=False)
        logging.info('Best val mean acc: {:2.4f}'.format(best_val_acc))
        logging.info('Best model: {}'.format(save_checkpoint))
    if (test_data is not None):
        current_checkpoint = (args.load_checkpoint if args.only_test else save_checkpoint)
        if (data_name == 'ARSC'):
            (_, test_acc) = eval_ARSC(test_data, tokenizer, model, 1, args.N, args.K, args.Q, current_checkpoint, is_test=True, cuda=current_cuda)
        else:
            (_, test_acc) = eval(data_name, test_data, tokenizer, model, 1, args.N, args.K, args.Q, args.test_episodes, current_checkpoint, is_test=True, cuda=current_cuda)
        logging.info('Test mean acc: {:2.4f}'.format(test_acc))
