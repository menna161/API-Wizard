import os
import time
import cPickle as Pickle
import numpy as np
import tensorflow as tf
from nabu.neuralnetworks.models import model_factory
from nabu.neuralnetworks.components import hooks
from nabu.neuralnetworks.components import sessions as nabu_sessions
from nabu.neuralnetworks.trainers import task_trainer as task_trainer_script
from tensorflow.core.protobuf import rewriter_config_pb2


def __init__(self, conf, tasksconf, dataconf, modelconf, evaluatorconf, lossesconf, expdir, init_filename, task_index):
    '\n\t\tMultiTaskTrainer constructor, creates the training graph\n\n\t\tArgs:\n\t\t\tconf: the trainer config\n\t\t\ttasksconf: the config file for each task\n\t\t\tdataconf: the data configuration as a ConfigParser\n\t\t\tmodelconf: the neural net model configuration\n\t\t\tevaluatorconf: the evaluator configuration for evaluating\n\t\t\t\tif None no evaluation will be done\n\t\t\tlossesconf: the configuration of the loss functions\n\t\t\texpdir: directory where the summaries will be written\n\t\t\tinit_filename: filename of the network that should be used to\n\t\t\tinitialize the model. Put to None if no network is available/wanted.\n\t\t\ttask_index: optional index of the worker task in the cluster\n\t\t'
    self.expdir = expdir
    self.conf = conf
    self.tasksconf = tasksconf
    self.task_index = task_index
    self.init_filename = init_filename
    self.batch_size = int(conf['batch_size'])
    self.tasks = self.conf['tasks'].split(' ')
    self.acc_steps = (('acc_steps' in self.conf) and (self.conf['acc_steps'] == 'True'))
    self.normalize_weights_acc_steps = (self.acc_steps and ('normalize_weights_acc_steps' in self.conf) and (self.conf['normalize_weights_acc_steps'] == 'True'))
    if ('task_weights' in self.conf):
        self.task_weights = map(float, self.conf['task_weights'].split(' '))
        if (len(self.tasks) != len(self.task_weights)):
            raise BaseException(('Number of task weights must equal number of tasks. but was %d and %d' % (len(self.task_weights), len(self.tasks))))
    else:
        self.task_weights = ([1.0] * len(self.tasks))
    self.graph = tf.Graph()
    modelfile = os.path.join(expdir, 'model', 'model.pkl')
    model_names = modelconf.get('hyper', 'model_names').split(' ')
    self.models = dict()
    with open(modelfile, 'wb') as fid:
        for model_name in model_names:
            self.models[model_name] = model_factory.factory(modelconf.get(model_name, 'architecture'))(conf=dict(modelconf.items(model_name)), name=model_name)
        Pickle.dump(self.models, fid)
    evaltype = evaluatorconf.get('evaluator', 'evaluator')
    self.task_trainers = []
    for task in self.tasks:
        taskconf = self.tasksconf[task]
        if lossesconf:
            lossconf = dict(lossesconf.items(taskconf['loss_type']))
        else:
            lossconf = None
        task_trainer = task_trainer_script.TaskTrainer(task, conf, taskconf, self.models, modelconf, dataconf, evaluatorconf, lossconf, self.batch_size)
        self.task_trainers.append(task_trainer)
    nr_tasks = len(self.task_trainers)
    num_replicas = 1
    self.is_chief = (task_index == 0)
    with self.graph.as_default():
        self.num_steps = tf.get_variable(name='num_steps', shape=[], dtype=tf.int32, initializer=tf.constant_initializer(0), trainable=False)
        self.global_step = tf.get_variable(name='global_step', shape=[], dtype=tf.int32, initializer=tf.constant_initializer(0), trainable=False)
        should_terminate = tf.get_variable(name='should_terminate', shape=[], dtype=tf.bool, initializer=tf.constant_initializer(False), trainable=False)
        self.should_save_final_model = tf.get_variable(name='should_save_final_model', shape=[], dtype=tf.bool, initializer=tf.constant_initializer(False), trainable=False)
        self.do_save_final_model = self.should_save_final_model.assign(True).op
        self.terminate = should_terminate.assign(True).op
        self.should_stop = tf.logical_or(tf.greater_equal(self.global_step, self.num_steps), should_terminate)
        num_steps = []
        done_ops = []
        for task_trainer in self.task_trainers:
            (task_num_steps, task_done_ops) = task_trainer.set_dataqueues()
            num_steps.append(task_num_steps)
            done_ops += task_done_ops
        self.set_num_steps = self.num_steps.assign(min(num_steps)).op
        self.done = tf.group(*done_ops)
        with tf.variable_scope('train'):
            learning_rate_fact = tf.get_variable(name='learning_rate_fact', shape=[], initializer=tf.constant_initializer(1.0), trainable=False)
            self.learning_rate = (tf.train.exponential_decay(learning_rate=float(conf['initial_learning_rate']), global_step=self.global_step, decay_steps=self.num_steps, decay_rate=float(conf['learning_rate_decay'])) * learning_rate_fact)
            if self.acc_steps:
                if self.normalize_weights_acc_steps:
                    vars_norm_weight = dict()
                    all_task_var_names = dict()
                    all_task_batch_grads_and_vars = dict()
                    for (task_trainer, task_weight) in zip(self.task_trainers, self.task_weights):
                        dummy_optimizer = optimizer = tf.train.AdamOptimizer(self.learning_rate)
                        task_batch_grads_and_vars = task_trainer.gather_grads(dummy_optimizer)
                        task_var_names = [task_var.name for (_, task_var) in task_batch_grads_and_vars]
                        all_task_var_names[task_trainer.task_name] = task_var_names
                        all_task_batch_grads_and_vars[task_trainer.task_name] = task_batch_grads_and_vars
                        for task_var_name in task_var_names:
                            if (task_var_name not in vars_norm_weight):
                                vars_norm_weight[task_var_name] = 0.0
                            vars_norm_weight[task_var_name] += task_weight
                    for (task_trainer, task_weight) in zip(self.task_trainers, self.task_weights):
                        task_var_names = all_task_var_names[task_trainer.task_name]
                        task_batch_grads_and_vars = all_task_batch_grads_and_vars[task_trainer.task_name]
                        task_vars_norm_weights = {task_var_name: (task_weight / vars_norm_weight[task_var_name]) for task_var_name in task_var_names}
                        task_trainer.train(self.learning_rate, var_weights=task_vars_norm_weights, batch_grads_and_vars=task_batch_grads_and_vars)
                else:
                    for (task_trainer, task_weight) in zip(self.task_trainers, self.task_weights):
                        task_trainer.train((self.learning_rate * task_weight))
            else:
                optimizer = tf.train.AdamOptimizer(self.learning_rate)
                all_batch_grads_and_vars = []
                for task_trainer in self.task_trainers:
                    all_batch_grads_and_vars.append(task_trainer.gather_grads(optimizer))
                batch_grads_and_vars_dict = dict()
                for (batch_grads_and_vars, task_weight) in zip(all_batch_grads_and_vars, self.task_weights):
                    for (grad, var) in batch_grads_and_vars:
                        if (var in batch_grads_and_vars_dict):
                            batch_grads_and_vars_dict[var] += (grad * task_weight)
                        else:
                            batch_grads_and_vars_dict[var] = (grad * task_weight)
                batch_grads_and_vars = zip(batch_grads_and_vars_dict.values(), batch_grads_and_vars_dict.keys())
                self.batch_grads_and_vars = batch_grads_and_vars
            self.reset_grad_loss_norm = tf.group(*[task_trainer.reset_grad_loss_norm for task_trainer in self.task_trainers], name='reset_grad_loss_norm_all_tasks')
            tmp = []
            for task_trainer in self.task_trainers:
                tmp += task_trainer.normalize_gradients
            self.normalize_gradients = tf.group(*tmp, name='normalize_gradients_all_tasks')
            with tf.variable_scope('accumulate_losses_from_tasks'):
                self.loss_all_tasks = [task_trainer.normalized_loss for task_trainer in self.task_trainers]
                self.total_loss = tf.reduce_sum([(loss * weight) for (loss, weight) in zip(self.loss_all_tasks, self.task_weights)], name='acc_loss')
            if self.acc_steps:
                tmp = []
                for task_trainer in self.task_trainers:
                    tmp.append(task_trainer.apply_gradients)
            else:
                self.apply_gradients = optimizer.apply_gradients(grads_and_vars=self.batch_grads_and_vars, name='apply_gradients')
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            global_step_inc = self.global_step.assign_add(1)
            self.other_update_op = tf.group(*(update_ops + [global_step_inc]), name='other_update')
        if (evaltype != 'None'):
            with tf.variable_scope('validate'):
                validated_step = tf.get_variable(name='validated_step', shape=[], dtype=tf.int32, initializer=tf.constant_initializer((- int(conf['valid_frequency']))), trainable=False)
                self.should_validate = tf.greater_equal((self.global_step - validated_step), int(conf['valid_frequency']))
                tasks_excluded_for_val = ['None']
                if evaluatorconf.has_option('evaluator', 'tasks_excluded_for_val'):
                    tasks_excluded_for_val = evaluatorconf.get('evaluator', 'tasks_excluded_for_val').split(' ')
                self.val_task_trainers = [task_trainer for task_trainer in self.task_trainers if (task_trainer.task_name not in tasks_excluded_for_val)]
                nr_val_tasks = len(self.val_task_trainers)
                valbatches = []
                for task_trainer in self.val_task_trainers:
                    valbatches.append(task_trainer.evaluate_evaluator())
                    self.valbatches = min(valbatches)
                self.process_val_batch = tf.group(*[task_trainer.process_val_batch for task_trainer in self.val_task_trainers])
                self.reset_val_loss_norm = tf.group(*[task_trainer.reset_val_loss_norm for task_trainer in self.val_task_trainers])
                self.val_loss_all_tasks = []
                for task_trainer in self.val_task_trainers:
                    self.val_loss_all_tasks.append(task_trainer.val_loss_normalized)
                self.validation_loss = tf.reduce_sum([(loss * weight) for (loss, weight) in zip(self.val_loss_all_tasks, self.task_weights)])
                self.half_lr = learning_rate_fact.assign((learning_rate_fact / 2)).op
                self.update_validated_step = validated_step.assign(self.global_step).op
                if self.acc_steps:
                    self.best_validation_all_tasks = [tf.get_variable(name=('best_validation_task_%i' % ind), shape=[], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False) for ind in range(nr_val_tasks)]
                    self.update_best_all_tasks = [best_val_task.assign(self.val_loss_all_tasks[ind]) for (ind, best_val_task) in enumerate(self.best_validation_all_tasks)]
                    self.previous_validation_all_tasks = [tf.get_variable(name=('previous_validation_task_%i' % ind), shape=[], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False) for ind in range(nr_val_tasks)]
                    self.update_prev_all_tasks = [prev_val_task.assign(self.val_loss_all_tasks[ind]) for (ind, prev_val_task) in enumerate(self.previous_validation_all_tasks)]
                    self.rel_validation_all_tasks = [tf.get_variable(name=('rel_validation_task_%i' % ind), shape=[int(self.conf['num_tries'])], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False) for ind in range(nr_val_tasks)]
                    rel_impr = [((self.previous_validation_all_tasks[ind] - self.val_loss_all_tasks[ind]) / self.previous_validation_all_tasks[ind]) for ind in range(nr_val_tasks)]
                    all_rel_imprs = [tf.concat([rel_val_task[1:], tf.expand_dims(rel_impr[ind], (- 1))], axis=0) for (ind, rel_val_task) in enumerate(self.rel_validation_all_tasks)]
                    self.update_rel_all_tasks = [tf.assign(rel_val_task, all_rel_imprs[ind]) for (ind, rel_val_task) in enumerate(self.rel_validation_all_tasks)]
                    self.num_tries_all_tasks = [tf.get_variable(name=('num_tries_task_%i' % ind), shape=[], dtype=tf.int32, initializer=tf.constant_initializer(0), trainable=False) for ind in range(nr_val_tasks)]
                    self.incr_num_tries_all_tasks = [num_tries.assign((num_tries + 1)) for (ind, num_tries) in enumerate(self.num_tries_all_tasks)]
                    self.reset_num_tries_all_tasks = [num_tries.assign(0) for (ind, num_tries) in enumerate(self.num_tries_all_tasks)]
                else:
                    self.best_validation = tf.get_variable(name='best_validation', shape=[], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False)
                    self.update_best = self.best_validation.assign(self.validation_loss)
                    self.previous_validation = tf.get_variable(name='previous_validation', shape=[], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False)
                    self.update_prev = self.previous_validation.assign(self.validation_loss)
                    self.rel_validation = tf.get_variable(name='rel_validation', shape=[int(self.conf['num_tries'])], dtype=tf.float32, initializer=tf.constant_initializer(1.79e+308), trainable=False)
                    rel_impr = ((self.previous_validation - self.validation_loss) / self.previous_validation)
                    all_rel_imprs = tf.concat([self.rel_validation[1:], tf.expand_dims(rel_impr, (- 1))], axis=0)
                    self.update_rel = tf.assign(self.rel_validation, all_rel_imprs)
                    self.num_tries = tf.get_variable(name='num_tries', shape=[], dtype=tf.int32, initializer=tf.constant_initializer(0), trainable=False)
                    self.incr_num_tries = self.num_tries.assign((self.num_tries + 1))
                    self.reset_num_tries = self.num_tries.assign(0)
                waiting_workers = tf.get_variable(name='waiting_workers', shape=[], dtype=tf.int32, initializer=tf.constant_initializer(0), trainable=False)
                self.waiting = waiting_workers.assign_add(1).op
                self.reset_waiting = waiting_workers.initializer
                self.all_waiting = tf.equal(waiting_workers, (num_replicas - 1))
        else:
            self.process_val_batch = None
        self.scaffold = tf.train.Scaffold(saver=tf.train.Saver(max_to_keep=1))
