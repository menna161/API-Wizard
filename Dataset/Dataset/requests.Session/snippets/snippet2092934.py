import os
import io
import sys
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.backends.cudnn
from torchvision.transforms import Compose, Normalize
import mercantile
import requests
from PIL import Image
from flask import Flask, send_file, render_template, abort
from robosat.tiles import fetch_image
from robosat.unet import UNet
from robosat.config import load_config
from robosat.colors import make_palette
from robosat.transforms import ConvertImageMode, ImageToTensor


def main(args):
    model = load_config(args.model)
    dataset = load_config(args.dataset)
    cuda = model['common']['cuda']
    if (cuda and (not torch.cuda.is_available())):
        sys.exit('Error: CUDA requested but not available')
    global size
    size = args.tile_size
    global token
    token = os.getenv('MAPBOX_ACCESS_TOKEN')
    if (not token):
        sys.exit('Error: map token needed visualizing results; export MAPBOX_ACCESS_TOKEN')
    global session
    session = requests.Session()
    global tiles
    tiles = args.url
    global predictor
    predictor = Predictor(args.checkpoint, model, dataset)
    app.run(host=args.host, port=args.port, threaded=False)
