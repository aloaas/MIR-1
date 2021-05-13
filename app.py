
import os
import time
from collections import namedtuple
import altair as alt
import math
import pop_music_highlighter.extractor as pmhe
import myller.extractor as me

import numpy as np
import pandas as pd
import streamlit as st

"""
# Thumbnail.me
Upload a .wav or .mp3 file below and get the respective audio thumbnail and self similarity matrix.
"""
analyte = st.radio(
     "Myller, Neural or  Both?",     ('Myller', 'Neural', 'Both'))
length = st.slider('How long thumbnail do you like?', 1, 31)

uploaded_file = st.file_uploader("Choose a file", type=['mp3', 'wav'])
if uploaded_file is not None:
    st.audio(uploaded_file)
    uploaded_file_path = os.path.join("data", uploaded_file.name)
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if analyte == "Neural" or analyte == "Both":
        path_neural_wav = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_audio.wav'.format(uploaded_file.name)
        with st.spinner("Processing..."):
            pmhe.extract([uploaded_file], length=length, save_score=True, save_thumbnail=True, save_wav=True)
            st.success("Success!")

        if os.path.isfile(path_neural_wav):
            st.audio(path_neural_wav)

    if analyte == "Myller" or analyte == "Both":

        path_ssm_norm = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SSM_norm.npy'.format(uploaded_file.name)
        path_myller_wav = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_audio.wav'.format(uploaded_file.name)
        path_scape_plot = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SP.npy'.format(uploaded_file.name)
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)
        st.write(uploaded_file_path)
        st.write(path_ssm_norm)
        with st.spinner("Processing once more..."):
            me.extract([uploaded_file_path], length=length, st=st)
        st.success("Success Again!")

        st.write(path_ssm_norm)
        if os.path.isfile(path_myller_wav):
            st.audio(path_myller_wav)

