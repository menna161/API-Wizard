import torch
import torch.nn as nn
import time
import argparse

if (__name__ == '__main__'):
    num_classes = 28
    input_size = 1
    model_path = 'model/Adam_batch_size=2048_epoch=300.pt'
    parser = argparse.ArgumentParser()
    parser.add_argument('-num_layers', default=2, type=int)
    parser.add_argument('-hidden_size', default=64, type=int)
    parser.add_argument('-window_size', default=10, type=int)
    parser.add_argument('-num_candidates', default=9, type=int)
    args = parser.parse_args()
    num_layers = args.num_layers
    hidden_size = args.hidden_size
    window_size = args.window_size
    num_candidates = args.num_candidates
    model = Model(input_size, hidden_size, num_layers, num_classes).to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print('model_path: {}'.format(model_path))
    test_normal_loader = generate('hdfs_test_normal')
    test_abnormal_loader = generate('hdfs_test_abnormal')
    TP = 0
    FP = 0
    start_time = time.time()
    with torch.no_grad():
        for line in test_normal_loader:
            for i in range((len(line) - window_size)):
                seq = line[i:(i + window_size)]
                label = line[(i + window_size)]
                seq = torch.tensor(seq, dtype=torch.float).view((- 1), window_size, input_size).to(device)
                label = torch.tensor(label).view((- 1)).to(device)
                output = model(seq)
                predicted = torch.argsort(output, 1)[0][(- num_candidates):]
                if (label not in predicted):
                    FP += 1
                    break
    with torch.no_grad():
        for line in test_abnormal_loader:
            for i in range((len(line) - window_size)):
                seq = line[i:(i + window_size)]
                label = line[(i + window_size)]
                seq = torch.tensor(seq, dtype=torch.float).view((- 1), window_size, input_size).to(device)
                label = torch.tensor(label).view((- 1)).to(device)
                output = model(seq)
                predicted = torch.argsort(output, 1)[0][(- num_candidates):]
                if (label not in predicted):
                    TP += 1
                    break
    elapsed_time = (time.time() - start_time)
    print('elapsed_time: {:.3f}s'.format(elapsed_time))
    FN = (len(test_abnormal_loader) - TP)
    P = ((100 * TP) / (TP + FP))
    R = ((100 * TP) / (TP + FN))
    F1 = (((2 * P) * R) / (P + R))
    print('false positive (FP): {}, false negative (FN): {}, Precision: {:.3f}%, Recall: {:.3f}%, F1-measure: {:.3f}%'.format(FP, FN, P, R, F1))
    print('Finished Predicting')
