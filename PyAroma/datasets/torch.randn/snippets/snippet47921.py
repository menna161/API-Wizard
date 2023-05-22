import math
import os
import torchvision
import torch.utils.data
from tqdm import tqdm
from tqdm import trange
import lib.OpenSet.meta_recognition as mr
from lib.Training.evaluate import sample_per_class_zs
from lib.Training.evaluate import eval_dataset


def get_incremental_dataset(parent_class):
    "\n    Wrapper that returns the incremental dataset class. For the incremental dataset scenario\n    the class will inherit from the original dataset and split the dataset as specified in the command line arguments.\n\n    We note that the use of the term task is slightly ambiguous. As our model is a unified model with a\n    growing classifier it technically always only has one task, namely to classify, reconstruct and replay everything\n    it has seen so far. In our context the below task variables are thus used for convenience to indicate when something\n    is added and how much has been seen already. We hope that this doesn't cause too much confusion.\n\n    Parameters:\n        parent_class: Dataset class to inherit from for the class incremental scenario.\n        args (dict): Command line arguments.\n    "

    class IncrementalDataset(parent_class):
        '\n        Incremental dataset class. Inherits from a dataset parent class. Defines functions to split classes into\n        separate sets, incrementing the current set and replacing previous sets with generative replay examples.\n\n        Parameters:\n        is_gpu (bool): True if CUDA is enabled. Sets value of pin_memory in DataLoader.\n        task_order (list): List defining class order (sequence of integers).\n        args (dict): Dictionary of (command line) arguments. Needs to contain num_base_tasks (int),\n            num_increment_tasks (int), batch_size (int), workers(int), var_samples (int) and distance_function (str).\n\n        Attributes:\n            task_order (list): Sequence of integers defining incremental class ordering.\n            seen_tasks (list): List of already seen tasks at any given increment.\n            num_base_tasks (int): Number of initial classes.\n            num_increment_tasks (int): Amount of classes that get added with each increment.\n            device (str): Device to compute on\n            vis_size (int): Visualization size used in generation of dataset snapshots.\n            trainsets (torch.utils.data.TensorDataset): Training set wrapper.\n            trainset (torch.utils.data.TensorDataset): Training increment set wrapper.\n            valsets (torch.utils.data.TensorDataset): Validation set wrapper\n            valset (torch.utils.data.TensorDataset): Validation increment set wrapper.\n            class_to_idx (dict): Defines mapping from class names to integers.\n            train_loader (torch.utils.data.DataLoader): Training set loader with shuffling.\n            val_loader (torch.utils.data.DataLoader): Validation set loader.\n        '

        def __init__(self, is_gpu, device, task_order, args):
            super().__init__(is_gpu, args)
            self.task_order = task_order
            self.seen_tasks = []
            self.num_base_tasks = (args.num_base_tasks + 1)
            self.num_increment_tasks = args.num_increment_tasks
            self.device = device
            self.args = args
            self.vis_size = 144
            (self.trainsets, self.valsets) = ({}, {})
            self.class_to_idx = {}
            self.__get_incremental_datasets()
            (self.trainset, self.valset) = self.__get_initial_dataset()
            (self.train_loader, self.val_loader) = self.get_dataset_loader(args.batch_size, args.workers, is_gpu)

        def __get_incremental_datasets(self):
            "\n            Splits the existing parent dataset into separate datasets per class. As our model's use a single-head\n            growing classifier, also relabels the targets according to task sequence so the first encountered class\n            is always 0, the second 1, etc. even if the former label was something else like class 5 and 7.\n            "
            datasets = [self.trainset, self.valset]
            for j in range(2):
                (tensors_list, targets_list) = ([], [])
                for i in range(self.num_classes):
                    tensors_list.append([])
                    targets_list.append([])
                for (i, (inp, target)) in enumerate(datasets[j]):
                    if isinstance(target, int):
                        pass
                    elif isinstance(target, torch.Tensor):
                        if (target.dim() > 0):
                            target = int(torch.argmax(target))
                        else:
                            target = int(target)
                    else:
                        raise ValueError
                    relabeled_target = self.task_order.index(target)
                    tensors_list[target].append(inp)
                    targets_list[target].append(relabeled_target)
                for i in range(self.num_classes):
                    tensors_list[i] = torch.stack(tensors_list[i], dim=0)
                    targets_list[i] = torch.LongTensor(targets_list[i])
                    if (j == 0):
                        self.trainsets[i] = torch.utils.data.TensorDataset(tensors_list[i], targets_list[i])
                    else:
                        self.valsets[i] = torch.utils.data.TensorDataset(tensors_list[i], targets_list[i])

        def __get_initial_dataset(self):
            '\n            Fills the initial trainset and valset for the number of base tasks/classes in the order specified by the\n            task order attribute.\n\n            Returns:\n                torch.utils.data.TensorDataset: trainset, valset\n            '
            for i in range(self.num_base_tasks):
                self.class_to_idx[str(self.task_order[0])] = i
                self.seen_tasks.append(self.task_order.pop(0))
            trainset = torch.utils.data.ConcatDataset([self.trainsets[j] for j in self.seen_tasks])
            valset = torch.utils.data.ConcatDataset([self.valsets[j] for j in self.seen_tasks])
            sorted_tasks = sorted(self.seen_tasks, reverse=True)
            for i in sorted_tasks:
                self.trainsets.pop(i)
                self.valsets.pop(i)
            return (trainset, valset)

        def get_dataset_loader(self, batch_size, workers, is_gpu):
            '\n            Defines the dataset loader for wrapped dataset\n\n            Parameters:\n                batch_size (int): Defines the batch size in data loader\n                workers (int): Number of parallel threads to be used by data loader\n                is_gpu (bool): True if CUDA is enabled so pin_memory is set to True\n\n            Returns:\n                 torch.utils.data.DataLoader: train_loader, val_loader\n            '
            train_loader = torch.utils.data.DataLoader(self.trainset, batch_size=batch_size, shuffle=True, num_workers=workers, pin_memory=is_gpu, sampler=None)
            val_loader = torch.utils.data.DataLoader(self.valset, batch_size=batch_size, shuffle=True, num_workers=workers, pin_memory=is_gpu)
            return (train_loader, val_loader)

        def increment_tasks(self, model, batch_size, workers, writer, save_path, is_gpu, upper_bound_baseline=False, generative_replay=False, openset_generative_replay=False, openset_threshold=0.05, openset_tailsize=0.05, autoregression=False):
            "\n            Main function to increment tasks/classes. Has multiple options to specify whether the new dataset should\n            provide an upper bound for a continual learning experiment by concatenation of new real data with\n            existing real data, using generative replay to rehearse previous tasks or using the OpenVAE's generative\n            replay with statistical outlier rejection to rehearse previous tasks. If nothing is specified the\n            incremental lower bound of just training on the new task increment is considered. Validation sets are always\n            composed of real data as well as the newly added task increment that is yet unseen. The latter is added by\n            popping indices from the task order queue and adding corresponding individual datasets.\n\n            Overwrites trainset and valset and updates the classes' train and val loaders.\n\n            Parameters:\n                model (torch.nn.module): unified model, needed if any form of generative replay is active.\n                batch_size (int): batch_size for generative replay. Only defines computation speed of replay.\n                workers (int): workers for parallel cpu thread for the newly composed data loaders.\n                writer (tensorboard.SummaryWriter): TensorBoard writer instance.\n                save_path (str): Path used for saving snapshots.\n                is_gpu (bool): Flag indicating whether GPU is used. Needed for the pin memory of the data loaders.\n                upper_bound_baseline (bool): If on, real data is kept and concatenated with new task's real data.\n                generative replay (bool): If True, generative replay is used to rehearse previously seen tasks.\n                openset_generative_replay (bool): If True, generative replay with statistical outlier rejection is\n                    used based on the aggregate posterior.\n                openset_threshold (float): statistical outlier rejection prior that is used to reject z samples from\n                    regions of low density.\n                openset_tailsize (int): Tailsize used in the fit of the Weibul models. Should be a percentage\n                    (range 0-1) specifying amount of dataset expected to be considered as atypical. Typically this\n                    is something low like 5% or even less.\n                autoregression (bool): If True, generative replay is conducted with the autoregressive model.\n            "
            new_tasks = []
            for i in range(self.num_increment_tasks):
                idx = self.task_order.pop(0)
                new_tasks.append(idx)
                self.class_to_idx[str(idx)] = len(self.seen_tasks)
                self.seen_tasks.append(idx)
            sorted_new_tasks = sorted(new_tasks, reverse=True)
            if upper_bound_baseline:
                new_trainsets = [self.trainsets.pop(j) for j in sorted_new_tasks]
                new_trainsets.append(self.trainset)
                self.trainset = torch.utils.data.ConcatDataset(new_trainsets)
            elif (generative_replay or openset_generative_replay):
                new_trainsets = [self.trainsets.pop(j) for j in sorted_new_tasks]
                genset = self.generate_seen_tasks(model, batch_size, len(self.trainset), writer, save_path, openset=openset_generative_replay, openset_threshold=openset_threshold, openset_tailsize=openset_tailsize, autoregression=autoregression)
                new_trainsets.append(genset)
                self.trainset = torch.utils.data.ConcatDataset(new_trainsets)
            elif (self.num_increment_tasks == 1):
                self.trainset = self.trainsets.pop(new_tasks[0])
            else:
                self.trainset = torch.utils.data.ConcatDataset([self.trainsets.pop(j) for j in sorted_new_tasks])
            new_valsets = [self.valsets.pop(j) for j in sorted_new_tasks]
            new_valsets.append(self.valset)
            self.valset = torch.utils.data.ConcatDataset(new_valsets)
            (self.train_loader, self.val_loader) = self.get_dataset_loader(batch_size, workers, is_gpu)

        def generate_seen_tasks(self, model, batch_size, seen_dataset_size, writer, save_path, openset=False, openset_threshold=0.05, openset_tailsize=0.05, autoregression=False):
            '\n            The function implementing the actual generative replay and openset generative replay with statistical\n            outlier rejection.\n\n            Parameters:\n                model (torch.nn.module): Unified model, needed if any form of generative replay is active.\n                batch_size (int): Batch_size for generative replay. Only defines computation speed of replay.\n                seen_dataset_size (int): Number of data points to generate. As the name suggests we have set this\n                    to the exact number of previously seen real data points. In principle this can be a hyper-parameter.\n                writer (tensorboard.SummaryWriter): TensorBoard writer instance.\n                save_path (str): Path used for saving snapshots.\n                openset_generative_replay (bool): If True, generative replay with statistical outlier rejection based\n                    on the aggregate posterior is used-\n                openset_threshold (float): statistical outlier rejection prior that is used to reject z samples from\n                    regions of low density.\n                openset_tailsize (int): Tailsize used in the fit of the Weibul models. Should be a percentage\n                    (range 0-1) specifying amount of dataset expected to be considered as atypical. Typically this\n                    is something low like 5% or even less.\n                autoregression (bool): If True, generative replay is conducted with the autoregressive model.\n\n            Returns:\n                torch.utils.data.TensorDataset: generated trainset\n            '
            data = []
            zs = []
            targets = []
            openset_success = True
            if openset:
                dataset_train_dict = eval_dataset(model, self.train_loader, (len(self.seen_tasks) - self.num_increment_tasks), self.device, samples=self.args.var_samples)
                z_means = mr.get_means(dataset_train_dict['zs_correct'])
                use_new_z_bound = False
                z_mean_bound = (- 100000)
                for c in range(len(z_means)):
                    if isinstance(z_means[c], torch.Tensor):
                        tmp_bound = torch.max(torch.abs(z_means[c])).cpu().item()
                        if (tmp_bound > z_mean_bound):
                            z_mean_bound = tmp_bound
                train_distances_to_mu = mr.calc_distances_to_means(z_means, dataset_train_dict['zs_correct'], self.args.distance_function)
                tailsize = int(((seen_dataset_size * openset_tailsize) / (len(self.seen_tasks) - self.num_increment_tasks)))
                print(('Fitting Weibull models with tailsize: ' + str(tailsize)))
                tailsizes = ([tailsize] * (len(self.seen_tasks) - self.num_increment_tasks))
                (weibull_models, valid_weibull) = mr.fit_weibull_models(train_distances_to_mu, tailsizes)
                if (not valid_weibull):
                    print('Open set fit was not successful')
                    openset_success = False
                else:
                    print('Using generative model to replay old data with openset detection')
                    class_counters = ([0] * (len(self.seen_tasks) - self.num_increment_tasks))
                    samples_per_class = int(math.ceil((seen_dataset_size / (len(self.seen_tasks) - self.num_increment_tasks))))
                    openset_attempts = 0
                    pbar = tqdm(total=seen_dataset_size)
                    while (sum(class_counters) < seen_dataset_size):
                        z_dict = sample_per_class_zs(model, (len(self.seen_tasks) - self.num_increment_tasks), batch_size, self.device, use_new_z_bound, z_mean_bound)
                        z_samples_distances_to_mean = mr.calc_distances_to_means(z_means, z_dict['z_samples'], self.args.distance_function)
                        z_samples_outlier_probs = mr.calc_outlier_probs(weibull_models, z_samples_distances_to_mean)
                        for i in range((len(self.seen_tasks) - self.num_increment_tasks)):
                            for j in range(len(z_samples_outlier_probs[i])):
                                if (class_counters[i] < samples_per_class):
                                    if (z_samples_outlier_probs[i][j] < openset_threshold):
                                        zs.append(z_dict['z_samples'][i][j])
                                        targets.append(i)
                                        class_counters[i] += 1
                                        pbar.update(1)
                                else:
                                    break
                        openset_attempts += 1
                        if ((openset_attempts == 2000) and any([(val == 0) for val in class_counters])):
                            data = []
                            zs = []
                            targets = []
                            if use_new_z_bound:
                                print('\n Open set generative replay timeout')
                                openset_success = False
                                break
                            else:
                                print('\n Open set generative replay from standard Gaussian failed. Trying sampling with modified variance bound')
                                use_new_z_bound = True
                                openset_attempts = 0
                    pbar.close()
                    if openset_success:
                        print('Openset sampling successful. Generating dataset')
                        zs = torch.stack(zs, dim=0)
                        targets = torch.LongTensor(targets)
                        for i in trange(0, len(zs), batch_size):
                            gen = model.module.decode(zs[i:(i + batch_size)])
                            gen = torch.sigmoid(gen)
                            if autoregression:
                                gen = model.module.pixelcnn.generate(gen)
                            data.append(gen.data.cpu())
                        data = torch.cat(data, dim=0)
                        (_, sd_idx) = torch.sort(targets)
                        subset_idx = sd_idx[torch.floor(torch.arange(0, data.size(0), (data.size(0) / self.vis_size))).long()]
                        viz_subset = data[subset_idx]
                        imgs = torchvision.utils.make_grid(viz_subset, nrow=int(math.sqrt(self.vis_size)), padding=5)
                        torchvision.utils.save_image(viz_subset, os.path.join(save_path, (('samples_seen_tasks_' + str((len(self.seen_tasks) - self.num_increment_tasks))) + '.png')), nrow=int(math.sqrt(self.vis_size)), padding=5)
                        writer.add_image('openset_generation_snapshot', imgs, (len(self.seen_tasks) - self.num_increment_tasks))
                        trainset = torch.utils.data.TensorDataset(data, targets)
                        return trainset
            if ((not openset) or (not openset_success)):
                print('Using generative model to replay old data')
                for i in trange(int((seen_dataset_size / batch_size))):
                    z_samples = torch.randn(batch_size, model.module.latent_dim).to(self.device)
                    gen = model.module.decode(z_samples)
                    gen = torch.sigmoid(gen)
                    if autoregression:
                        gen = model.module.pixelcnn.generate(gen)
                    cl = model.module.classifier(z_samples)
                    cl = torch.nn.functional.softmax(cl, dim=1)
                    label = torch.argmax(cl, dim=1)
                    data.append(gen.data.cpu())
                    targets.append(label.data.cpu())
                data = torch.cat(data, dim=0)
                targets = torch.cat(targets, dim=0)
                (_, sd_idx) = torch.sort(targets)
                subset_idx = sd_idx[torch.floor(torch.arange(0, data.size(0), (data.size(0) / self.vis_size))).long()]
                viz_subset = data[subset_idx]
                imgs = torchvision.utils.make_grid(viz_subset, nrow=int(math.sqrt(self.vis_size)), padding=5)
                torchvision.utils.save_image(viz_subset, os.path.join(save_path, (('samples_seen_tasks_' + str((len(self.seen_tasks) - self.num_increment_tasks))) + '.png')), nrow=int(math.sqrt(self.vis_size)), padding=5)
                writer.add_image('dataset_generation_snapshot', imgs, (len(self.seen_tasks) - self.num_increment_tasks))
            trainset = torch.utils.data.TensorDataset(data, targets)
            return trainset
    return IncrementalDataset
