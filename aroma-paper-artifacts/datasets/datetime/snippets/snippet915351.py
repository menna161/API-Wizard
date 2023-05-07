import datetime
import json
import logging
import os
import random
import sys
from typing import List
import torch
import transformers
from torch.utils.data import DataLoader
from tqdm import tqdm
from machamp.utils import myutils
from machamp.model.machamp import MachampModel
from machamp.model.callback import Callback
from machamp.data.machamp_dataset_collection import MachampDatasetCollection
from machamp.utils import image
from machamp.data.machamp_sampler import MachampBatchSampler
from machamp.modules.allennlp.slanted_triangular import SlantedTriangular
from machamp.predictor.predict import predict_with_paths


def train(name: str, parameters_config_path: str, dataset_config_paths: List[str], device: str, resume: str=None, retrain: str=None, seed: int=None, cmd: str=''):
    '\n    \n    Parameters\n    ----------\n    name: str\n        The name of the model.\n    parameters_config_path: str\n        Path to the hyperparameters configuration.\n    dataset_config_paths: List[str]\n        List of paths to dataset configurations.\n    device: str\n        Description of cuda device to use, i.e.: "cpu" or "gpu:0".\n    resume: str = None\n        Resume training of an incompleted training.\n    retrain: str = None\n        If retraining from a machamp model instead of \n        a transformers model, this holds the path to the\n        previous model to use.\n    seed: int = 8446\n        Random seed, which is used for torch and the \n        random package. \n    cmd: str = \'\'\n        The command invoked to start the training\n    '
    start_time = datetime.datetime.now()
    first_epoch = 1
    if resume:
        parameters_config = myutils.load_json((resume + '/params-config.json'))
        dataset_configs = myutils.load_json((resume + '/dataset-configs.json'))
        serialization_dir = resume
        epoch = 1
        for epoch in range(1, (parameters_config['training']['num_epochs'] + 1)):
            train_state_path = os.path.join(serialization_dir, (('train_state_epoch_' + str(epoch)) + '.pt'))
            if os.path.isfile(train_state_path):
                break
        first_epoch = (epoch + 1)
    else:
        parameters_config = myutils.load_json(parameters_config_path)
        dataset_configs = myutils.merge_configs(dataset_config_paths, parameters_config)
        serialization_dir = (((('logs/' + name) + '/') + start_time.strftime('%Y.%m.%d_%H.%M.%S')) + '/')
        counter = 2
        while os.path.isdir(serialization_dir):
            serialization_dir += ('.' + str(counter))
            counter += 1
        os.makedirs(serialization_dir)
        if (seed != None):
            parameters_config['random_seed'] = seed
        json.dump(parameters_config, open((serialization_dir + '/params-config.json'), 'w'), indent=4)
        json.dump(dataset_configs, open((serialization_dir + '/dataset-configs.json'), 'w'), indent=4)
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO, handlers=[logging.FileHandler(os.path.join(serialization_dir, 'log.txt')), logging.StreamHandler(sys.stdout)])
    stderr_logger = logging.getLogger('STDERR')
    sl = myutils.StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl
    logger = logging.getLogger(__name__)
    if (cmd != ''):
        logger.info(('cmd: ' + cmd))
    if os.path.isfile('.git/logs/HEAD'):
        logger.info(('git commit ' + open('.git/logs/HEAD', encoding='utf-8', errors='ignore').readlines()[(- 1)].split(' ')[1]))
    random.seed(parameters_config['random_seed'])
    torch.manual_seed(parameters_config['random_seed'])
    batch_size = parameters_config['batching']['batch_size']
    train_dataset = MachampDatasetCollection(parameters_config['transformer_model'], dataset_configs, is_train=True, max_input_length=parameters_config['encoder']['max_input_length'], num_epochs=parameters_config['training']['num_epochs'])
    train_sampler = MachampBatchSampler(train_dataset, batch_size, parameters_config['batching']['max_tokens'], parameters_config['batching']['shuffle'], parameters_config['batching']['sampling_smoothing'], parameters_config['batching']['sort_by_size'], parameters_config['batching']['diverse'], True)
    train_dataloader = DataLoader(train_dataset, batch_sampler=train_sampler, collate_fn=(lambda x: x))
    train_dataset.vocabulary.save_vocabs(os.path.join(serialization_dir, 'vocabularies'))
    dev_dataset = MachampDatasetCollection(parameters_config['transformer_model'], dataset_configs, is_train=False, vocabulary=train_dataset.vocabulary, max_input_length=parameters_config['encoder']['max_input_length'])
    dev_sampler = MachampBatchSampler(dev_dataset, batch_size, parameters_config['batching']['max_tokens'], False, 1.0, parameters_config['batching']['sort_by_size'], False, True)
    dev_dataloader = DataLoader(dev_dataset, batch_sampler=dev_sampler, collate_fn=(lambda x: x))
    if resume:
        model_path = os.path.join(serialization_dir, (('model_' + str(epoch)) + '.pt'))
        model = torch.load(model_path)
    else:
        model = MachampModel(train_dataset.vocabulary, train_dataset.tasks, train_dataset.task_types, parameters_config['transformer_model'], device, dataset_configs, train_dataset.tokenizer, **parameters_config['encoder'], retrain=retrain, reset_transformer_model=parameters_config['reset_transformer_model'])
    first_group = []
    second_group = ['^decoders.*', 'scalars.*']
    pred_head_names = ['pred_layer', 'cls', 'lm_head', 'generator_lm_head', 'predictions', 'mlm', 'vocab_projector']
    for attribute in model.named_parameters():
        if attribute[0].startswith('mlm'):
            if (attribute[0].split('.')[1] in pred_head_names):
                second_group.append(attribute[0])
            elif ('decoder' in attribute[0]):
                second_group.append(attribute[0])
            else:
                first_group.append(attribute[0])
    parameter_groups = [[first_group, {}], [second_group, {}]]
    parameter_groups = myutils.make_parameter_groups(model.named_parameters(), parameter_groups)
    optimizer = transformers.AdamW(parameter_groups, **parameters_config['training']['optimizer'])
    scheduler = SlantedTriangular(optimizer, parameters_config['training']['num_epochs'], len(train_dataloader), **parameters_config['training']['learning_rate_scheduler'])
    callback = Callback(serialization_dir, parameters_config['training']['num_epochs'], parameters_config['training']['keep_top_n'])
    if resume:
        checkpoint = torch.load(train_state_path, map_location=device)
        callback = checkpoint['callback']
        callback.serialization_dir = serialization_dir
        optimizer.load_state_dict(checkpoint['optimizer'])
        scheduler.load_state_dict(checkpoint['scheduler'])
        del checkpoint
    model.to(device)
    logger.info('MaChAmp succesfully initialized in {:.1f}s'.format((datetime.datetime.now() - start_time).seconds))
    logger.info(image.machamp)
    logger.info('starting training...')
    for epoch in range(first_epoch, (parameters_config['training']['num_epochs'] + 1)):
        logger.info((((('Epoch ' + str(epoch)) + '/') + str(parameters_config['training']['num_epochs'])) + ': training'))
        callback.start_epoch_timer()
        model.train()
        model.reset_metrics()
        total_train_losses = {}
        train_batch_idx = 0
        for (train_batch_idx, batch) in enumerate(tqdm(train_dataloader, file=sys.stdout)):
            optimizer.zero_grad()
            if (len(batch) == 0):
                continue
            batch = myutils.prep_batch(batch, device, train_dataset)
            (loss, _, _, _, _, loss_dict) = model.forward(batch['token_ids'], batch['golds'], batch['seg_ids'], batch['offsets'], batch['subword_mask'], batch['task_masks'], batch['word_mask'])
            for task in loss_dict:
                if (task not in total_train_losses):
                    total_train_losses[task] = 0.0
                total_train_losses[task] += loss_dict[task]
            loss.backward()
            scheduler.step_batch()
            optimizer.step()
        scheduler.step()
        train_metrics = model.get_metrics()
        avg_train_losses = {x: (total_train_losses[x] / (train_batch_idx + 1)) for x in total_train_losses}
        avg_train_losses['sum'] = sum(avg_train_losses.values())
        callback.add_train_results(epoch, avg_train_losses, train_metrics)
        if (len(dev_dataset) > 0):
            logger.info((('Epoch ' + str(epoch)) + ': evaluating on dev'))
            model.eval()
            model.reset_metrics()
            total_dev_losses = evaluate(dev_dataloader, model, train_dataset)
            dev_metrics = model.get_metrics()
            callback.add_dev_results(epoch, total_dev_losses, dev_metrics)
        callback.end_epoch(epoch, model)
        estimated_total_time = ((datetime.datetime.now() - callback.epoch_start_time).seconds * parameters_config['training']['num_epochs'])
        if (estimated_total_time > (45 * 60)):
            state_path = os.path.join(serialization_dir, (('train_state_epoch_' + str(epoch)) + '.pt'))
            logger.info('Saving training state, so that we can use --resume if needed')
            logger.info(('Path: ' + state_path))
            torch.save({'callback': callback, 'optimizer': optimizer.state_dict(), 'scheduler': scheduler.state_dict()}, state_path)
        prev_state_path = os.path.join(serialization_dir, (('train_state_epoch_' + str((epoch - 1))) + '.pt'))
        if os.path.isfile(prev_state_path):
            logger.info('Removing old training state.')
            logger.info(('Path: ' + prev_state_path))
            os.remove(prev_state_path)
    state_path = os.path.join(serialization_dir, (('train_state_epoch_' + str(epoch)) + '.pt'))
    if os.path.isfile(state_path):
        os.remove(state_path)
    scalars = {}
    for task in model.scalars:
        if (model.scalars[task] != None):
            scalars[task] = torch.nn.functional.softmax(model.scalars[task].scalar_parameters.data).tolist()
    json.dump(scalars, open(os.path.join(serialization_dir, 'scalars.json'), 'w'), indent=4)
    if (len(dev_dataset) > 0):
        logger.info(('Predicting on dev set' + ('s' * (len(dev_dataloader.dataset.datasets) > 1))))
        del model
        del train_dataloader
        del train_sampler
        del optimizer
        model = torch.load(os.path.join(serialization_dir, 'model.pt'), map_location=device)
        for dataset_name in dataset_configs:
            model.reset_metrics()
            task_types = [dataset_configs[dataset_name]['tasks'][task]['task_type'] for task in dataset_configs[dataset_name]['tasks']]
            if (('dev_data_path' in dataset_configs[dataset_name]) and ('mlm' not in task_types)):
                in_path = dataset_configs[dataset_name]['dev_data_path']
                out_path = os.path.join(serialization_dir, (dataset_name + '.out'))
                predict_with_paths(model, in_path, out_path, dataset_name, batch_size, False, device)
    return os.path.join(serialization_dir, 'model.pt')
