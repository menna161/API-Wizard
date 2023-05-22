import pyaudio
import time
import numpy as np
import threading


def initiate(self):
    'run this after changing settings (like rate) before recording'
    if (self.device is None):
        self.device = self.valid_input_devices()[0]
    if (self.rate is None):
        self.rate = self.valid_low_rate(self.device)
    self.chunk = int((self.rate / self.updatesPerSecond))
    if (not self.valid_test(self.device, self.rate)):
        print('guessing a valid microphone device/rate...')
        self.device = self.valid_input_devices()[0]
        self.rate = self.valid_low_rate(self.device)
    self.datax = (np.arange(self.chunk) / float(self.rate))
    msg = ('recording from "%s" ' % self.info['name'])
    msg += ('(device %d) ' % self.device)
    msg += ('at %d Hz' % self.rate)
    print(msg)
