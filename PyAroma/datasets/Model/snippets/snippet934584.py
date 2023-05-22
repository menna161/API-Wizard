import os
import sys
import random
import time
import traceback
import torch
import torch.optim as optim
from configs import g_conf, set_type_of_process, merge_with_yaml
from network import CoILModel, Loss, adjust_learning_rate_auto
from input import CoILDataset, Augmenter, select_balancing_strategy
from logger import coil_logger
from coilutils.checkpoint_schedule import is_ready_to_save, get_latest_saved_checkpoint, check_loss_validation_stopped


def execute(gpu, exp_batch, exp_alias, suppress_output=True, number_of_workers=12):
    '\n        The main training function. This functions loads the latest checkpoint\n        for a given, exp_batch (folder) and exp_alias (experiment configuration).\n        With this checkpoint it starts from the beginning or continue some training.\n    Args:\n        gpu: The GPU number\n        exp_batch: the folder with the experiments\n        exp_alias: the alias, experiment name\n        suppress_output: if the output are going to be saved on a file\n        number_of_workers: the number of threads used for data loading\n\n    Returns:\n        None\n\n    '
    try:
        os.environ['CUDA_VISIBLE_DEVICES'] = gpu
        g_conf.VARIABLE_WEIGHT = {}
        merge_with_yaml(os.path.join('configs', exp_batch, (exp_alias + '.yaml')))
        set_type_of_process('train')
        coil_logger.add_message('Loading', {'GPU': gpu})
        if suppress_output:
            if (not os.path.exists('_output_logs')):
                os.mkdir('_output_logs')
            sys.stdout = open(os.path.join('_output_logs', (((((exp_alias + '_') + g_conf.PROCESS_NAME) + '_') + str(os.getpid())) + '.out')), 'a', buffering=1)
            sys.stderr = open(os.path.join('_output_logs', (((((exp_alias + '_err_') + g_conf.PROCESS_NAME) + '_') + str(os.getpid())) + '.out')), 'a', buffering=1)
        if coil_logger.check_finish('train'):
            coil_logger.add_message('Finished', {})
            return
        if (g_conf.PRELOAD_MODEL_ALIAS is not None):
            checkpoint = torch.load(os.path.join('_logs', g_conf.PRELOAD_MODEL_BATCH, g_conf.PRELOAD_MODEL_ALIAS, 'checkpoints', (str(g_conf.PRELOAD_MODEL_CHECKPOINT) + '.pth')))
        checkpoint_file = get_latest_saved_checkpoint()
        if (checkpoint_file is not None):
            checkpoint = torch.load(os.path.join('_logs', exp_batch, exp_alias, 'checkpoints', str(get_latest_saved_checkpoint())))
            iteration = checkpoint['iteration']
            best_loss = checkpoint['best_loss']
            best_loss_iter = checkpoint['best_loss_iter']
        else:
            iteration = 0
            best_loss = 10000.0
            best_loss_iter = 0
        full_dataset = os.path.join(os.environ['COIL_DATASET_PATH'], g_conf.TRAIN_DATASET_NAME)
        augmenter = Augmenter(g_conf.AUGMENTATION)
        dataset = CoILDataset(full_dataset, transform=augmenter, preload_name=((str(g_conf.NUMBER_OF_HOURS) + 'hours_') + g_conf.TRAIN_DATASET_NAME))
        print('Loaded dataset')
        data_loader = select_balancing_strategy(dataset, iteration, number_of_workers)
        model = CoILModel(g_conf.MODEL_TYPE, g_conf.MODEL_CONFIGURATION)
        model.cuda()
        optimizer = optim.Adam(model.parameters(), lr=g_conf.LEARNING_RATE)
        if ((checkpoint_file is not None) or (g_conf.PRELOAD_MODEL_ALIAS is not None)):
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            accumulated_time = checkpoint['total_time']
            loss_window = coil_logger.recover_loss_window('train', iteration)
        else:
            accumulated_time = 0
            loss_window = []
        print('Before the loss')
        criterion = Loss(g_conf.LOSS_FUNCTION)
        for data in data_loader:
            if ((g_conf.FINISH_ON_VALIDATION_STALE is not None) and check_loss_validation_stopped(iteration, g_conf.FINISH_ON_VALIDATION_STALE)):
                break
            '\n                ####################################\n                    Main optimization loop\n                ####################################\n            '
            iteration += 1
            if ((iteration % 1000) == 0):
                adjust_learning_rate_auto(optimizer, loss_window)
            capture_time = time.time()
            controls = data['directions']
            model.zero_grad()
            branches = model(torch.squeeze(data['rgb'].cuda()), dataset.extract_inputs(data).cuda())
            loss_function_params = {'branches': branches, 'targets': dataset.extract_targets(data).cuda(), 'controls': controls.cuda(), 'inputs': dataset.extract_inputs(data).cuda(), 'branch_weights': g_conf.BRANCH_LOSS_WEIGHT, 'variable_weights': g_conf.VARIABLE_WEIGHT}
            (loss, _) = criterion(loss_function_params)
            loss.backward()
            optimizer.step()
            '\n                ####################################\n                    Saving the model if necessary\n                ####################################\n            '
            if is_ready_to_save(iteration):
                state = {'iteration': iteration, 'state_dict': model.state_dict(), 'best_loss': best_loss, 'total_time': accumulated_time, 'optimizer': optimizer.state_dict(), 'best_loss_iter': best_loss_iter}
                torch.save(state, os.path.join('_logs', exp_batch, exp_alias, 'checkpoints', (str(iteration) + '.pth')))
            '\n                ################################################\n                    Adding tensorboard logs.\n                    Making calculations for logging purposes.\n                    These logs are monitored by the printer module.\n                #################################################\n            '
            coil_logger.add_scalar('Loss', loss.data, iteration)
            coil_logger.add_image('Image', torch.squeeze(data['rgb']), iteration)
            if (loss.data < best_loss):
                best_loss = loss.data.tolist()
                best_loss_iter = iteration
            position = random.randint(0, (len(data) - 1))
            output = model.extract_branch(torch.stack(branches[0:4]), controls)
            error = torch.abs((output - dataset.extract_targets(data).cuda()))
            accumulated_time += (time.time() - capture_time)
            coil_logger.add_message('Iterating', {'Iteration': iteration, 'Loss': loss.data.tolist(), 'Images/s': ((iteration * g_conf.BATCH_SIZE) / accumulated_time), 'BestLoss': best_loss, 'BestLossIteration': best_loss_iter, 'Output': output[position].data.tolist(), 'GroundTruth': dataset.extract_targets(data)[position].data.tolist(), 'Error': error[position].data.tolist(), 'Inputs': dataset.extract_inputs(data)[position].data.tolist()}, iteration)
            loss_window.append(loss.data.tolist())
            coil_logger.write_on_error_csv('train', loss.data)
            print(('Iteration: %d  Loss: %f' % (iteration, loss.data)))
        coil_logger.add_message('Finished', {})
    except KeyboardInterrupt:
        coil_logger.add_message('Error', {'Message': 'Killed By User'})
    except RuntimeError as e:
        coil_logger.add_message('Error', {'Message': str(e)})
    except:
        traceback.print_exc()
        coil_logger.add_message('Error', {'Message': 'Something Happened'})
