import io
from pathlib import Path

from .model import MusicHighlighter
from .lib import *
import tensorflow as tf
import numpy as np
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ''

def plot_nn(score, highlight, fig):
    fig = plt.figure(fig)
    plt.plot(score, label='Score')
    plt.axvline(highlight[0], color='red', label='Start of thumbnail')
    plt.axvline(highlight[1], color='red', label='End of thumbnail')
    plt.xlabel('Time (frames)')
    plt.ylabel('Score')
    return fig

def extract(fs, name=None, length=30, save_score=True, save_thumbnail=True, save_wav=True, st=None):
    for f in fs:
        with tf.Session() as sess:

            model = MusicHighlighter()
            sess.run(tf.global_variables_initializer())

            # name = "".join(".".join(f.split('.')[:-1]).split("/")[1:])  # If we want file names with it.

            model.saver.restore(sess, "pop_music_highlighter" + os.path.sep + "model" + os.path.sep + "model")

            audio, spectrogram, duration, mel_plot, sr = audio_read(f)
            #st.pyplot(spectrogram)
            n_chunk, remainder = np.divmod(duration, 3)
            chunk_spec = chunk(spectrogram, n_chunk)
            pos = positional_encoding(batch_size=1, n_pos=n_chunk, d_pos=model.dim_feature * 4)

            n_chunk = n_chunk.astype('int')
            chunk_spec = chunk_spec.astype('float')
            pos = pos.astype('float')

            attn_score = model.calculate(sess=sess, x=chunk_spec, pos_enc=pos, num_chunk=n_chunk)
            attn_score = np.repeat(attn_score, 3)
            attn_score = np.append(attn_score, np.zeros(remainder))

            # score
            attn_score = attn_score / attn_score.max()
            score = attn_score
            st.write(n_chunk)

            if save_score:
                if not os.path.exists("output" + os.path.sep + "attention"):
                    os.mkdir("output" + os.path.sep + "attention")
                np.save('output' + os.path.sep + 'attention' + os.path.sep + '{}_score.npy'.format(name), attn_score)

            # thumbnail

            attn_score = attn_score.cumsum()
            attn_score = np.append(attn_score[length], attn_score[length:] - attn_score[:-length])
            index = np.argmax(attn_score)
            highlight = [index, index + length]
            st.text(highlight)
            st.pyplot(plot_nn(score, highlight, audio, sr))
            if save_thumbnail:
                if not os.path.exists("output" + os.path.sep + "attention"):
                    os.mkdir("output" + os.path.sep + "attention")

                np.save('output' + os.path.sep + 'attention' + os.path.sep + '{}_highlight.npy'.format(name), highlight)
            print('output' + os.path.sep + 'attention' + os.path.sep + '{}_highlight.npy'.format(name))
            if save_wav:
                if not os.path.exists("output" + os.path.sep + "attention"):
                    os.mkdir("output" + os.path.sep + "attention")

                librosa.output.write_wav('output' + os.path.sep + 'attention' + os.path.sep + '{}_audio.wav'.format(name),
                                         audio[highlight[0] * 22050:highlight[1] * 22050], 22050)


if __name__ == '__main__':
    fs = ["data/Pink Floyd - The Great Gig in The Sky.wav", "data/FMP_C4_Audio_Beatles_YouCantDoThat.wav"]
    # fs = ["data/Pink Floyd - The Great Gig in The Sky.wav"]
    extract(fs, length=10, save_score=True, save_thumbnail=True, save_wav=True)
