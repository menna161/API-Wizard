from collections import OrderedDict
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *
from multiprocessing import Pool
import numpy as np
from nnunet.configuration import default_num_threads
from scipy.ndimage import label


def export_segmentations_postprocess(indir, outdir):
    maybe_mkdir_p(outdir)
    niftis = subfiles(indir, suffix='nii.gz', join=False)
    for n in niftis:
        print('\n', n)
        identifier = str(n.split('_')[(- 1)][:(- 7)])
        outfname = join(outdir, ('test-segmentation-%s.nii' % identifier))
        img = sitk.ReadImage(join(indir, n))
        img_npy = sitk.GetArrayFromImage(img)
        (lmap, num_objects) = label((img_npy > 0).astype(int))
        sizes = []
        for o in range(1, (num_objects + 1)):
            sizes.append((lmap == o).sum())
        mx = (np.argmax(sizes) + 1)
        print(sizes)
        img_npy[(lmap != mx)] = 0
        img_new = sitk.GetImageFromArray(img_npy)
        img_new.CopyInformation(img)
        sitk.WriteImage(img_new, outfname)
