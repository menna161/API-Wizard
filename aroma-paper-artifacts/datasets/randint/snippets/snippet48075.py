import os
import errno
import wget
import zipfile
import glob
import librosa
import scipy
import math
from tqdm import tqdm
import torch
import torch.utils.data
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import numpy as np
import scipy.io.wavfile as wavf


def __download(self):
    "\n        Downloads the AudioMNIST dataset from the web if dataset\n        hasn't already been downloaded and does a spectrogram conversion.\n        The latter could potentially be refactored into a separate function and conversion parameters (here hard-coded\n        according to original authors) exposed to the command line parser.\n        "
    if self.__check_exists():
        return
    print('Downloading AudioMNIST dataset')
    try:
        os.makedirs(self.__path)
    except OSError as e:
        if (e.errno == errno.EEXIST):
            pass
        else:
            raise
    if (not os.path.exists(os.path.join(self.__path, 'AudioMNIST-master.zip'))):
        url = 'https://github.com/soerenab/AudioMNIST/archive/master.zip'
        wget_data = wget.download(url, out=self.__path)
        archive = zipfile.ZipFile(wget_data)
        for file in archive.namelist():
            if file.startswith('AudioMNIST-master/data/'):
                archive.extract(file, self.__path)
        print('Download successful')
    audio_mnist_src = os.path.join(self.__path, 'AudioMNIST-master/data/')
    data = np.array(glob.glob(os.path.join(audio_mnist_src, '**/*.wav')))
    train_images = []
    train_labels = []
    test_images = []
    test_labels = []
    train_folders = [28, 56, 7, 19, 35, 1, 6, 16, 23, 34, 46, 53, 36, 57, 9, 24, 37, 2, 8, 17, 29, 39, 48, 54, 43, 58, 14, 25, 38, 3, 10, 20, 30, 40, 49, 55, 12, 47, 59, 15, 27, 41, 4, 11, 21, 31, 44, 50]
    test_folders = [26, 52, 60, 18, 32, 42, 5, 13, 22, 33, 45, 51]
    print('Converting audio to images')
    for filepath in tqdm(data):
        (dig, vp, rep) = filepath.rstrip('.wav').split('/')[(- 1)].split('_')
        (fs, data) = wavf.read(filepath)
        data = librosa.core.resample(y=data.astype(np.float32), orig_sr=fs, target_sr=8000, res_type='scipy')
        if (len(data) > 8000):
            raise ValueError('data length cannot exceed padding length.')
        elif (len(data) < 8000):
            embedded_data = np.zeros(8000)
            offset = np.random.randint(low=0, high=(8000 - len(data)))
            embedded_data[offset:(offset + len(data))] = data
        elif (len(data) == 8000):
            embedded_data = data
            pass
        (f, t, zxx) = scipy.signal.stft(embedded_data, 8000, nperseg=455, noverlap=420, window='hann')
        zxx = np.abs(zxx[(0:227, 2:(- 1))])
        zxx = librosa.amplitude_to_db(zxx, ref=np.max)
        zxx = ((zxx - zxx.min()) / (zxx.max() - zxx.min()))
        zxx = zxx[::(- 1)]
        zxx = np.atleast_3d(zxx).transpose(2, 0, 1)
        if (int(vp) in train_folders):
            train_images.append(zxx)
            train_labels.append(int(dig))
        elif (int(vp) in test_folders):
            test_images.append(zxx)
            test_labels.append(int(dig))
        else:
            raise Exception('Person neither in train nor in test set!')
    train_images = torch.Tensor(train_images).float()
    train_labels = torch.Tensor(train_labels).long()
    test_images = torch.Tensor(test_images).float()
    test_labels = torch.Tensor(test_labels).long()
    torch.save(train_images, os.path.join(self.__path, 'train_images_tensor.pt'))
    torch.save(train_labels, os.path.join(self.__path, 'train_labels_tensor.pt'))
    torch.save(test_images, os.path.join(self.__path, 'test_images_tensor.pt'))
    torch.save(test_labels, os.path.join(self.__path, 'test_labels_tensor.pt'))
    print('Done!')
