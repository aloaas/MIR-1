import os.path

import numpy as np
import librosa
from pydub import AudioSegment
import matplotlib.pyplot as plt
import librosa.display
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def chunk(incoming, n_chunk):
    input_length = incoming.shape[1]
    chunk_length = input_length // n_chunk
    outputs = []
    for i in range(incoming.shape[0]):
        for j in range(n_chunk):
            outputs.append(incoming[i, j*chunk_length:(j+1)*chunk_length, :])
    outputs = np.array(outputs)
    return outputs


def audio_read(f):
    try:
        y, sr = librosa.core.load('data' + os.path.sep + f, sr=22050)
    except FileNotFoundError:
        y, sr = librosa.core.load(f, sr=22050)
    d = librosa.core.get_duration(y=y, sr=sr)
    S = librosa.feature.melspectrogram(y, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
    S_DB = librosa.power_to_db(S, ref=np.max)
    plot = plt.Figure()
    canvas = FigureCanvas(plot)
    ax = plot.add_subplot(111)

    hop_length = 512
    librosa.display.specshow(S_DB, sr=sr, hop_length=hop_length, ax=ax, x_axis='time', y_axis='mel')
    #plt.colorbar(format='%+2.0f dB', ax=ax)
    S = np.transpose(np.log(1+10000*S))
    S = np.expand_dims(S, axis=0)
    return y, S, int(d), plot, sr


def positional_encoding(batch_size, n_pos, d_pos):
    # keep dim 0 for padding token position encoding zero vector
    position_enc = np.array([
        [pos / np.power(10000, 2 * (j // 2) / d_pos) for j in range(d_pos)]
        if pos != 0 else np.zeros(d_pos) for pos in range(n_pos)])

    position_enc[1:, 0::2] = np.sin(position_enc[1:, 0::2]) # dim 2i
    position_enc[1:, 1::2] = np.cos(position_enc[1:, 1::2]) # dim 2i+1
    position_enc = np.tile(position_enc, [batch_size, 1, 1])
    return position_enc
