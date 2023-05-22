import torch
import argparse
import numpy as np
import utils
from pathlib import Path
from datetime import datetime
from network import ContactsNet
from dataset import ProteinDataLoader

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Alphafold - PyTorch version')
    parser.add_argument('-i', '--input', type=str, required=True, help='target protein, support both .pkl or .tfrec format')
    parser.add_argument('-o', '--out', type=str, default='', help='output dir')
    parser.add_argument('-m', '--model', type=str, default='model', help='model dir')
    parser.add_argument('-r', '--replica', type=str, default='0', help='model replica')
    parser.add_argument('-t', '--type', type=str, choices=['D', 'B', 'T'], default='D', help='model type: D - Distogram, B - Background, T - Torsion')
    parser.add_argument('-e', '--ensemble', default=False, action='store_true', help='ensembling all replica outputs')
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='debug mode')
    args = parser.parse_args()
    DEBUG = args.debug
    TARGET_PATH = args.input
    timestr = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    OUT_DIR = (Path(args.out) if args.out else Path(f'contacts_{TARGET}_{timestr}'))
    if args.ensemble:
        ensemble(TARGET_PATH, OUT_DIR)
    else:
        DEVICE = torch.device(('cuda' if torch.cuda.is_available() else 'cpu'))
        TARGET = TARGET_PATH.split('/')[(- 1)].split('.')[0]
        REPLICA = args.replica
        if (args.type == 'D'):
            MODEL_TYPE = 'Distogram'
            MODEL_PATH = (Path(args.model) / '873731')
        elif (args.type == 'B'):
            MODEL_TYPE = 'Background'
            MODEL_PATH = (Path(args.model) / '916425')
        elif (args.type == 'T'):
            MODEL_TYPE = 'Torsion'
            MODEL_PATH = (Path(args.model) / '941521')
        OUT_DIR = ((OUT_DIR / MODEL_TYPE) / REPLICA)
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f'Input file: {TARGET_PATH}')
        print(f'Output dir: {OUT_DIR}')
        print(f'{MODEL_TYPE} model: {MODEL_PATH}')
        print(f'Replica: {REPLICA}')
        print(f'Device: {DEVICE}')
        run_eval(TARGET_PATH, MODEL_PATH, REPLICA, OUT_DIR, DEVICE)
