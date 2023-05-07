import argparse
import csv
import json
import logging
import os
import random
import sys
from io import open
import re
import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from tqdm import tqdm, trange
from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE
from pytorch_pretrained_bert.modeling import BertForMultipleChoice, WEIGHTS_NAME, CONFIG_NAME, BertConfig
from pytorch_pretrained_bert.optimization import BertAdam, warmup_linear
from pytorch_pretrained_bert.tokenization import BertTokenizer
from apex.parallel import DistributedDataParallel as DDP
from apex.optimizers import FP16_Optimizer
from apex.optimizers import FusedAdam


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default=None, type=str, required=True, help='The input data dir. Should contain the .csv files (or other data files) for the task.')
    parser.add_argument('--bert_model', default=None, type=str, required=True, help='Bert pre-trained model selected in the list: bert-base-uncased, bert-large-uncased, bert-base-cased, bert-large-cased, bert-base-multilingual-uncased, bert-base-multilingual-cased, bert-base-chinese.')
    parser.add_argument('--output_dir', default=None, type=str, required=True, help='The output directory where the model checkpoints will be written.')
    parser.add_argument('--save_model_name', default='model', type=str, required=True, help='The output model name where the model checkpoints will be written.')
    parser.add_argument('--max_seq_length', default=128, type=int, help='The maximum total input sequence length after WordPiece tokenization. \nSequences longer than this will be truncated, and sequences shorter \nthan this will be padded.')
    parser.add_argument('--do_train', action='store_true', help='Whether to run training.')
    parser.add_argument('--wsc', action='store_true', help='Whether to run training with wsc.')
    parser.add_argument('--swag_transfer', action='store_true', help='Whether to run training with swag.')
    parser.add_argument('--inhouse', action='store_true', help='Whether to run eval on the inhouse train/dev set.')
    parser.add_argument('--do_eval', action='store_true', help='Whether to run eval on the dev set.')
    parser.add_argument('--do_test', action='store_true', help='Whether to run test on the test set.')
    parser.add_argument('--do_lower_case', action='store_true', help='Set this flag if you are using an uncased model.')
    parser.add_argument('--train_batch_size', default=32, type=int, help='Total batch size for training.')
    parser.add_argument('--eval_batch_size', default=8, type=int, help='Total batch size for eval.')
    parser.add_argument('--epoch_suffix', default=0, type=int, help='Epoch suffix number.')
    parser.add_argument('--learning_rate', default=0.0001, type=float, help='The initial learning rate for Adam.')
    parser.add_argument('--mlp_hidden_dim', default=64, type=int, help='mlp_hidden_dim.')
    parser.add_argument('--mlp_dropout', default=0.1, type=float, help='hidden drop out')
    parser.add_argument('--weight_decay', default=0.01, type=float, help='Weight decay for optimization')
    parser.add_argument('--num_train_epochs', default=3.0, type=float, help='Total number of training epochs to perform.')
    parser.add_argument('--warmup_proportion', default=0.1, type=float, help='Proportion of training to perform linear learning rate warmup for. E.g., 0.1 = 10%% of training.')
    parser.add_argument('--no_cuda', action='store_true', help='Whether not to use CUDA when available')
    parser.add_argument('--local_rank', type=int, default=(- 1), help='local_rank for distributed training on gpus')
    parser.add_argument('--seed', type=int, default=42, help='random seed for initialization')
    parser.add_argument('--patience', type=int, default=5, help='early stop epoch nums on dev')
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1, help='Number of updates steps to accumulate before performing a backward/update pass.')
    parser.add_argument('--fp16', action='store_true', help='Whether to use 16-bit float precision instead of 32-bit')
    parser.add_argument('--loss_scale', type=float, default=0, help='Loss scaling to improve fp16 numeric stability. Only used when fp16 set to True.\n0 (default value): dynamic loss scaling.\nPositive power of 2: static loss scaling value.\n')
    args = parser.parse_args()
    print('torch.cuda.is_available()', torch.cuda.is_available())
    if ((args.local_rank == (- 1)) or args.no_cuda):
        device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
        n_gpu = torch.cuda.device_count()
    else:
        torch.cuda.set_device(args.local_rank)
        device = torch.device('cuda', args.local_rank)
        n_gpu = 1
        torch.distributed.init_process_group(backend='nccl')
    logger.info('device: {} n_gpu: {}, distributed training: {}, 16-bits training: {}'.format(device, n_gpu, bool((args.local_rank != (- 1))), args.fp16))
    if (args.gradient_accumulation_steps < 1):
        raise ValueError('Invalid gradient_accumulation_steps parameter: {}, should be >= 1'.format(args.gradient_accumulation_steps))
    args.train_batch_size = (args.train_batch_size // args.gradient_accumulation_steps)
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if (n_gpu > 0):
        torch.cuda.manual_seed_all(args.seed)
    if ((not args.do_train) and (not args.do_eval) and (not args.do_test)):
        raise ValueError('At least one of `do_train` or `do_eval` must be True.')
    if (os.path.exists(args.output_dir) and os.listdir(args.output_dir)):
        print('WARNING: Output directory ({}) already exists and is not empty.'.format(args.output_dir))
    if (not os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)
    tokenizer = BertTokenizer.from_pretrained(args.bert_model, do_lower_case=args.do_lower_case)
    train_examples = None
    num_train_optimization_steps = None
    if args.do_train:
        ori_train_examples = read_csqa_examples(os.path.join(args.data_dir, 'train_rand_split.jsonl'))
        ori_dev_examples = read_csqa_examples(os.path.join(args.data_dir, 'dev_rand_split.jsonl'))
        ori_test_examples = read_csqa_examples(os.path.join(args.data_dir, 'train2_rand_split.jsonl'))
        if args.inhouse:
            train_examples = ori_train_examples[0:850]
            test_examples = ori_train_examples[8500:]
            dev_examples = ori_dev_examples[:]
        else:
            train_examples = ori_train_examples[:]
            dev_examples = ori_dev_examples[:]
        num_train_optimization_steps = (int(((len(train_examples) / args.train_batch_size) / args.gradient_accumulation_steps)) * args.num_train_epochs)
        if (args.local_rank != (- 1)):
            num_train_optimization_steps = (num_train_optimization_steps // torch.distributed.get_world_size())
    model = BertForMultipleChoice.from_pretrained(args.bert_model, cache_dir=os.path.join(PYTORCH_PRETRAINED_BERT_CACHE, 'distributed_{}'.format(args.local_rank)), num_choices=5, mlp_hidden_dim=args.mlp_hidden_dim, mlp_dropout=args.mlp_dropout)
    if args.fp16:
        model.half()
    model.to(device)
    if (args.local_rank != (- 1)):
        try:
            from apex.parallel import DistributedDataParallel as DDP
        except ImportError:
            raise ImportError('Please install apex from https://www.github.com/nvidia/apex to use distributed and fp16 training.')
        model = DDP(model)
    elif (n_gpu > 1):
        model = torch.nn.DataParallel(model)
    param_optimizer = list(model.named_parameters())
    param_optimizer = [n for n in param_optimizer if ('pooler' not in n[0])]
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [{'params': [p for (n, p) in param_optimizer if (not any(((nd in n) for nd in no_decay)))], 'weight_decay': args.weight_decay}, {'params': [p for (n, p) in param_optimizer if any(((nd in n) for nd in no_decay))], 'weight_decay': 0.0}]
    if args.fp16:
        try:
            from apex.optimizers import FP16_Optimizer
            from apex.optimizers import FusedAdam
        except ImportError:
            raise ImportError('Please install apex from https://www.github.com/nvidia/apex to use distributed and fp16 training.')
        optimizer = FusedAdam(optimizer_grouped_parameters, lr=args.learning_rate, bias_correction=False, max_grad_norm=1.0)
        if (args.loss_scale == 0):
            optimizer = FP16_Optimizer(optimizer, dynamic_loss_scale=True)
        else:
            optimizer = FP16_Optimizer(optimizer, static_loss_scale=args.loss_scale)
    else:
        optimizer = BertAdam(optimizer_grouped_parameters, lr=args.learning_rate, warmup=args.warmup_proportion, t_total=num_train_optimization_steps)
    global_step = 0
    if args.do_train:
        train_features = convert_examples_to_features(train_examples, tokenizer, args.max_seq_length, True)
        dev_features = convert_examples_to_features(dev_examples, tokenizer, args.max_seq_length, True)
        train_dataloader = get_train_dataloader(train_features, args)
        dev_dataloader = get_eval_dataloader(dev_features, args)
        if args.inhouse:
            test_features = convert_examples_to_features(test_examples, tokenizer, args.max_seq_length, True)
            test_dataloader = get_eval_dataloader(test_features, args)
        logger.info('***** Running training *****')
        logger.info('  Num examples = %d', len(train_examples))
        logger.info('  Batch size = %d', args.train_batch_size)
        logger.info('  Num steps = %d', num_train_optimization_steps)
        logger.info('')
        logger.info('  Num train features = %d', len(train_features))
        logger.info('  Num dev features = %d', len(dev_features))
        best_dev_accuracy = 0
        best_dev_epoch = 0
        no_up = 0
        epoch_tqdm = trange(int(args.num_train_epochs), desc='Epoch')
        for epoch in epoch_tqdm:
            model.train()
            tr_loss = 0
            (nb_tr_examples, nb_tr_steps) = (0, 0)
            for (step, batch) in enumerate(tqdm(train_dataloader, desc='Iteration')):
                batch = tuple((t.to(device) for t in batch))
                (input_ids, input_mask, segment_ids, label_ids) = batch
                loss = model(input_ids, segment_ids, input_mask, label_ids)
                if (n_gpu > 1):
                    loss = loss.mean()
                if (args.fp16 and (args.loss_scale != 1.0)):
                    loss = (loss * args.loss_scale)
                if (args.gradient_accumulation_steps > 1):
                    loss = (loss / args.gradient_accumulation_steps)
                tr_loss += loss.item()
                nb_tr_examples += input_ids.size(0)
                nb_tr_steps += 1
                if args.fp16:
                    optimizer.backward(loss)
                else:
                    loss.backward()
                if (((step + 1) % args.gradient_accumulation_steps) == 0):
                    if args.fp16:
                        lr_this_step = (args.learning_rate * warmup_linear((global_step / num_train_optimization_steps), args.warmup_proportion))
                        for param_group in optimizer.param_groups:
                            param_group['lr'] = lr_this_step
                    optimizer.step()
                    optimizer.zero_grad()
                    global_step += 1
            (dev_loss, dev_accuracy) = evaluate(model, device, dev_dataloader, desc='Evaluate Dev')
            if args.inhouse:
                (test_loss, test_accuracy) = evaluate(model, device, test_dataloader, desc='Evaluate Test')
            if (dev_accuracy > best_dev_accuracy):
                best_dev_accuracy = dev_accuracy
                best_dev_epoch = (epoch + 1)
                no_up = 0
                model_to_save = (model.module if hasattr(model, 'module') else model)
                output_model_file = os.path.join(args.output_dir, (args.save_model_name + ('.bin.%d' % epoch)))
                torch.save(model_to_save.state_dict(), output_model_file)
                output_config_file = os.path.join(args.output_dir, (args.save_model_name + '.config'))
                with open(output_config_file, 'w') as fpp:
                    fpp.write(model_to_save.config.to_json_string())
            else:
                no_up += 1
            tqdm.write(('\t ***** Eval results (Epoch %s) *****' % str((epoch + 1))))
            tqdm.write(('\t dev_accuracy = %s' % str(dev_accuracy)))
            tqdm.write('')
            if args.inhouse:
                tqdm.write(('\t test_accuracy = %s' % str(test_accuracy)))
                tqdm.write('')
            tqdm.write(('\t best_dev_accuracy = %s' % str(best_dev_accuracy)))
            tqdm.write(('\t best_dev_epoch = %s' % str(best_dev_epoch)))
            tqdm.write(('\t no_up = %s' % str(no_up)))
            tqdm.write('')
            if (no_up >= args.patience):
                epoch_tqdm.close()
                break
    model.to(device)
    if (args.do_eval and ((args.local_rank == (- 1)) or (torch.distributed.get_rank() == 0))):
        output_model_file = os.path.join(args.output_dir, (args.save_model_name + ('.bin.%d' % args.epoch_suffix)))
        output_config_file = os.path.join(args.output_dir, (args.save_model_name + '.config'))
        config = BertConfig(output_config_file)
        model = BertForMultipleChoice(config, num_choices=5, mlp_hidden_dim=args.mlp_hidden_dim, mlp_dropout=args.mlp_dropout)
        model.load_state_dict(torch.load(output_model_file))
        model.to(device)
        if args.wsc:
            eval_examples = read_csqa_examples('../datasets/wsc.jsonl')
        elif args.swag_transfer:
            eval_examples = read_csqa_examples('../datasets/swagaf/data/val.jsonl')
        else:
            eval_examples = read_csqa_examples(os.path.join(args.data_dir, 'dev_rand_split.jsonl'))
        eval_features = convert_examples_to_features(eval_examples, tokenizer, args.max_seq_length, True)
        if args.inhouse:
            eval_examples_test = read_csqa_examples(os.path.join(args.data_dir, 'train_rand_split.jsonl'))[8500:]
            eval_features_test = convert_examples_to_features(eval_examples_test, tokenizer, args.max_seq_length, True)
        logger.info('***** Running evaluation *****')
        logger.info('  Num examples = %d', len(eval_examples))
        logger.info('  Batch size = %d', args.eval_batch_size)
        all_input_ids = torch.tensor(select_field(eval_features, 'input_ids'), dtype=torch.long)
        all_input_mask = torch.tensor(select_field(eval_features, 'input_mask'), dtype=torch.long)
        all_segment_ids = torch.tensor(select_field(eval_features, 'segment_ids'), dtype=torch.long)
        all_label = torch.tensor([f.label for f in eval_features], dtype=torch.long)
        eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label)
        eval_sampler = SequentialSampler(eval_data)
        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
        model.eval()
        (eval_loss, eval_accuracy) = (0, 0)
        (nb_eval_steps, nb_eval_examples) = (0, 0)
        test_outputs = []
        for (input_ids, input_mask, segment_ids, label_ids) in tqdm(eval_dataloader, desc='evaluating'):
            input_ids = input_ids.to(device)
            input_mask = input_mask.to(device)
            segment_ids = segment_ids.to(device)
            label_ids = label_ids.to(device)
            with torch.no_grad():
                tmp_eval_loss = model(input_ids, segment_ids, input_mask, label_ids)
                logits = model(input_ids, segment_ids, input_mask)
            logits = logits.detach().cpu().numpy()
            outputs = np.argmax(logits, axis=1)
            test_outputs += list(outputs)
            label_ids = label_ids.to('cpu').numpy()
            tmp_eval_accuracy = accuracy(logits, label_ids)
            eval_loss += tmp_eval_loss.mean().item()
            eval_accuracy += tmp_eval_accuracy
            nb_eval_examples += input_ids.size(0)
            nb_eval_steps += 1
        eval_loss = (eval_loss / nb_eval_steps)
        eval_accuracy = (eval_accuracy / nb_eval_examples)
        if args.wsc:
            result = {'eval_accuracy': eval_accuracy}
            logger.info('***** Eval results *****')
            for key in sorted(result.keys()):
                logger.info('  %s = %s', key, str(result[key]))
            test_output_file = os.path.join(args.output_dir, (args.save_model_name + '_wsc_prediction.csv'))
            with open(test_output_file, 'w') as fout:
                with open(os.path.join('../datasets/wsc.jsonl'), 'r', encoding='utf-8') as fin:
                    examples = []
                    for (i, line) in enumerate(fin.readlines()):
                        csqa_json = json.loads(line)
                        label_pred = chr((ord('A') + test_outputs[i]))
                        if (label_pred in ['C', 'E']):
                            label_pred = 'A'
                        if (label_pred in ['D']):
                            label_pred = 'B'
                        fout.write((((csqa_json['id'] + ',') + str(label_pred)) + '\n'))
        elif args.swag_transfer:
            result = {'eval_accuracy': eval_accuracy}
            logger.info('***** Eval results *****')
            for key in sorted(result.keys()):
                logger.info('  %s = %s', key, str(result[key]))
            test_output_file = os.path.join(args.output_dir, (args.save_model_name + '_swag_val.csv'))
            with open(test_output_file, 'w') as fout:
                with open(os.path.join('../datasets/swagaf/data/val.jsonl'), 'r', encoding='utf-8') as fin:
                    examples = []
                    for (i, line) in enumerate(fin.readlines()):
                        csqa_json = json.loads(line)
                        label_pred = chr((ord('A') + test_outputs[i]))
                        if (label_pred == 'E'):
                            label_pred = 'A'
                        fout.write((((csqa_json['id'] + ',') + str(label_pred)) + '\n'))
        elif args.inhouse:
            dev_result = {'dev_eval_accuracy': eval_accuracy}
            logger.info('***** Running evaluation *****')
            logger.info('  Num examples = %d', len(eval_examples))
            logger.info('  Batch size = %d', args.eval_batch_size)
            all_input_ids = torch.tensor(select_field(eval_features_test, 'input_ids'), dtype=torch.long)
            all_input_mask = torch.tensor(select_field(eval_features_test, 'input_mask'), dtype=torch.long)
            all_segment_ids = torch.tensor(select_field(eval_features_test, 'segment_ids'), dtype=torch.long)
            all_label = torch.tensor([f.label for f in eval_features_test], dtype=torch.long)
            eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label)
            eval_sampler = SequentialSampler(eval_data)
            eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
            model.eval()
            (eval_loss, eval_accuracy) = (0, 0)
            (nb_eval_steps, nb_eval_examples) = (0, 0)
            test_outputs = []
            for (input_ids, input_mask, segment_ids, label_ids) in eval_dataloader:
                input_ids = input_ids.to(device)
                input_mask = input_mask.to(device)
                segment_ids = segment_ids.to(device)
                label_ids = label_ids.to(device)
                with torch.no_grad():
                    tmp_eval_loss = model(input_ids, segment_ids, input_mask, label_ids)
                    logits = model(input_ids, segment_ids, input_mask)
                logits = logits.detach().cpu().numpy()
                outputs = np.argmax(logits, axis=1)
                test_outputs += list(outputs)
                label_ids = label_ids.to('cpu').numpy()
                tmp_eval_accuracy = accuracy(logits, label_ids)
                eval_loss += tmp_eval_loss.mean().item()
                eval_accuracy += tmp_eval_accuracy
                nb_eval_examples += input_ids.size(0)
                nb_eval_steps += 1
            eval_loss = (eval_loss / nb_eval_steps)
            eval_accuracy = (eval_accuracy / nb_eval_examples)
            test_result = {'test_eval_accuracy': eval_accuracy}
            with open(output_eval_file, 'w') as writer:
                logger.info('***** Eval results *****')
                for key in sorted(result.keys()):
                    logger.info('  %s = %s', key, str(result[key]))
                    writer.write(('%s = %s\n' % (key, str(result[key]))))
        else:
            result = {'eval_accuracy': eval_accuracy}
            test_output_file = os.path.join(args.output_dir, (args.save_model_name + '_dev_output.csv'))
            with open(test_output_file, 'w') as fout:
                with open(os.path.join(args.data_dir, 'dev_rand_split.jsonl'), 'r', encoding='utf-8') as fin:
                    examples = []
                    for (i, line) in enumerate(fin.readlines()):
                        csqa_json = json.loads(line)
                        label_pred = chr((ord('A') + test_outputs[i]))
                        fout.write((((csqa_json['id'] + ',') + str(label_pred)) + '\n'))
            output_eval_file = os.path.join(args.output_dir, (args.save_model_name + '_res_on_dev.txt'))
            with open(output_eval_file, 'w') as writer:
                logger.info('***** Eval results *****')
                for key in sorted(result.keys()):
                    logger.info('  %s = %s', key, str(result[key]))
                    writer.write(('%s = %s\n' % (key, str(result[key]))))
    if (args.do_test and ((args.local_rank == (- 1)) or (torch.distributed.get_rank() == 0))):
        output_model_file = os.path.join(args.output_dir, (args.save_model_name + ('.bin.%d' % args.epoch_suffix)))
        output_config_file = os.path.join(args.output_dir, (args.save_model_name + '.config'))
        config = BertConfig(output_config_file)
        model = BertForMultipleChoice(config, num_choices=5, mlp_hidden_dim=args.mlp_hidden_dim, mlp_dropout=args.mlp_dropout)
        model.load_state_dict(torch.load(output_model_file))
        model.to(device)
        eval_examples = read_csqa_examples(os.path.join(args.data_dir, 'test_rand_split_no_answers.jsonl'), have_answer=False)
        eval_features = convert_examples_to_features(eval_examples, tokenizer, args.max_seq_length, True)
        logger.info('***** Running evaluation *****')
        logger.info('  Num examples = %d', len(eval_examples))
        logger.info('  Batch size = %d', args.eval_batch_size)
        all_input_ids = torch.tensor(select_field(eval_features, 'input_ids'), dtype=torch.long)
        all_input_mask = torch.tensor(select_field(eval_features, 'input_mask'), dtype=torch.long)
        all_segment_ids = torch.tensor(select_field(eval_features, 'segment_ids'), dtype=torch.long)
        all_label = torch.tensor([f.label for f in eval_features], dtype=torch.long)
        eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label)
        eval_sampler = SequentialSampler(eval_data)
        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
        model.eval()
        test_outputs = []
        for (input_ids, input_mask, segment_ids, label_ids) in eval_dataloader:
            input_ids = input_ids.to(device)
            input_mask = input_mask.to(device)
            segment_ids = segment_ids.to(device)
            with torch.no_grad():
                logits = model(input_ids, segment_ids, input_mask)
            logits = logits.detach().cpu().numpy()
            outputs = np.argmax(logits, axis=1)
            test_outputs += list(outputs)
        test_output_file = os.path.join(args.output_dir, (args.save_model_name + '_test_output.csv'))
        with open(test_output_file, 'w') as fout:
            with open(os.path.join(args.data_dir, 'test_rand_split_no_answers.jsonl'), 'r', encoding='utf-8') as fin:
                examples = []
                for (i, line) in enumerate(fin.readlines()):
                    csqa_json = json.loads(line)
                    label_pred = chr((ord('A') + test_outputs[i]))
                    fout.write((((csqa_json['id'] + ',') + str(label_pred)) + '\n'))
