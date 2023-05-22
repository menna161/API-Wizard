import argparse
from os.path import join as pjoin
import numpy as np
import torch
import torch.nn.functional as F
from tensorboardX import SummaryWriter
import torchvision.utils as vutils
from core.loader.data_loader import *
from core.metrics import runningScore
from core.utils import np_to_tb


def test(args):
    device = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
    (log_dir, model_name) = os.path.split(args.model_path)
    model = torch.load(args.model_path)
    model = model.to(device)
    writer = SummaryWriter(log_dir=log_dir)
    class_names = ['upper_ns', 'middle_ns', 'lower_ns', 'rijnland_chalk', 'scruff', 'zechstein']
    running_metrics_overall = runningScore(6)
    if ('both' in args.split):
        splits = ['test1', 'test2']
    else:
        splits = args.split
    for (sdx, split) in enumerate(splits):
        labels = np.load(pjoin('data', 'test_once', (split + '_labels.npy')))
        (irange, xrange, depth) = labels.shape
        if args.inline:
            i_list = list(range(irange))
            i_list = [('i_' + str(inline)) for inline in i_list]
        else:
            i_list = []
        if args.crossline:
            x_list = list(range(xrange))
            x_list = [('x_' + str(crossline)) for crossline in x_list]
        else:
            x_list = []
        list_test = (i_list + x_list)
        file_object = open(pjoin('data', 'splits', (('section_' + split) + '.txt')), 'w')
        file_object.write('\n'.join(list_test))
        file_object.close()
        test_set = section_loader(is_transform=True, split=split, augmentations=None)
        n_classes = test_set.n_classes
        test_loader = data.DataLoader(test_set, batch_size=1, num_workers=4, shuffle=False)
        running_metrics_split = runningScore(n_classes)
        with torch.no_grad():
            model.eval()
            total_iteration = 0
            for (i, (images, labels)) in enumerate(test_loader):
                total_iteration = (total_iteration + 1)
                (image_original, labels_original) = (images, labels)
                (images, labels) = (images.to(device), labels.to(device))
                outputs = model(images)
                pred = outputs.detach().max(1)[1].cpu().numpy()
                gt = labels.detach().cpu().numpy()
                running_metrics_split.update(gt, pred)
                running_metrics_overall.update(gt, pred)
                numbers = [0, 99, 149, 399, 499]
                if (i in numbers):
                    tb_original_image = vutils.make_grid(image_original[0][0], normalize=True, scale_each=True)
                    writer.add_image('test/original_image', tb_original_image, i)
                    labels_original = labels_original.numpy()[0]
                    correct_label_decoded = test_set.decode_segmap(np.squeeze(labels_original))
                    writer.add_image('test/original_label', np_to_tb(correct_label_decoded), i)
                    out = F.softmax(outputs, dim=1)
                    prediction = out.max(1)[1].cpu().numpy()[0]
                    confidence = out.max(1)[0].cpu().detach()[0]
                    tb_confidence = vutils.make_grid(confidence, normalize=True, scale_each=True)
                    decoded = test_set.decode_segmap(np.squeeze(prediction))
                    writer.add_image('test/predicted', np_to_tb(decoded), i)
                    writer.add_image('test/confidence', tb_confidence, i)
                    unary = outputs.cpu().detach()
                    unary_max = torch.max(unary)
                    unary_min = torch.min(unary)
                    unary = unary.add(((- 1) * unary_min))
                    unary = (unary / (unary_max - unary_min))
                    for channel in range(0, len(class_names)):
                        decoded_channel = unary[0][channel]
                        tb_channel = vutils.make_grid(decoded_channel, normalize=True, scale_each=True)
                        writer.add_image(f'test_classes/_{class_names[channel]}', tb_channel, i)
        (score, class_iou) = running_metrics_split.get_scores()
        writer.add_text(f'test__{split}/', f"Pixel Acc: {score['Pixel Acc: ']:.3f}", 0)
        for (cdx, class_name) in enumerate(class_names):
            writer.add_text(f'test__{split}/', f"  {class_name}_accuracy {score['Class Accuracy: '][cdx]:.3f}", 0)
        writer.add_text(f'test__{split}/', f"Mean Class Acc: {score['Mean Class Acc: ']:.3f}", 0)
        writer.add_text(f'test__{split}/', f"Freq Weighted IoU: {score['Freq Weighted IoU: ']:.3f}", 0)
        writer.add_text(f'test__{split}/', f"Mean IoU: {score['Mean IoU: ']:0.3f}", 0)
        running_metrics_split.reset()
    (score, class_iou) = running_metrics_overall.get_scores()
    writer.add_text('test_final', f"Pixel Acc: {score['Pixel Acc: ']:.3f}", 0)
    for (cdx, class_name) in enumerate(class_names):
        writer.add_text('test_final', f"  {class_name}_accuracy {score['Class Accuracy: '][cdx]:.3f}", 0)
    writer.add_text('test_final', f"Mean Class Acc: {score['Mean Class Acc: ']:.3f}", 0)
    writer.add_text('test_final', f"Freq Weighted IoU: {score['Freq Weighted IoU: ']:.3f}", 0)
    writer.add_text('test_final', f"Mean IoU: {score['Mean IoU: ']:0.3f}", 0)
    print('--------------- FINAL RESULTS -----------------')
    print(f"Pixel Acc: {score['Pixel Acc: ']:.3f}")
    for (cdx, class_name) in enumerate(class_names):
        print(f"     {class_name}_accuracy {score['Class Accuracy: '][cdx]:.3f}")
    print(f"Mean Class Acc: {score['Mean Class Acc: ']:.3f}")
    print(f"Freq Weighted IoU: {score['Freq Weighted IoU: ']:.3f}")
    print(f"Mean IoU: {score['Mean IoU: ']:0.3f}")
    confusion = score['confusion_matrix']
    np.savetxt(pjoin(log_dir, 'confusion.csv'), confusion, delimiter=' ')
    writer.close()
    return
