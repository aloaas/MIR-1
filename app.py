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

COLOR = 'white'
plt.rcParams['figure.facecolor'] = '#035a85'
plt.rcParams['axes.facecolor'] = COLOR
plt.rcParams['savefig.facecolor'] = '#035a85'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR



length = None
analyte = st.radio(
    "Pick one..", ('None', 'Repetition', 'Attention', 'Both'))
if analyte != "None":
    length = st.slider('How long a thumbnail would you like?', 1, 31, value=0)

if length in range(1, 31):

    uploaded_file = st.file_uploader("Choose a file", type=['mp3', 'wav'])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.audio(uploaded_file)
        uploaded_file_path = os.path.join("data", uploaded_file.name)

        name = os.path.split(uploaded_file.name)[-1][:-4]
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if analyte is not None and analyte == "Repetition" or analyte == "Both":

            path_ssm_norm = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SSM_norm.npy'.format(name)
            path_myller_wav = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_audio.wav'.format(name)
            path_scape_plot = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SP.npy'.format(name)

            with st.spinner("Processing repetition..."):
                me.extract([uploaded_file_path], name=name, length=length, st=st)
            st.success("Repetition Success!")

            if os.path.isfile(path_myller_wav):
                st.audio(path_myller_wav)

            if os.path.isfile(path_myller_wav):
                os.remove(path_myller_wav)

        if analyte is not None and analyte == "Attention" or analyte == "Both":
            score = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_score.npy'.format(name)
            highlight = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_highlight.npy'.format(name)
            path_neural_wav = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_audio.wav'.format(name)
            #print(highlight)
            #print(score)
            with st.spinner("Processing attention..."):
                pmhe.extract([uploaded_file.name], name=name, length=length, save_score=True, save_thumbnail=True,
                             save_wav=True, st=st)
                st.success("Attention Success!")

            if os.path.isfile(path_neural_wav):
                st.audio(path_neural_wav)

            if os.path.isfile(path_neural_wav):
                os.remove(path_neural_wav)

        if os.path.isfile(uploaded_file_path):
            os.remove(uploaded_file_path)
