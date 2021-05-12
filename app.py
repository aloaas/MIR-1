
import os
import time
from collections import namedtuple
import altair as alt
import math
#import pop_music_highlighter.extractor as pmhe
import myller.extractor as me

import numpy as np
import pandas as pd
import streamlit as st

"""
# Thumbnail.me
Upload a .wav or .mp3 file below and get the respective audio thumbnail and self similarity matrix.
"""
uploaded_file = st.file_uploader("Choose a file", type=['mp3', 'wav'])
if uploaded_file is not None:
    st.audio(uploaded_file)
    st.write(uploaded_file)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        #path = 'output' + os.path.sep + 'attention' + os.path.sep + '{}_audio.wav'.format(uploaded_file.name)

#   with st.spinner("Processing..."):
#      pmhe.extract(uploaded_file, length=15, save_score=True, save_thumbnail=True, save_wav=True)
# st.success("Success!")

#if os.path.isfile(path):
 #   st.audio(path)


    path = 'output' + os.path.sep + 'repetition' + os.path.sep + '{}_SSM_norm.npy'.format(uploaded_file.name)
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write(file_details)
    st.write(file_path)

    # uploaded_file = os.path.join("tempDir", uploaded_file.name)
    # with open(uploaded_file, "wb") as f:
    #     f.write(uploaded_file.getbuffer())
    # st.success("Saved File")

    with st.spinner("Processing once more..."):
        me.extract(file_path, length=15)
    st.success("Success Again!")

    if os.path.isfile(path):
        st.audio(path)

