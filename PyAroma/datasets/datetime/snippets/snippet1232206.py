import transformers
import torch
import os
import json
import random
import numpy as np
import argparse
from datetime import datetime
from tqdm import tqdm
from torch.nn import DataParallel
from tokenizations import tokenization_bert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0,1,2,3', type=str, required=False, help='设置使用哪些显卡')
    parser.add_argument('--model_config', default='config/model_config_small.json', type=str, required=False, help='选择模型参数')
    parser.add_argument('--tokenizer_path', default='cache/vocab_small.txt', type=str, required=False, help='选择词库')
    parser.add_argument('--raw_data_path', default='data/eval.json', type=str, required=False, help='原始语料')
    parser.add_argument('--tokenized_data_path', default='data/tokenized_eval/', type=str, required=False, help='tokenized语料存放位置')
    parser.add_argument('--raw', action='store_true', help='是否先做tokenize')
    parser.add_argument('--batch_size', default=8, type=int, required=False, help='batch size')
    parser.add_argument('--log_step', default=1, type=int, required=False, help='多少步汇报一次')
    parser.add_argument('--stride', default=768, type=int, required=False, help='取数据的窗口步长')
    parser.add_argument('--num_pieces', default=100, type=int, required=False, help='将训练语料分成多少份')
    parser.add_argument('--min_length', default=128, type=int, required=False, help='最短收录文章长度')
    parser.add_argument('--pretrained_model', default='', type=str, required=False, help='模型起点路径')
    parser.add_argument('--output_dir', default='eval_result/', type=str, required=False, help='结果输出路径')
    args = parser.parse_args()
    print(('args:\n' + args.__repr__()))
    from tokenizations import tokenization_bert
    os.environ['CUDA_VISIBLE_DEVICES'] = args.device
    model_config = transformers.modeling_gpt2.GPT2Config.from_json_file(args.model_config)
    print(('config:\n' + model_config.to_json_string()))
    n_ctx = model_config.n_ctx
    full_tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
    full_tokenizer.model_max_length = n_ctx
    device = ('cuda' if torch.cuda.is_available() else 'cpu')
    print('using device:', device)
    raw_data_path = args.raw_data_path
    tokenized_data_path = args.tokenized_data_path
    raw = args.raw
    batch_size = args.batch_size
    log_step = args.log_step
    stride = args.stride
    num_pieces = args.num_pieces
    min_length = args.min_length
    output_dir = args.output_dir
    if (not os.path.exists(output_dir)):
        os.mkdir(output_dir)
    if raw:
        print('building files')
        build_files(data_path=raw_data_path, tokenized_data_path=tokenized_data_path, num_pieces=num_pieces, full_tokenizer=full_tokenizer, min_length=min_length)
        print('files built')
    if (not args.pretrained_model):
        print('you need to specify a trained model.')
        exit(1)
    else:
        model = transformers.modeling_gpt2.GPT2LMHeadModel.from_pretrained(args.pretrained_model)
    model.eval()
    model.to(device)
    num_parameters = 0
    parameters = model.parameters()
    for parameter in parameters:
        num_parameters += parameter.numel()
    print('number of parameters: {}'.format(num_parameters))
    multi_gpu = False
    full_len = 0
    print('calculating total steps')
    for i in tqdm(range(num_pieces)):
        with open((tokenized_data_path + 'tokenized_train_{}.txt'.format(i)), 'r') as f:
            full_len += len([int(item) for item in f.read().strip().split()])
    if (torch.cuda.device_count() > 1):
        print("Let's use", torch.cuda.device_count(), 'GPUs!')
        model = DataParallel(model)
        multi_gpu = True
    print('starting training')
    overall_step = 0
    total_loss = 0
    total_steps = 0
    now = datetime.now()
    print('time: {}'.format(now))
    piece_num = 0
    for i in range(num_pieces):
        with open((tokenized_data_path + 'tokenized_train_{}.txt'.format(i)), 'r') as f:
            line = f.read().strip()
        tokens = line.split()
        tokens = [int(token) for token in tokens]
        start_point = 0
        samples = []
        while (start_point < (len(tokens) - n_ctx)):
            samples.append(tokens[start_point:(start_point + n_ctx)])
            start_point += stride
        start_point -= stride
        last = tokens[(start_point + n_ctx):]
        last.extend([(full_tokenizer.convert_tokens_to_ids(['[PAD]']) * (n_ctx - len(last)))])
        random.shuffle(samples)
        for step in range((len(samples) // batch_size)):
            batch = samples[(step * batch_size):((step + 1) * batch_size)]
            batch_labels = []
            batch_inputs = []
            for ids in batch:
                int_ids_for_labels = [int(x) for x in ids]
                int_ids_for_inputs = [int(x) for x in ids]
                batch_labels.append(int_ids_for_labels)
                batch_inputs.append(int_ids_for_inputs)
            batch_labels = torch.tensor(batch_labels).long().to(device)
            batch_inputs = torch.tensor(batch_inputs).long().to(device)
            outputs = model.forward(input_ids=batch_inputs, labels=batch_labels)
            (loss, logits) = outputs[:2]
            if multi_gpu:
                loss = loss.mean()
            total_loss += loss
            total_steps += 1
            if (((overall_step + 1) % log_step) == 0):
                print('now time: {}:{}. Step {} of piece {}, ppl {}'.format(datetime.now().hour, datetime.now().minute, (step + 1), piece_num, torch.exp(loss)))
        piece_num += 1
    if (not os.path.exists(args.output_dir)):
        os.mkdir(args.output_dir)
    else:
        with open((args.output_dir + 'result.txt'), 'w') as f:
            f.write(np.exp((total_loss / total_steps)))
