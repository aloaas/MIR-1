
import os
import time
from collections import namedtuple
import altair as alt
import math
import pop_music_highlighter.extractor as pmhe
import myller.extractor as me

import pandas as pd
import streamlit as st
import numpy as np
from matplotlib import pyplot as plt

"""
# Thumbnail.me
Upload a .wav or .mp3 file below and get the respective audio thumbnail and self similarity matrix.
"""
analyte = st.radio(
     "Pick one..",     ('Myller', 'Neural', 'Both'))
if analyte is not None:
    st.write(analyte)
    length = st.slider('How long thumbnail do you like?', 1, 31)

if length is not None:
    st.write(length)

    uploaded_file = st.file_uploader("Choose a file", type=['mp3', 'wav'])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        st.audio(uploaded_file)
        uploaded_file_path = os.path.join("data", uploaded_file.name)

        name = os.path.split(uploaded_file.name)[-1][:-4]
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if analyte is not None and analyte == "Neural" or analyte == "Both":
            path_neural_wav = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_audio.wav'.format(uploaded_file.name)
            with st.spinner("Processing..."):
                pmhe.extract([uploaded_file], length=length, save_score=True, save_thumbnail=True, save_wav=True)
                st.success("Success!")

            if os.path.isfile(path_neural_wav):
                st.audio(path_neural_wav)

        if analyte is not None and analyte == "Myller" or analyte == "Both":

            path_ssm_norm = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SSM_norm.npy'.format(name)
            path_myller_wav = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_audio.wav'.format(name)
            path_scape_plot = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SP.npy'.format(name)
            st.write(uploaded_file_path)
            st.write(path_ssm_norm)
            with st.spinner("Processing once more..."):
                me.extract([uploaded_file_path], length=length, st=st)
            st.success("Success Again!")

            st.write(path_ssm_norm)
            st.write(path_myller_wav)

            if os.path.isfile(path_myller_wav):
                st.audio(path_myller_wav)





def visualize_scape_plot(SP, Fs=1, ax=None, figsize=(4, 3), title='',
                         xlabel='Center (seconds)', ylabel='Length (seconds)'):
    """Visualize scape plot

    Notebook: C4/C4S3_ScapePlot.ipynb

    Args:
        SP: Scape plot data (encodes as start-duration matrix)
        Fs: Sampling rate (Default value = 1)
        ax: Used axes (Default value = None)
        figsize: Figure size (Default value = (4, 3))
        title: Title of figure (Default value = '')
        xlabel: Label for x-axis (Default value = 'Center (seconds)')
        ylabel: Label for y-axis (Default value = 'Length (seconds)')

    Returns:
        fig: Handle for figure
        ax: Handle for axes
        im: Handle for imshow
    """
    fig = None
    if(ax is None):
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
    N = SP.shape[0]
    SP_vis = np.zeros((N, N))
    for length_minus_one in range(N):
        for start in range(N-length_minus_one):
            center = start + length_minus_one//2
            SP_vis[length_minus_one, center] = SP[length_minus_one, start]

    extent = np.array([-0.5, (N-1)+0.5, -0.5, (N-1)+0.5]) / Fs
    im = plt.imshow(SP_vis, cmap='hot_r', aspect='auto', origin='lower', extent=extent)
    x = np.asarray(range(N))
    x_half_lower = x/2
    x_half_upper = x/2 + N/2 - 1/2
    plt.plot(x_half_lower/Fs, x/Fs, '-', linewidth=3, color='black')
    plt.plot(x_half_upper/Fs, np.flip(x, axis=0)/Fs, '-', linewidth=3, color='black')
    plt.plot(x/Fs, np.zeros(N)/Fs, '-', linewidth=3, color='black')
    plt.xlim([0, (N-1) / Fs])
    plt.ylim([0, (N-1) / Fs])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.colorbar(im, ax=ax)
    return fig, ax, im


