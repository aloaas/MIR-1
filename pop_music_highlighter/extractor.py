import io
from pathlib import Path

from .model import MusicHighlighter
from .lib import *
import tensorflow as tf
import numpy as np
import os
import matplotlib.colors

os.environ["CUDA_VISIBLE_DEVICES"] = ''
COLOR = 'white'
plt.rcParams['figure.facecolor'] = '#035a85'
plt.rcParams['axes.facecolor'] = COLOR
plt.rcParams['savefig.facecolor'] = '#035a85'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR


def plot_nn(score, highlight):
    fig, ax = plt.subplots(num="1")
    ax.plot(score, label='Score', color='white')
    ax.axvline(highlight[0], color='#f6d033', label='Start of thumbnail')
    ax.axvline(highlight[1], color='#f6d033', label='End of thumbnail')
    ax.set_xlabel('Time (frames)')
    ax.set_ylabel('Score')
    ax.set_facecolor("#035a85")
    ax.axvspan(highlight[0], highlight[1], ymin=0, ymax=1, alpha=0.2, color='#f6d033')
    ax.set_title("Attention Score")
    return fig


def extract(fs, name=None, length=30, save_score=True, save_thumbnail=True, save_wav=True, st=None):
    for f in fs:
        with tf.Session() as sess:

            model = MusicHighlighter()
            sess.run(tf.global_variables_initializer())

            model.saver.restore(sess, "pop_music_highlighter" + os.path.sep + "model" + os.path.sep + "model")

            audio, spectrogram, duration, mel_plot, sr = audio_read(f)

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
            #if st is not None:
             #   st.write(n_chunk)

            if save_score:
                if not os.path.exists("output" + os.path.sep + "attention"):
                    os.mkdir("output" + os.path.sep + "attention")
                np.save('output' + os.path.sep + 'attention' + os.path.sep + '{}_score.npy'.format(name), attn_score)

            # thumbnail

            attn_score = attn_score.cumsum()
            attn_score = np.append(attn_score[length], attn_score[length:] - attn_score[:-length])
            index = np.argmax(attn_score)
            highlight = [index, index + length]
            if st is not None:
                #st.text(highlight)
                st.pyplot(plot_nn(score, highlight))
            else:
                fig = plot_nn(score, highlight)
                fig.show()

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
