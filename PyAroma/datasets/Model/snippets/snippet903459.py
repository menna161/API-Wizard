import argparse
import os
import random
import numpy as np
import rouge
import torch
from torch import nn
from tqdm import tqdm
from eval_utils import format_text
from data_loader import get_paragraph_input_loader, get_fullstory_loader
from model import GPT2BaseModel, PlotMachinesModel
from generate_utils import toks_to_str
from parallel import DataParallelModel, DataParallelCriterion
from transformers import *
import shutil


def main(args):
    init(args)
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
    data_dir = args.data_dir
    if args.debug_mode:
        text_encoder = GPT2Tokenizer.from_pretrained('gpt2')
    else:
        text_encoder = GPT2Tokenizer.from_pretrained('gpt2-medium')
    text_encoder.add_special_tokens({'bos_token': '_start_', 'cls_token': '_classify_', 'eos_token': '_end_', 'additional_special_tokens': ['_kw_', '_endkw_', '_t_', '_i_', '_b_', '_c_']})
    vocab = len(text_encoder)
    datafile = (os.path.join(data_dir, 'test_encoded.csv') if args.testset else os.path.join(data_dir, 'val_encoded.csv'))
    print('Loading dataset...')
    val_loader = get_fullstory_loader(datafile, args.n_batch, text_encoder, num_workers=0, shuffle=False, gen_len=gen_len, n_ctx=n_ctx, include_kw=(not args.exclude_kw), max_size=args.max_ex)
    print(len(val_loader))
    if (args.use_model == 'plotmachines'):
        doc_model = PlotMachinesModel(args, vocab=vocab, n_ctx=n_ctx, gen_len=gen_len, lastidx=text_encoder.eos_token_id, includeprev=args.use_neighbor_feat)
    else:
        doc_model = GPT2BaseModel(args, vocab=vocab, n_ctx=n_ctx, gen_len=gen_len, lastidx=text_encoder.eos_token_id, includeprev=args.use_neighbor_feat)
    doc_model.to(device)
    if (n_gpu > 1):
        doc_model = DataParallelModel(doc_model)
    if args.debug_mode:
        gptclf = GPT2Model.from_pretrained('gpt2')
        gptclf.eval()
        device = ('cuda' if torch.cuda.is_available() else 'cpu')
        gptclf.to(device)
        gpttok = GPT2Tokenizer.from_pretrained('gpt2')
    else:
        gptclf = GPT2Model.from_pretrained('gpt2-medium')
        gptclf.eval()
        device = ('cuda' if torch.cuda.is_available() else 'cpu')
        gptclf.to(device)
        gpttok = GPT2Tokenizer.from_pretrained('gpt2-medium')
    prevloss = []
    upd = []
    (start_iter, running_loss) = (1, 0)
    load_dir = args.load_dir
    bestcheck = os.path.join(load_dir, 'checkpoint_best.pt')
    checkpoint = torch.load(bestcheck, map_location='cpu')
    state_dict = checkpoint['state_dict']
    if (n_gpu == 1):
        if ((state_dict.get('module.pos_emb_mask') is None) and (doc_model.state_dict().get('pos_emb_mask') is not None)):
            state_dict['module.pos_emb_mask'] = doc_model.state_dict().get('pos_emb_mask')
        for k in list(state_dict.keys()):
            state_dict[k[7:]] = state_dict[k]
            del state_dict[k]
    elif ((state_dict.get('module.pos_emb_mask') is None) and (doc_model.state_dict().get('module.pos_emb_mask') is not None)):
        state_dict['module.pos_emb_mask'] = doc_model.state_dict().get('module.pos_emb_mask')
    doc_model.load_state_dict(state_dict)
    print('Parallelized')
    tagset = ((['_i_'] + (args.bodynum * ['_b_'])) + ['_c_'])
    vort = ('test' if args.testset else 'val')
    generatedocs(doc_model, gptclf, gpttok, val_loader, text_encoder, device, beam, gen_len, k, p, args.decoding_strategy, os.path.join(args.save_dir, (vort + '.gens.tsv')), 'gen', 'tgt', gen_len, [], args, tags=tagset, dim=args.n_embd, save_dir=args.save_dir, localfile=os.path.join('/tmp', (vort + '.gens.tsv')))
    print('done decoding....')
