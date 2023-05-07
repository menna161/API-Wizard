import argparse
import logging
import math
import os
import cv2
import numpy as np
import torch
import data.hd3data as hd3data
import data.flowtransforms as transforms
import hd3model
import losses
from models.hd3_ops import resize_dense_vector
from models_refine.refinement_networks import PPacNet
import prob_utils
import refinement_models
from utils import flowlib, utils


def main():
    global args
    args = get_parser().parse_args()
    LOGGER.info(args)
    with open(args.data_list, 'r') as file_list:
        fnames = file_list.readlines()
        assert (len(fnames[0].strip().split(' ')) == ((2 + args.evaluate) + (args.evaluate * args.additional_flow_masks)))
        input_size = cv2.imread(os.path.join(args.data_root, fnames[0].split(' ')[0])).shape
        if (args.visualize or args.save_inputs or args.save_refined):
            names = [l.strip().split(' ')[0].split('/')[(- 1)] for l in fnames]
            sub_folders = [l.strip().split(' ')[0][:(- len(names[i]))] for (i, l) in enumerate(fnames)]
            names = [l.split('.')[0] for l in names]
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    (target_height, target_width) = get_target_size(input_size[0], input_size[1])
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=mean, std=std)])
    data = hd3data.HD3Data(mode='flow', data_root=args.data_root, data_list=args.data_list, label_num=(args.evaluate + (args.evaluate * args.additional_flow_masks)), transform=transform, out_size=True)
    data_loader = torch.utils.data.DataLoader(data, batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=True)
    model_hd3 = hd3model.HD3Model('flow', args.encoder, args.decoder, [4, 4, 4, 4, 4], args.context).cuda()
    model_hd3 = torch.nn.DataParallel(model_hd3).cuda()
    model_hd3.eval()
    refinement_network = PPacNet(args.kernel_size_preprocessing, args.kernel_size_joint, args.conv_specification, args.shared_filters, args.depth_layers_prob, args.depth_layers_guidance, args.depth_layers_joint)
    model_refine = refinement_models.EpeNet(refinement_network).cuda()
    model_refine = torch.nn.DataParallel(model_refine).cuda()
    model_refine.eval()
    name_hd3_model = args.model_hd3_path
    if os.path.isfile(name_hd3_model):
        checkpoint = torch.load(name_hd3_model)
        model_hd3.load_state_dict(checkpoint['state_dict'])
        LOGGER.info("Loaded HD3 checkpoint '{}'".format(name_hd3_model))
    else:
        LOGGER.info("No checkpoint found at '{}'".format(name_hd3_model))
    name_refinement_model = args.model_refine_path
    if os.path.isfile(name_refinement_model):
        checkpoint = torch.load(name_refinement_model)
        model_refine.load_state_dict(checkpoint['state_dict'])
        LOGGER.info("Loaded refinement checkpoint '{}'".format(name_refinement_model))
    else:
        LOGGER.info("No checkpoint found at '{}'".format(name_refinement_model))
    if args.evaluate:
        epe_hd3 = utils.AverageMeter()
        outliers_hd3 = utils.AverageMeter()
        epe_refined = utils.AverageMeter()
        outliers_refined = utils.AverageMeter()
    if args.visualize:
        visualization_folder = os.path.join(args.save_folder, 'visualizations')
        utils.check_makedirs(visualization_folder)
    if args.save_inputs:
        input_folder = os.path.join(args.save_folder, 'hd3_inputs')
        utils.check_makedirs(input_folder)
    if args.save_refined:
        refined_folder = os.path.join(args.save_folder, 'refined_flow')
        utils.check_makedirs(refined_folder)
    with torch.no_grad():
        for (i, (img_list, label_list, img_size)) in enumerate(data_loader):
            if ((i % 10) == 0):
                LOGGER.info('Done with {}/{} samples'.format(i, len(data_loader)))
            img_size = img_size.cpu().numpy()
            img_list = [img.to(torch.device('cuda')) for img in img_list]
            label_list = [label.to(torch.device('cuda')) for label in label_list]
            resized_img_list = [torch.nn.functional.interpolate(img, (target_height, target_width), mode='bilinear', align_corners=True) for img in img_list]
            output = model_hd3(img_list=resized_img_list, label_list=label_list, get_full_vect=True, get_full_prob=True, get_epe=args.evaluate)
            for (level, level_flow) in enumerate(output['full_vect']):
                scale_factor = (1 / (2 ** (6 - level)))
                output['full_vect'][level] = resize_dense_vector((level_flow * scale_factor), img_size[(0, 1)], img_size[(0, 0)])
            hd3_flow = output['full_vect'][(- 1)]
            if args.evaluate:
                epe_hd3.update(losses.endpoint_error(hd3_flow, label_list[0]).mean().data, hd3_flow.size(0))
                outliers_hd3.update(losses.outlier_rate(hd3_flow, label_list[0]).mean().data, hd3_flow.size(0))
            probabilities = prob_utils.get_upsampled_probabilities_hd3(output['full_vect'], output['full_prob'])
            if args.save_inputs:
                save_hd3_inputs(hd3_flow, probabilities, input_folder, sub_folders[(i * args.batch_size):((i + 1) * args.batch_size)], names[(i * args.batch_size):((i + 1) * args.batch_size)])
                continue
            log_probabilities = prob_utils.safe_log(probabilities)
            output_refine = model_refine(hd3_flow, log_probabilities, img_list[0], label_list=label_list, get_loss=args.evaluate, get_epe=args.evaluate, get_outliers=args.evaluate)
            if args.evaluate:
                epe_refined.update(output_refine['epe'].mean().data, hd3_flow.size(0))
                outliers_refined.update(output_refine['outliers'].mean().data, hd3_flow.size(0))
            if args.visualize:
                refined_flow = output_refine['flow']
                ground_truth = None
                if args.evaluate:
                    ground_truth = label_list[0][(:, :2)]
                save_visualizations(hd3_flow, refined_flow, ground_truth, visualization_folder, sub_folders[(i * args.batch_size):((i + 1) * args.batch_size)], names[(i * args.batch_size):((i + 1) * args.batch_size)])
            if args.save_refined:
                refined_flow = output_refine['flow']
                save_refined_flow(refined_flow, refined_folder, sub_folders[(i * args.batch_size):((i + 1) * args.batch_size)], names[(i * args.batch_size):((i + 1) * args.batch_size)])
    if args.evaluate:
        LOGGER.info('Accuracy of HD3 optical flow:      AEE={epe_hd3.avg:.4f}, Outliers={outliers_hd3.avg:.4f}'.format(epe_hd3=epe_hd3, outliers_hd3=outliers_hd3))
        if (not args.save_inputs):
            LOGGER.info('Accuracy of refined optical flow:  AEE={epe_refined.avg:.4f}, Outliers={outliers_refined.avg:.4f}'.format(epe_refined=epe_refined, outliers_refined=outliers_refined))
