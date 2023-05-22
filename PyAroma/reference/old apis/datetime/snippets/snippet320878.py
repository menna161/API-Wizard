import datetime
import os.path
import time
from collections import defaultdict
from types import SimpleNamespace
import torch
import yaml
from sacred import Experiment
from sacred.observers import MongoObserver
import amci.utils


def train(args, _run, _writer):
    model = amci.utils.get_model(args)
    q = model.Training.get_proposal_model(args)
    optimizer = torch.optim.Adam(q.parameters(), lr=args.learning_rate)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=args.scheduler_patience, factor=args.scheduler_factor, verbose=True)
    training = model.Training(args.q1_or_q2, q, args)
    logs = defaultdict(list)

    def save_checkpoint():
        print('Saving model and logs')
        torch.save((q.state_dict(), args, logs), os.path.join(args.output_folder, 'checkpoint.pytorch'))
    time_of_last_checkpoint = time.time()
    dataset_size = (args.number_train_samples + args.number_validation_samples)
    num_batches = (float(args.number_train_samples) / args.minibatch_size)
    for epoch_no in range(args.epochs):
        data = training.generate_dataset(dataset_size)
        train_data = {k: v[:args.number_train_samples] for (k, v) in data.items()}
        validation_data = {k: v[args.number_train_samples:] for (k, v) in data.items()}
        missteps = 0
        with torch.no_grad():
            validation_loss = training.loss(**validation_data).mean().item()
        for local_iter in range(args.max_dataset_iterations):
            print(f'validation_loss: {validation_loss:.5f}')
            train_loss = 0.0
            for batch_data in amci.utils.iterate_minibatches(args.minibatch_size, train_data):
                optimizer.zero_grad()
                loss = training.loss(**batch_data).mean()
                loss.backward()
                optimizer.step()
                train_loss += (loss.item() / num_batches)
            with torch.no_grad():
                next_validation_loss = training.loss(**validation_data).mean().item()
            if (next_validation_loss > validation_loss):
                missteps += 1
            validation_loss = next_validation_loss
            if (missteps > args.misstep_tolerance):
                break
        scheduler.step(validation_loss)
        if ((args.loss_print != 0) and ((epoch_no % args.loss_print) == 0)):
            print(f'{epoch_no} train_loss: {train_loss:.5f}  validation_loss: {validation_loss:.5f}  local_iter: {local_iter}')
        _run.log_scalar('train_loss', train_loss)
        _run.log_scalar('validation_loss', validation_loss)
        _writer.add_scalar('train_loss', train_loss, epoch_no)
        _writer.add_scalar('validation_loss', validation_loss, epoch_no)
        logs['train_loss'].append(train_loss)
        logs['validation_loss'].append(validation_loss)
        logs['loss_time'].append(datetime.datetime.now().timestamp())
        if torch.isnan(loss).any():
            raise Exception(f'NaN loss on epoch {epoch_no}.')
        if ((time.time() - time_of_last_checkpoint) > args.checkpoint_frequency_in_seconds):
            save_checkpoint()
            time_of_last_checkpoint = time.time()
    save_checkpoint()
