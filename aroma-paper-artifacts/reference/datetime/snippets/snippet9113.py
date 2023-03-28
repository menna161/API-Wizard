import sys
import time
import os
import pickle
import cProfile
import re
import datetime
import numpy as np
import torch
from torch.autograd import Variable
from torch.utils.data import Sampler, DataLoader
from . import helpers
from . import voc_eval_helpers
from . import active_learning_helpers
from layers import box_utils
import data


def sim_active_learning(args):
    '\n    Simulated active learning loop for experimentation purposes, labels are already known.\n    '
    global unlabeled_idx
    if (args.labeled_idx_file is None):
        raise FileNotFoundError("No path specified for the labeled idx file'")
        sys.exit()
    if (args.debug and (not os.path.exists((args.experiment_dir + 'sample_selection/')))):
        os.mkdir((args.experiment_dir + 'sample_selection/'))
    helpers.set_all_seeds(args)
    sample_select_dataset = helpers.load_sample_select_set(args, args.imageset_train)
    train_dataset = helpers.load_trainset(args, args.imageset_train)
    label_dict = helpers.read_labeled(args.path_to_labeled_idx_file, args.annotate_all_objects, args.dataset, args)
    val_dataset = helpers.load_evalset(args, args.imageset_train, idx=label_dict['val_set']['image_set_idx'])
    print(args)
    args.num_classes = (train_dataset.num_classes + 1)
    args.sample_select_dataset_imageset_ids = [id[1] for id in sample_select_dataset.ids]
    args.summary = {}
    args.summary['sample_selection'] = {}
    args.summary['train_model'] = {}
    args.summary['eval_model'] = {}
    for i in range(args.start_iter, len(args.samples_per_iter)):
        print('Starting Active Learning iteration: {:d}/{:d}'.format(i, len(args.samples_per_iter)))
        print('Local time: ', datetime.datetime.now())
        timers = {}
        timers['full_al_iteration'] = helpers.Timer()
        timers['full_al_iteration'].tic()
        timers['sample_selection'] = helpers.Timer()
        timers['train_model'] = helpers.Timer()
        timers['eval_model'] = helpers.Timer()
        args.al_iteration = i
        print('Selecting samples...')
        timers['sample_selection'].tic()
        if ((not (args.skip_sample_selection_first_iter and (i == args.start_iter))) and (not args.train_basenets)):
            if ((args.sampling_strategy == 'random_none') and (not args.density_diversity)):
                new_labeled_idx = active_learning_helpers.sample_selection(args, sample_select_dataset, active_learning_iter=i)
            elif ((args.sampling_strategy not in ['p-max_localization-stability', 'no_ensemble_entropy-only', 'random_none']) and (args.modeltype != 'SSD300KL')):
                label_dict = helpers.read_labeled(args.path_to_labeled_idx_file, args.annotate_all_objects, args.dataset, args)
                unlabeled_idx = [s for s in args.sample_select_dataset_imageset_ids if ((s not in label_dict['train_set']) and (s not in label_dict['val_set']['image_set_idx']))]
                print('Number of unlabeled images:', len(unlabeled_idx))
                len_unlabeled_idx = len(unlabeled_idx)
                if (not (args.skip_detection_part_sample_selection and (args.start_iter == i))):
                    if (len_unlabeled_idx > 2000):
                        num_splits = 20
                    else:
                        num_splits = 10
                    split_indices = np.ceil(np.linspace(0, len_unlabeled_idx, (num_splits + 1), dtype=int))
                    split_indices = [int(i) for i in split_indices]
                    for split_num in range(1, (num_splits + 1)):
                        if (args.debug and (split_num > 1)):
                            continue
                        print('split num: ', split_num)
                        print(split_indices[(split_num - 1)], split_indices[split_num])
                        print('Local time: ', datetime.datetime.now())
                        print('\n\n\n')
                        unlabeled_imageset_split = unlabeled_idx[split_indices[(split_num - 1)]:split_indices[split_num]]
                        len_unlabeled_idx = len(unlabeled_imageset_split)
                        if args.debug:
                            if (split_num == 0):
                                unlabeled_imageset_split = unlabeled_imageset_split[:4]
                            else:
                                unlabeled_imageset_split = unlabeled_imageset_split[:5]
                            len_unlabeled_idx = len(unlabeled_imageset_split)
                            unlabeled_idx = unlabeled_imageset_split
                        for j in range(args.ensemble_size):
                            print('Ensemble: ', j)
                            print('Local time: ', datetime.datetime.now())
                            if (args.device == 'cuda'):
                                torch.cuda.empty_cache()
                            net = helpers.build_sample_selection_net(args, ensemble_idx=j, merging_method=args.merging_method, sampling_strategy=args.sampling_strategy, default_forward=False)
                            (output, num_unlabeled_images, priors, unlabeled_imgset) = active_learning_helpers.detect_on_unlabeled_imgs(net, args, sample_select_dataset, unlabeled_idx=unlabeled_imageset_split, len_unlabeled_idx=len_unlabeled_idx)
                            detections_path = helpers.save_detections(args, output, j, num_unlabeled_images)
                        print('\nStarting clustering observations...')
                        print('Local time: ', datetime.datetime.now())
                        print('')
                        observations = active_learning_helpers.cluster_detections_to_observations(args, args.merging_method, unlabeled_imgset, num_unlabeled_images, priors=priors)
                        if (args.merging_method in ['pre_nms_avg', 'bsas', 'hbdscan']):
                            os.remove(detections_path)
                        (all_observations, observations_path) = helpers.save_observations(args, i, observations)
                else:
                    print('Loading observations from memory...')
                    path = (((args.experiment_dir + 'sample_selection/observations-iter_') + str(i)) + '_.pickle')
                    all_observations = helpers.unpickle(path)
                print('\nStarting calculating uncertainties...')
                print('Local time: ', datetime.datetime.now())
                print('')
                (uncertainty_per_image, classification_uncertainty, localization_uncertainty) = active_learning_helpers.calculate_uncertainties(args, all_observations, unlabeled_idx)
                print('Uncertainties calculated')
                print('Local time: ', datetime.datetime.now())
                print('')
                with open((((args.experiment_dir + 'sample_selection/uncertainties-iter_') + str(i)) + '_.pickle'), 'wb') as f:
                    pickle.dump((uncertainty_per_image, classification_uncertainty, localization_uncertainty), f)
                if (not args.density_diversity):
                    if args.debug:
                        args.samples_per_iter[i] = 3
                    if (not args.budget_measured_in_objects):
                        if (not args.user_relevance_feedback):
                            top_k_uncertain_images = uncertainty_per_image.cpu().topk(k=args.samples_per_iter[i])
                        else:
                            top_k_uncertain_images = uncertainty_per_image.cpu().topk(k=args.samples_per_iter[i], largest=False)
                        new_labeled_idx = [unlabeled_idx[idx] for idx in top_k_uncertain_images[1]]
                    elif (not args.user_relevance_feedback):
                        sorted_indices = uncertainty_per_image.cpu().sort(descending=True)[1].numpy()
                        ordered_uncertain_images = [unlabeled_idx[i] for i in sorted_indices]
                        new_labeled_idx = active_learning_helpers.select_samples_with_object_budget(args, ordered_uncertain_images, object_budget=args.samples_per_iter[i], dataset=sample_select_dataset)
                    else:
                        sorted_indices = uncertainty_per_image.cpu().sort(descending=False)[1].numpy()
                        ordered_certain_images = [unlabeled_idx[i] for i in sorted_indices]
                        new_labeled_idx = active_learning_helpers.select_samples_with_object_budget(args, ordered_certain_images, object_budget=args.samples_per_iter[i], dataset=sample_select_dataset)
                    del all_observations, uncertainty_per_image, classification_uncertainty, localization_uncertainty
            else:
                label_dict = helpers.read_labeled(args.path_to_labeled_idx_file, args.annotate_all_objects, args.dataset, args)
                unlabeled_idx = [s for s in args.sample_select_dataset_imageset_ids if ((s not in label_dict['train_set']) and (s not in label_dict['val_set']['image_set_idx']))]
                print('Number of unlabeled images:', len(unlabeled_idx))
                if args.debug:
                    unlabeled_idx = [idx[1] for idx in sample_select_dataset.ids[:10]]
                    args.samples_per_iter[i] = 3
                len_unlabeled_idx = len(unlabeled_idx)
                if ((args.sampling_strategy == 'p-max_localization-stability') and (args.modeltype != 'SSD300KL')):
                    net = helpers.build_sample_selection_net(args, ensemble_idx=0, merging_method=args.merging_method, default_forward=False, sampling_strategy=args.sampling_strategy)
                    new_labeled_idx = active_learning_helpers.localization_stability_sample_selection(args, net, sample_select_dataset, unlabeled_idx, len_unlabeled_idx, i)
                elif ((args.sampling_strategy == 'no_ensemble_entropy-only') and (args.modeltype != 'SSD300KL')):
                    net = helpers.build_sample_selection_net(args, ensemble_idx=0, merging_method=args.merging_method, default_forward=False, sampling_strategy=args.sampling_strategy)
                    (new_labeled_idx, uncertainty_per_image) = active_learning_helpers.entropy_only_baseline(args, net, sample_select_dataset, unlabeled_idx, len_unlabeled_idx, i)
                elif (args.modeltype == 'SSD300KL'):
                    net = helpers.build_sample_selection_net(args, ensemble_idx=0, merging_method=args.merging_method, default_forward=False, sampling_strategy=args.sampling_strategy)
                    new_labeled_idx = active_learning_helpers.SSDKL_sample_selection(args, net, sample_select_dataset, unlabeled_idx, len_unlabeled_idx, i)
                elif (args.density_diversity == 'density'):
                    pass
                else:
                    raise NotImplementedError()
            if (args.density_diversity == 'density'):
                density_per_image = active_learning_helpers.density_sampling(args, sample_select_dataset, unlabeled_idx)
                if (args.sampling_strategy == 'random_none'):
                    print('sampling strategy: density only')
                    informativeness_per_image = density_per_image
                else:
                    print('sampling strategy: density + uncertainty, equal weighing')
                    informativeness_per_image = (density_per_image + uncertainty_per_image)
                if (not args.budget_measured_in_objects):
                    if (not args.user_relevance_feedback):
                        top_k_uncertain_images = informativeness_per_image.topk(k=args.samples_per_iter[args.al_iteration])
                    else:
                        top_k_uncertain_images = informativeness_per_image.topk(k=args.samples_per_iter[args.al_iteration], largest=False)
                    new_labeled_idx = [unlabeled_idx[idx] for idx in top_k_uncertain_images[1]]
                elif (not args.user_relevance_feedback):
                    sorted_indices = informativeness_per_image.cpu().sort(descending=True)[1].numpy()
                    ordered_uncertain_images = [unlabeled_idx[i] for i in sorted_indices]
                    new_labeled_idx = active_learning_helpers.select_samples_with_object_budget(args, ordered_uncertain_images, object_budget=args.samples_per_iter[args.al_iteration], dataset=sample_select_dataset)
                else:
                    sorted_indices = informativeness_per_image.cpu().sort(descending=False)[1].numpy()
                    ordered_certain_images = [unlabeled_idx[i] for i in sorted_indices]
                    new_labeled_idx = active_learning_helpers.select_samples_with_object_budget(args, ordered_certain_images, object_budget=args.samples_per_iter[args.al_iteration], dataset=sample_select_dataset)
            helpers.write_labeled(args, new_labeled_idx)
            selected_classes = helpers.class_dist_in_imageset(args, new_labeled_idx, sample_select_dataset)
            args.summary['sample_selection']['object_classes_selected'] = selected_classes
            args.summary['sample_selection']['images_selected'] = new_labeled_idx
            helpers.write_summary(args, timers, write='sample_selection')
            print('Samples are selected for Active Learning iteration: {:d}/{:d}'.format(i, len(args.samples_per_iter)))
            print('Samples are written to:  {}'.format(args.path_to_labeled_idx_file))
        else:
            print('skip sample selection for first al-iter')
        print('Starting training of Active Learning iteration: {:d}/{:d}'.format(i, len(args.samples_per_iter)))
        timers['train_model'].tic()
        args.summary['train_model']['losses'] = {}
        for j in range(args.ensemble_size):
            print('train model {:d}/{:d}'.format((j + 1), args.ensemble_size))
            print('Local time: ', datetime.datetime.now())
            if ((i == args.start_iter) and (j < args.start_first_iter_from_ensemble_id)):
                print('Skip training this model as it has already been trained')
                continue
            helpers.set_all_seeds(args, seed_incrementer=j)
            active_learning_helpers.train_model(args, train_dataset, val_dataset, ensemble_idx=j)
        timers['train_model'].toc()
        helpers.write_summary(args, timers, write='train_model')
        if args.eval_every_iter:
            print('Start eval')
            print('Local time: ', datetime.datetime.now())
            eval_dataset = helpers.load_evalset(args, imageset=args.imageset_test)
            path_to_weights = os.path.join(args.experiment_dir, 'weights/')
            if args.eval_n_per_al_iter:
                al_iters_avaluated = {}
            network_list = [net for net in os.listdir(path_to_weights) if (int(net.split('_')[2]) == i)]
            if args.eval_n_per_al_iter:
                if (i in al_iters_avaluated):
                    if (al_iters_avaluated[i] >= args.eval_n_per_al_iter):
                        print('already evaluated ', str(args.eval_n_per_al_iter), 'networks, continuing to next network ')
                        print()
                        continue
                    else:
                        al_iters_avaluated[i] += 1
                al_iters_avaluated[i] = 1
            for weights in network_list:
                args.path_to_eval_weights = (path_to_weights + weights)
                eval_net = helpers.build_eval_net(args)
                timers['eval_model'].tic()
                args.eval_ensemble_idx = weights.split('_')[(- 2)]
                args.al_iteration = i
                if (args.dataset in ['VOC07', 'VOC07_1_class', 'VOC07_6_class']):
                    voc_eval_helpers.eval(eval_dataset, args, eval_net, i, args.eval_ensemble_idx)
                else:
                    raise NotImplementedError()
                timers['eval_model'].toc()
                helpers.eval_summary_writer(args, timers)
