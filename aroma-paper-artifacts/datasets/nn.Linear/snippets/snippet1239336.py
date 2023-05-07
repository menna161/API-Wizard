import torch, numpy, os, argparse, sys, shutil, errno, numbers
from PIL import Image
from torch.utils.data import TensorDataset
from netdissect.zdataset import standard_z_sample
from netdissect.progress import default_progress, verbose_progress
from netdissect.autoeval import autoimport_eval
from netdissect.workerpool import WorkerBase, WorkerPool
from netdissect.nethook import retain_layers
from netdissect.runningstats import RunningTopK


def main():
    parser = argparse.ArgumentParser(description='GAN sample making utility')
    parser.add_argument('--model', type=str, default=None, help='constructor for the model to test')
    parser.add_argument('--pthfile', type=str, default=None, help='filename of .pth file for the model')
    parser.add_argument('--outdir', type=str, default='images', help='directory for image output')
    parser.add_argument('--size', type=int, default=100, help='number of images to output')
    parser.add_argument('--test_size', type=int, default=None, help='number of images to test')
    parser.add_argument('--layer', type=str, default=None, help='layer to inspect')
    parser.add_argument('--seed', type=int, default=1, help='seed')
    parser.add_argument('--quiet', action='store_true', default=False, help='silences console output')
    if (len(sys.argv) == 1):
        parser.print_usage(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    verbose_progress((not args.quiet))
    model = autoimport_eval(args.model)
    if (args.pthfile is not None):
        data = torch.load(args.pthfile)
        if ('state_dict' in data):
            meta = {}
            for key in data:
                if isinstance(data[key], numbers.Number):
                    meta[key] = data[key]
            data = data['state_dict']
        model.load_state_dict(data)
    if isinstance(model, torch.nn.DataParallel):
        model = next(model.children())
    first_layer = [c for c in model.modules() if isinstance(c, (torch.nn.Conv2d, torch.nn.ConvTranspose2d, torch.nn.Linear))][0]
    if isinstance(first_layer, (torch.nn.Conv2d, torch.nn.ConvTranspose2d)):
        z_channels = first_layer.in_channels
        spatialdims = (1, 1)
    else:
        z_channels = first_layer.in_features
        spatialdims = ()
    retain_layers(model, [args.layer])
    model.cuda()
    if (args.test_size is None):
        args.test_size = (args.size * 20)
    z_universe = standard_z_sample(args.test_size, z_channels, seed=args.seed)
    z_universe = z_universe.view((tuple(z_universe.shape) + spatialdims))
    indexes = get_all_highest_znums(model, z_universe, args.size, seed=args.seed)
    save_chosen_unit_images(args.outdir, model, z_universe, indexes, lightbox=True)
