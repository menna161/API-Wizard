import torch, numpy, os, argparse, numbers, sys, shutil
from PIL import Image
from torch.utils.data import TensorDataset
from netdissect.zdataset import standard_z_sample
from netdissect.progress import default_progress, verbose_progress
from netdissect.autoeval import autoimport_eval
from netdissect.workerpool import WorkerBase, WorkerPool
from netdissect.nethook import edit_layers, retain_layers


def main():
    parser = argparse.ArgumentParser(description='GAN sample making utility')
    parser.add_argument('--model', type=str, default=None, help='constructor for the model to test')
    parser.add_argument('--pthfile', type=str, default=None, help='filename of .pth file for the model')
    parser.add_argument('--outdir', type=str, default='images', help='directory for image output')
    parser.add_argument('--size', type=int, default=100, help='number of images to output')
    parser.add_argument('--test_size', type=int, default=None, help='number of images to test')
    parser.add_argument('--layer', type=str, default=None, help='layer to inspect')
    parser.add_argument('--seed', type=int, default=1, help='seed')
    parser.add_argument('--maximize_units', type=int, nargs='+', default=None, help='units to maximize')
    parser.add_argument('--ablate_units', type=int, nargs='+', default=None, help='units to ablate')
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
    if (args.maximize_units is not None):
        retain_layers(model, [args.layer])
    model.cuda()
    if (args.maximize_units is None):
        indexes = torch.arange(args.size)
        z_sample = standard_z_sample(args.size, z_channels, seed=args.seed)
        z_sample = z_sample.view((tuple(z_sample.shape) + spatialdims))
    else:
        if (args.test_size is None):
            args.test_size = (args.size * 20)
        z_universe = standard_z_sample(args.test_size, z_channels, seed=args.seed)
        z_universe = z_universe.view((tuple(z_universe.shape) + spatialdims))
        indexes = get_highest_znums(model, z_universe, args.maximize_units, args.size, seed=args.seed)
        z_sample = z_universe[indexes]
    if args.ablate_units:
        edit_layers(model, [args.layer])
        dims = max(2, (max(args.ablate_units) + 1))
        model.ablation[args.layer] = torch.zeros(dims)
        model.ablation[args.layer][args.ablate_units] = 1
    save_znum_images(args.outdir, model, z_sample, indexes, args.layer, args.ablate_units)
    copy_lightbox_to(args.outdir)
