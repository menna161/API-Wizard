import pickle
import numpy as np
import matplotlib.pyplot as plt
from am_analysis import am_analysis as ama
import time
from copy import deepcopy

if (__name__ == '__main__'):
    [x, fs] = pickle.load(open('./example_data/ecg_data.pkl', 'rb'))
    segment_length = 5
    segment_overlap = 0
    T = (1 / fs)
    n = x.shape[0]
    energy_x = (T * sum((x ** 2))[0])
    duration = (T * n)
    power_x = (energy_x / duration)
    tic = time.time()
    (x_segmented, _, _) = ama.epoching(x, round((segment_length * fs)))
    n_segments = x_segmented.shape[2]
    wavelet_spectrogram_data_a = []
    wavelet_modulation_spectrogram_data_a = []
    for i_segment in range(0, n_segments):
        x_tmp_wavelet = x_segmented[:, :, i_segment]
        wavelet_spectrogram_data_a.append(ama.wavelet_spectrogram(x_tmp_wavelet, fs))
        wavelet_modulation_spectrogram_data_a.append(ama.wavelet_modulation_spectrogram(x_tmp_wavelet, fs))
    toc = (time.time() - tic)
    print((str(toc) + ' seconds'))
    tic = time.time()
    wavelet_spect_data = ama.wavelet_spectrogram(x, fs)
    (wavelet_spect_segmented, _, _) = ama.epoching(np.squeeze(wavelet_spect_data['power_spectrogram']), round((segment_length * fs)))
    n_segments = wavelet_spect_segmented.shape[2]
    wavelet_spect_segmented = (n_segments * wavelet_spect_segmented)
    wavelet_spectrogram_power_b = []
    wavelet_modulation_spectrogram_power_b = []
    for i_segment in range(0, n_segments):
        wavelet_spectrogram_power_b.append(wavelet_spect_segmented[:, :, i_segment])
        x_tmp_wavelet = np.sqrt(np.squeeze(wavelet_spect_segmented[:, :, i_segment]))
        mod_psd_wavelet = ama.rfft_psd(x_tmp_wavelet, fs)
        wavelet_modulation_spectrogram_power_b.append((mod_psd_wavelet['PSD'] / mod_psd_wavelet['freq_delta']))
    toc = (time.time() - tic)
    print((str(toc) + ' seconds'))
    wavelet_spectrogram_data_b = deepcopy(wavelet_spectrogram_data_a)
    wavelet_modulation_spectrogram_data_b = deepcopy(wavelet_modulation_spectrogram_data_a)
    for i_segment in range(0, n_segments):
        wavelet_spectrogram_data_b[i_segment]['power_spectrogram'] = wavelet_spectrogram_power_b[i_segment][:, :, np.newaxis]
        wavelet_modulation_spectrogram_data_b[i_segment]['power_modulation_spectrogram'] = np.transpose(wavelet_modulation_spectrogram_power_b[i_segment])[:, :, np.newaxis]
    random_segment = np.random.randint(0, n_segments)
    pwr_spectrogram_wavelet_a = np.zeros(n_segments)
    pwr_spectrogram_wavelet_b = np.zeros(n_segments)
    pwr_modulation_spectrogram_wavelet_a = np.zeros(n_segments)
    pwr_modulation_spectrogram_wavelet_b = np.zeros(n_segments)
    for i_segment in range(0, n_segments):
        if (i_segment == random_segment):
            plt.figure()
            plt.subplot(1, 2, 1)
            ama.plot_spectrogram_data(wavelet_spectrogram_data_a[i_segment], 0)
            plt.subplot(1, 2, 2)
            ama.plot_spectrogram_data(wavelet_spectrogram_data_b[i_segment], 0)
            plt.figure()
            plt.subplot(1, 2, 1)
            ama.plot_modulation_spectrogram_data(wavelet_modulation_spectrogram_data_a[i_segment], 0)
            plt.subplot(1, 2, 2)
            ama.plot_modulation_spectrogram_data(wavelet_modulation_spectrogram_data_b[i_segment], 0)
        pwr_spectrogram_wavelet_a[i_segment] = ((sum(sum(wavelet_spectrogram_data_a[i_segment]['power_spectrogram'])) * wavelet_spectrogram_data_a[0]['freq_delta']) * wavelet_spectrogram_data_a[0]['time_delta'])
        pwr_spectrogram_wavelet_b[i_segment] = ((sum(sum(wavelet_spectrogram_data_b[i_segment]['power_spectrogram'])) * wavelet_spectrogram_data_b[0]['freq_delta']) * wavelet_spectrogram_data_b[0]['time_delta'])
        pwr_modulation_spectrogram_wavelet_a[i_segment] = ((sum(sum(wavelet_modulation_spectrogram_data_a[i_segment]['power_modulation_spectrogram'])) * wavelet_modulation_spectrogram_data_a[0]['freq_delta']) * wavelet_modulation_spectrogram_data_a[0]['freq_mod_delta'])
        pwr_modulation_spectrogram_wavelet_b[i_segment] = ((sum(sum(wavelet_modulation_spectrogram_data_b[i_segment]['power_modulation_spectrogram'])) * wavelet_modulation_spectrogram_data_b[0]['freq_delta']) * wavelet_modulation_spectrogram_data_b[0]['freq_mod_delta'])
    plt.figure()
    plt.title('Total Power per Epoch, based on Spectrogram')
    plt.plot(pwr_spectrogram_wavelet_a, label='Wavelet Spectrogram A')
    plt.plot(pwr_spectrogram_wavelet_b, label='Wavelet Spectrogram B')
    plt.legend()
    print(('Mean Power Spectrogram A: ' + str(np.mean(pwr_spectrogram_wavelet_a))))
    print(('Mean Power Spectrogram B: ' + str(np.mean(pwr_spectrogram_wavelet_b))))
    plt.figure()
    plt.title('Total Power per Epoch, based on Modulation Spectrogram')
    plt.plot(pwr_modulation_spectrogram_wavelet_a, label='Wavelet Modulation Spectrogram A')
    plt.plot(pwr_modulation_spectrogram_wavelet_b, label='Wavelet Modulation Spectrogram B')
    plt.legend()
    print(('Mean Power Modulation Spectrogram A: ' + str(np.mean(pwr_modulation_spectrogram_wavelet_a))))
    print(('Mean Power Modulation Spectrogram B: ' + str(np.mean(pwr_modulation_spectrogram_wavelet_b))))
    plt.show()
