import pickle
from time import time
import abc
import traceback
import datetime
import socket
import subprocess
import os
import sys
import pprint
import argparse
import re
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.client import timeline
from dataset import Dataset, SupervisedDataset
import optimizer
from main_model import abstract_main_model, distmult_model, complex_model, supervised_model
from aux_model.decision_tree_model import DecisionTreeModel
from aux_model.supervised_decision_tree_model import SupervisedDecisionTreeModel
from aux_model.baselines import UniformAuxModel, FrequencyAuxModel
import evaluate


def train(arg_parser):
    'Create an instance of model with the command line arguments and train it.\n\n    Arguments:\n    arg_parser -- An `argparse.ArgumentParser`.\n    '
    args = arg_parser.parse_args()
    if (not args.em):
        args.num_samples = 1
    if (args.model == 'DistMult'):
        Model = distmult_model.DistMultModel
    elif (args.model == 'ComplEx'):
        Model = complex_model.ComplExModel
    elif (args.model in ['supervised', 'supervised_nce']):
        Model = supervised_model.SupervisedModel
    if ((args.aux_model is not None) and (args.neg_samples is None)):
        raise 'ERROR: --aux_model provided but --neg_samples not set.'
    if ((args.aux_model is not None) and (args.num_samples != 1)):
        raise 'ERROR: --aux_model currently only implemented for --num_samples 1.'
    if (args.rng_seed is None):
        args.rng_seed = int.from_bytes(os.urandom(4), byteorder='little')
    rng = random.Random(args.rng_seed)
    tf.set_random_seed(rng.randint(0, ((2 ** 32) - 1)))
    try:
        os.mkdir(args.output)
    except OSError:
        if (not args.force):
            sys.stderr.write(('ERROR: Cannot create output directory %s\n' % args.output))
            sys.stderr.write('HINT: Does the directory already exist? To prevent accidental data loss this\n      script, by default, does not write to an existing output directory.\n      Specify a non-existing output directory or use the `--force`.\n')
            exit(1)
    else:
        print(('Writing output into directory `%s`.' % args.output))
    try:
        with open(os.path.join(args.output, 'log'), 'w') as log_file:
            log_file.write('#!/usr/bin/python\n')
            log_file.write('\n')
            log_file.write(('program = "%s"\n' % arg_parser.prog))
            log_file.write(('args = {\n %s\n}\n\n' % pprint.pformat(vars(args), indent=4)[1:(- 1)]))
            try:
                git_revision = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
                log_file.write(('git_revision = "%s"\n' % git_revision))
            except:
                pass
            log_file.write(('host_name = "%s"\n' % socket.gethostname()))
            log_file.write(('start_time = "%s"\n' % str(datetime.datetime.now())))
            log_file.write('\n')
            if (args.model in ['supervised', 'supervised_nce']):
                dat = SupervisedDataset(args.input, args.validation_points, log_file=log_file, emb_dim=(None if (args.embedding_dim == 512) else args.embedding_dim))
            else:
                dat = Dataset(args.input, binary_files=args.binary_dataset, log_file=log_file)
            if (args.aux_model is None):
                aux_model = None
            elif (args.aux_model == 'uniform'):
                aux_model = UniformAuxModel(dat, log_file=log_file, supervised=(args.model in ['supervised', 'supervised_nce']))
            elif (args.aux_model == 'frequency'):
                aux_model = FrequencyAuxModel(dat, log_file=log_file, supervised=(args.model in ['supervised', 'supervised_nce']), exponent=args.aux_frequency_exponent)
            elif (args.model in ['supervised', 'supervised_nce']):
                aux_model = SupervisedDecisionTreeModel(args.aux_model, dat, log_file=log_file)
            else:
                aux_model = DecisionTreeModel(args.aux_model, dat, log_file=log_file)
            model = Model(args, dat, rng, aux_model=aux_model, log_file=log_file)
            session_config = tf.ConfigProto(log_device_placement=True)
            if args.trace:
                session_config.gpu_options.allow_growth = True
            session = tf.Session(config=session_config)
            init_fd = {}
            if (args.model in ['supervised', 'supervised_nce']):
                init_fd[model.feed_train_features] = dat.features['train']
            session.run(tf.initializers.global_variables(), feed_dict=init_fd, options=tf.RunOptions(report_tensor_allocations_upon_oom=True))
            del init_fd
            if (args.model in ['supervised', 'supervised_nce']):
                del dat.features['train']
            if (args.initialize_from is not None):
                load_checkpoint(model, session, args.initialize_from, log_file=log_file)
            if (args.model in ['supervised', 'supervised_nce']):
                evaluator = evaluate.SupervisedEvaluator(model, dat, args, log_file=log_file)
            else:
                evaluator = evaluate.Evaluator(model, dat, args, log_file=log_file)
            training_loop(args, model, session, dat, rng, evaluator, log_file=log_file)
            log_file.write('\n')
            log_file.write(('end_time = "%s"\n' % str(datetime.datetime.now())))
    except:
        with open(os.path.join(args.output, 'err'), 'w') as err_file:
            traceback.print_exc(file=err_file)
        exit(2)
