import os
import time
from collections import namedtuple
import altair as alt
import math
import pop_music_highlighter.extractor as pmhe

import numpy as np
import pandas as pd
import streamlit as st

"""
# Thumbnail.me
Upload a .wav or .mp3 file below and get the respective audio thumbnail.
"""





uploaded_file = st.file_uploader("Choose a file", type=['mp3', 'wav'])
if uploaded_file is not None:
    st.audio(uploaded_file)
    with open(os.path.join("data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    path = 'output' + os.path.sep + 'attention'+ os.path.sep + '{}_audio.wav'.format(uploaded_file.name)
    with st.spinner("Processing..."):
        pmhe.extract(uploaded_file, length=10, save_score=True, save_thumbnail=True, save_wav=True)
    st.success("Success!")

    if os.path.isfile(path):
        st.audio(path)

