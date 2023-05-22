import shutil
import argparse
import os
import random
import numpy as np
import rouge
import torch
from torch import nn
from tqdm import tqdm
import math
from data_loader import get_paragraph_input_loader, get_paragraph_memory_input_loader
from eval_utils import format_text, evaluate_doc_model
from generate_utils import generate_paragraph
from model import GPT2BaseModel, PlotMachinesModel
from logger import Logger
from loss import ParagraphLoss
from parallel import DataParallelModel, DataParallelCriterion
from transformers import *


def main(args):
    init(args)
    save_dir = os.path.join(args.output_dir, args.experiment_name, 'checkpoints')
    save_dir_local = 'checkpoints_local'
    desc = args.desc
    data_dir = args.data_dir
    log_dir = os.path.join(args.output_dir, args.experiment_name, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(save_dir_local, exist_ok=True)
    train_log_interval = args.train_log_interval
    val_log_interval = args.val_log_interval
    beam = args.beam
    p = args.p
    n_ctx = args.n_ctx
    gen_len = args.gen_len
    k = args.k
    decoding_strategy = args.decoding_strategy
    accum_iter = args.accum_iter
    device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
    n_gpu = torch.cuda.device_count()
    print('device', device, 'n_gpu', n_gpu)
    logger = Logger(log_dir)
    if args.use_offline_gpt2:
        text_encoder = GPT2Tokenizer.from_pretrained('./gpt2model')
    elif args.debug_mode:
        text_encoder = GPT2Tokenizer.from_pretrained('gpt2')
    else:
        text_encoder = GPT2Tokenizer.from_pretrained('gpt2-medium')
    text_encoder.add_special_tokens({'bos_token': '_start_', 'cls_token': '_classify_', 'eos_token': '_end_', 'additional_special_tokens': ['_kw_', '_endkw_', '_t_', '_i_', '_b_', '_c_']})
    vocab = len(text_encoder)
    print('Loading dataset...')
    if (args.use_model == 'base'):
        train_loader = get_paragraph_input_loader(os.path.join(data_dir, 'train_encoded.csv'), args.n_batch, text_encoder, num_workers=3, shuffle=True, gen_len=gen_len, n_ctx=n_ctx, include_discourse_type=args.use_discourse, include_neigh=args.use_neighbor_feat, max_size=args.max_ex, include_kw=(not args.exclude_kw), dim=args.n_embd, debug_mode=args.debug_mode)
        val_loader = get_paragraph_input_loader(os.path.join(data_dir, 'val_encoded.csv'), n_gpu, text_encoder, num_workers=0, shuffle=False, gen_len=gen_len, n_ctx=n_ctx, include_discourse_type=args.use_discourse, include_neigh=args.use_neighbor_feat, max_size=args.num_val_examples, include_kw=(not args.exclude_kw), dim=args.n_embd, debug_mode=args.debug_mode)
        print('Train length: {}, Validation length: {}'.format(len(train_loader), len(val_loader)))
        doc_model = GPT2BaseModel(args, vocab=vocab, n_ctx=n_ctx, gen_len=gen_len, lastidx=text_encoder.eos_token_id, includeprev=args.use_neighbor_feat, use_offline_gpt2=args.use_offline_gpt2)
    elif (args.use_model == 'plotmachines'):
        train_loader = get_paragraph_memory_input_loader(os.path.join(data_dir, 'train_encoded.csv'), args.n_batch, text_encoder, num_workers=3, shuffle=True, gen_len=gen_len, n_ctx=n_ctx, include_discourse_type=args.use_discourse, include_neigh=args.use_neighbor_feat, max_size=args.max_ex, include_kw=(not args.exclude_kw), memsize=args.memstatesize, dim=args.n_embd, use_kwmem=True, debug_mode=args.debug_mode)
        val_loader = get_paragraph_memory_input_loader(os.path.join(data_dir, 'val_encoded.csv'), n_gpu, text_encoder, num_workers=0, shuffle=False, gen_len=gen_len, n_ctx=n_ctx, include_discourse_type=args.use_discourse, include_neigh=args.use_neighbor_feat, max_size=args.num_val_examples, include_kw=(not args.exclude_kw), memsize=args.memstatesize, dim=args.n_embd, use_kwmem=True, debug_mode=args.debug_mode)
        print('Train length: {}, Validation length: {}'.format(len(train_loader), len(val_loader)))
        doc_model = PlotMachinesModel(args, vocab=vocab, n_ctx=n_ctx, gen_len=gen_len, lastidx=text_encoder.eos_token_id, includeprev=args.use_neighbor_feat, use_offline_gpt2=args.use_offline_gpt2)
    n_updates_total = ((len(train_loader) // args.accum_iter) * args.num_epochs)
    if args.debug_mode:
        print_model_params(log_dir, doc_model)
    criterion = nn.CrossEntropyLoss(reduction='none')
    model_opt = AdamW(filter((lambda p: p.requires_grad), doc_model.parameters()), lr=args.lr, betas=(args.b1, args.b2), eps=args.e)
    lm_loss = ParagraphLoss(criterion, n_ctx=n_ctx, gen_len=gen_len)
    print('Loading Model')
    doc_model.to(device)
    if (n_gpu > 1):
        doc_model = DataParallelModel(doc_model)
        lm_loss = DataParallelCriterion(lm_loss)
    print('Parallelized')
    bestloss = (- 1)
    (start_iter, running_loss) = (1, 0)
    prevloss = 1000
    (start_iter, running_loss) = load_checkpoint(args.checkpoint, doc_model, model_opt)
    for i in range(args.num_epochs):
        (start_iter, running_loss, bestloss, updates, val_loss1) = run_epoch(bestloss, start_iter, running_loss, doc_model, lm_loss, model_opt, train_loader, val_loader, train_log_interval, val_log_interval, device, beam, gen_len, k, p, decoding_strategy, accum_iter, 'FT Training Epoch [{}/{}]'.format((i + 1), args.num_epochs), save_dir, logger, text_encoder, show_progress=args.show_progress, my_local_dir=save_dir_local)
        print('VAL LOSS: ', str(val_loss1))
        if ((val_loss1 > prevloss) or math.isnan(val_loss1)):
            break
        prevloss = val_loss1
    print('Done training...')
    print('Evaluating on validation with best checkpoint...')
    bestcheck = os.path.join(save_dir, 'checkpoint_best.pt')
    checkpoint = torch.load(bestcheck, map_location='cpu')
    state_dict = checkpoint['state_dict']
    if ((state_dict.get('module.pos_emb_mask') is None) and (doc_model.state_dict().get('module.pos_emb_mask') is not None)):
        state_dict['module.pos_emb_mask'] = doc_model.state_dict().get('module.pos_emb_mask')
    doc_model.load_state_dict(state_dict)
    evaluate_doc_model(doc_model, val_loader, text_encoder, device, beam, gen_len, k, p, args.decoding_strategy, os.path.join(save_dir, 'valeval.log'), 'gen', 'tgt', gen_len, [], args)
