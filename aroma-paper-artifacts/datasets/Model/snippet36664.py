import math
import os
from sacrebleu import corpus_bleu
import csv
import argparse
import logging
from tqdm import trange, tqdm
import json
import torch
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from pytorch_pretrained_bert import OpenAIGPTDoubleHeadsModel, OpenAIGPTTokenizer, OpenAIAdam, cached_path
from pytorch_pretrained_bert import GPT2LMHeadModel, GPT2Tokenizer, OpenAIGPTTokenizer, OpenAIGPTLMHeadModel


def run_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='openai-gpt', help='pretrained model name or path to local checkpoint')
    parser.add_argument('--setting', type=str, default='explain_predict')
    parser.add_argument('--n_train_print', type=int, default=10)
    parser.add_argument('--n_gen', type=int, default=20)
    parser.add_argument('--batch_size', type=int, default=(- 1))
    parser.add_argument('--length', type=int, default=(- 1))
    parser.add_argument('--temperature', type=int, default=1)
    parser.add_argument('--top_k', type=int, default=0)
    parser.add_argument('--unconditional', action='store_true', help='If true, unconditional generation.')
    parser.add_argument('--do_train', action='store_true', help='Whether to run training.')
    parser.add_argument('--do_eval', action='store_true', help='Whether to run eval on the dev set.')
    parser.add_argument('--do_test', action='store_true', help='Whether to run eval on the test set.')
    parser.add_argument('--output_dir', default=None, type=str, required=True, help='The output directory where the model predictions and checkpoints will be written.')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--num_train_epochs', type=int, default=10)
    parser.add_argument('--num_eval_print', type=int, default=15)
    parser.add_argument('--train_batch_size', type=int, default=36)
    parser.add_argument('--eval_batch_size', type=int, default=60)
    parser.add_argument('--max_grad_norm', type=int, default=1)
    parser.add_argument('--learning_rate', type=float, default=1e-06)
    parser.add_argument('--warmup_proportion', type=float, default=0.002)
    parser.add_argument('--lr_schedule', type=str, default='warmup_linear')
    parser.add_argument('--weight_decay', type=float, default=0.01)
    parser.add_argument('--data', type=str, default='/stage/examples/commonsenseqa/')
    args = parser.parse_args()
    print(args)
    if (args.batch_size == (- 1)):
        args.batch_size = 1
    np.random.seed(args.seed)
    torch.random.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
    n_gpu = torch.cuda.device_count()
    logger.info('device: {}, n_gpu {}'.format(device, n_gpu))
    if ((not args.do_train) and (not args.do_eval) and (not args.do_test)):
        raise ValueError('At least one of `do_train` or `do_eval`  or do_test must be True.')
    if (not os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)
    special_tokens = ['_start_</w>', 'or</w>', '_answer_</w>', '_classify_</w>', '_end_</w>']
    tokenizer = OpenAIGPTTokenizer.from_pretrained(args.model_name, special_tokens=special_tokens)
    special_tokens_ids = list((tokenizer.convert_tokens_to_ids(token) for token in special_tokens))
    model = OpenAIGPTLMHeadModel.from_pretrained(args.model_name, num_special_tokens=len(special_tokens))
    model.to(device)
    datasets = parse_cqa(args.data, args.setting)
    numericalized = [CommonsenseExample.numericalize_list(CommonsenseExample.tokenize_list(d, tokenizer), tokenizer) for d in datasets]
    tensor_datasets = pre_process_datasets(numericalized, *special_tokens_ids)
    if args.do_train:
        train_tensor_dataset = tensor_datasets[0]
        train_data = TensorDataset(*train_tensor_dataset)
        train_sampler = RandomSampler(train_data)
        if args.do_test_train:
            train_sampler = SequentialSampler(train_data)
        train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=args.train_batch_size)
    if args.do_eval:
        eval_tensor_dataset = tensor_datasets[1]
        eval_data = TensorDataset(*eval_tensor_dataset)
        eval_sampler = SequentialSampler(eval_data)
        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size)
    if args.do_test:
        test_tensor_dataset = tensor_datasets[(- 1)]
        test_data = TensorDataset(*test_tensor_dataset)
        test_sampler = SequentialSampler(test_data)
        test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=args.eval_batch_size)
    if args.do_train:
        param_optimizer = list(model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [{'params': [p for (n, p) in param_optimizer if (not any(((nd in n) for nd in no_decay)))], 'weight_decay': 0.01}, {'params': [p for (n, p) in param_optimizer if any(((nd in n) for nd in no_decay))], 'weight_decay': 0.0}]
        num_train_optimization_steps = ((len(train_data) * args.num_train_epochs) // args.train_batch_size)
        optimizer = OpenAIAdam(optimizer_grouped_parameters, lr=args.learning_rate, warmup=args.warmup_proportion, max_grad_norm=args.max_grad_norm, weight_decay=args.weight_decay, t_total=num_train_optimization_steps)

    def trim_unks(x):
        try:
            unk_id = x.index('_end_</w>')
            return x[:unk_id]
        except:
            return x

    def detokenize(x):
        y = ''.join(trim_unks(x))
        y = y.replace('</w>', ' ')
        y = y.replace(' .', '.')
        y = y.replace(' ,', ',')
        y = y.replace(' ?', '?')
        y = y.replace(' !', '!')
        y = y.replace(" ' ", "'")
        y = y.replace(" 're", "'re")
        y = y.replace(" 's", "'s")
        y = y.replace(" n't", "n't")
        return y

    def detok_batch(x):
        if (not isinstance(x, list)):
            x = x.tolist()
        return [detokenize(tokenizer.convert_ids_to_tokens([z for z in y if (z >= 0)])) for y in x]
    if args.do_train:
        best_eval = 0
        (nb_tr_steps, tr_loss, exp_average_loss) = (0, 0, None)
        model.train()
        for _ in range(int(args.num_train_epochs)):
            (tr_loss, train_ppl, n_train_examples) = (0, 0, 0)
            nb_tr_steps = 0
            tqdm_bar = tqdm(train_dataloader, desc='Training')
            (train_pred_strs, train_lab_strs) = ([], [])
            for (step, batch) in enumerate(tqdm_bar):
                inputs = batch[0].to(device)
                labels = batch[1].to(device)
                loss = model(inputs, lm_labels=labels)
                train_ppl += (loss.item() * inputs.size(0))
                n_train_examples += inputs.size(0)
                loss.backward()
                optimizer.step()
                tr_loss += loss.item()
                exp_average_loss = (loss.item() if (exp_average_loss is None) else ((0.7 * exp_average_loss) + (0.3 * loss.item())))
                nb_tr_steps += 1
                if (args.n_train_print > 0):
                    with torch.no_grad():
                        preds = sample(model, batch[2], 10, device)
                    pred_str = detok_batch(preds)
                    label_str = detok_batch(labels)
                    train_lab_strs.extend(label_str)
                    train_pred_strs.extend(pred_str)
                    input_str = detok_batch(inputs)
                    for print_idx in range(min(args.n_train_print, inputs.size(0))):
                        print('INPT: ', input_str[print_idx])
                        print('GOLD: ', label_str[print_idx])
                        print('PRED: ', pred_str[print_idx])
                        print()
            train_bleu = None
            if (args.n_train_print > 0):
                train_bleu = computeBLEU(train_pred_strs, [[x] for x in train_lab_strs])
                train_ppl = math.exp((train_ppl / n_train_examples))
            if args.do_eval:
                model.eval()
                (eval_loss, eval_em, eval_ppl) = (0, 0, 0)
                (nb_eval_steps, nb_eval_examples) = (0, 0)
                (label_strs, prediction_strs) = ([], [])
                n_words = 0
                for batch in eval_dataloader:
                    inputs = batch[0].to(device)
                    labels = batch[1].to(device)
                    with torch.no_grad():
                        loss = model(inputs, lm_labels=labels)
                        preds = sample(model, batch[2], args.n_gen, device)
                    eval_loss += loss.item()
                    eval_ppl += (loss.item() * inputs.size(0))
                    nb_eval_examples += inputs.size(0)
                    nb_eval_steps += 1
                    pred_str = detok_batch(preds)
                    label_str = detok_batch(labels)
                    label_strs.extend(label_str)
                    prediction_strs.extend(pred_str)
                    input_str = detok_batch(inputs)
                    eval_em += sum([(x == y) for (x, y) in zip(pred_str, label_str)])
                    for print_idx in range(min(inputs.size(0), args.num_eval_print)):
                        print('INPT: ', input_str[print_idx])
                        print('GOLD: ', label_str[print_idx])
                        print('PRED: ', pred_str[print_idx])
                        print()
                eval_bleu = computeBLEU(prediction_strs, [[x] for x in label_strs])
                eval_ppl = math.exp((eval_ppl / nb_eval_examples))
                eval_em = (eval_em / nb_eval_examples)
                eval_loss = (eval_loss / nb_eval_steps)
                train_loss = ((tr_loss / nb_tr_steps) if args.do_train else None)
                result = {'eval_loss': eval_loss, 'eval_em': eval_em, 'eval_bleu': eval_bleu, 'eval_ppl': eval_ppl, 'train_loss': train_loss, 'train_bleu': train_bleu, 'train_ppl': train_ppl}
                output_eval_file = os.path.join(args.output_dir, 'eval_results.txt')
                with open(output_eval_file, 'a') as writer:
                    for key in sorted(result.keys()):
                        logger.info('  %s = %s', key, str(result[key]))
                        writer.write(('%s = %s\n' % (key, str(result[key]))))
                if (eval_bleu > best_eval):
                    best_eval = eval_bleu
                    model_to_save = (model.module if hasattr(model, 'module') else model)
                    output_model_file = os.path.join(args.output_dir, 'pytorch_model.bin')
                    config = model.config
                    torch.save(model_to_save.state_dict(), output_model_file)
    if args.do_eval:
        output_model_file = os.path.join(args.output_dir, 'pytorch_model.bin')
        model_state_dict = torch.load(output_model_file)
        model = OpenAIGPTLMHeadModel(model.config)
        model.load_state_dict(model_state_dict)
        model.to(device)
        model.eval()
        (eval_loss, eval_em, eval_ppl) = (0, 0, 0)
        (nb_eval_steps, nb_eval_examples) = (0, 0)
        (label_strs, prediction_strs) = ([], [])
        n_words = 0
        for batch in eval_dataloader:
            inputs = batch[0].to(device)
            labels = batch[1].to(device)
            with torch.no_grad():
                loss = model(inputs, lm_labels=labels)
                preds = sample(model, batch[2], args.n_gen, device)
            eval_loss += loss.item()
            eval_ppl += (loss.item() * inputs.size(0))
            nb_eval_examples += inputs.size(0)
            nb_eval_steps += 1
            pred_str = detok_batch(preds)
            label_str = detok_batch(labels)
            label_strs.extend(label_str)
            prediction_strs.extend(pred_str)
            input_str = detok_batch(inputs)
            eval_em += sum([(x == y) for (x, y) in zip(pred_str, label_str)])
            for print_idx in range(min(inputs.size(0), args.num_eval_print)):
                print('INPT: ', input_str[print_idx])
                print('GOLD: ', label_str[print_idx])
                print('PRED: ', pred_str[print_idx])
                print()
        eval_bleu = computeBLEU(prediction_strs, [[x] for x in label_strs])
        eval_ppl = math.exp((eval_ppl / nb_eval_examples))
        eval_em = (eval_em / nb_eval_examples)
        eval_loss = (eval_loss / nb_eval_steps)
        train_loss = ((tr_loss / nb_tr_steps) if args.do_train else None)
        result = {'eval_loss': eval_loss, 'eval_em': eval_em, 'eval_bleu': eval_bleu, 'eval_ppl': eval_ppl, 'train_loss': train_loss}
        output_eval_file = os.path.join(args.output_dir, 'eval_results.txt')
        with open(output_eval_file, 'a') as writer:
            logger.info('***** Best Eval results *****')
            for key in sorted(result.keys()):
                logger.info('  %s = %s', key, str(result[key]))
                writer.write(('%s = %s\n' % (key, str(result[key]))))
        output_preds_file = os.path.join(args.output_dir, f'{args.eval_preds_prefix}_{args.setting}.txt')
        with open(output_preds_file, 'w') as writer:
            logger.info('Writing predictions')
            for p in prediction_strs:
                writer.write((p + '\n'))
    if args.do_test:
        output_model_file = os.path.join(args.output_dir, 'pytorch_model.bin')
        model_state_dict = torch.load(output_model_file)
        model = OpenAIGPTLMHeadModel(model.config)
        model.load_state_dict(model_state_dict)
        model.to(device)
        model.eval()
        (eval_loss, eval_em, eval_ppl) = (0, 0, 0)
        (nb_eval_steps, nb_eval_examples) = (0, 0)
        (label_strs, prediction_strs) = ([], [])
        n_words = 0
        for batch in test_dataloader:
            inputs = batch[0].to(device)
            with torch.no_grad():
                preds = sample(model, batch[1], args.n_gen, device)
            pred_str = detok_batch(preds)
            prediction_strs.extend(pred_str)
        output_preds_file = os.path.join(args.output_dir, f'{args.test_preds_prefix}_{args.setting}.txt')
        with open(output_preds_file, 'w') as writer:
            logger.info('Writing predictions')
            for p in prediction_strs:
                writer.write(f'''"{p.strip()}"
''')
