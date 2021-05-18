# AudioThumbnail Project

This is a project for the music information retrieval (LTAT.02.015) course in Tartu University. The goal of this project is to implement audio thumbnailing methodologies and from that develop a web app. 

The web application is available at: https://share.streamlit.io/aloaas/mir-1/main/app.py 

Requirements to run ```main.py``` or ```streamlit run app.py```.
- seperate venv
- python 3.7
- ```pip install -r requirements.txt```

# Description / Report 
## Introduction

Audio thumbnailing is a process of determining the most representative continous segment that represents the whole song, can be thought of as a 'preview' of the song [1]. Audio thumbnails are an important piece in MIR by providing a first impression to a listener to either continue listening or choose another song. We explore two ways of audio thumbnailing. Firstly, a repetition-based approach [1] [2] [3] using self-similarity matrices and scape plots. Secondly a neural network that finds the segment of a song that most contributes to classify emotion [4]. We implement these models and from there we implemented a Streamlit app that showcases these methods. 

## Repetition-based approach (```myller```)

Chorus or main theme of a song are very good canditates thumbnailing, due to being repeated multiple times in a song. But repeating sections can differ from one another by dynamics, instruments and/or tempo, thus the applied methodology has to be robust enough to work with these differences. The repetition-based approach uses chroma features of a song from which self-similarity matrices (SSM) can be derived from. From SSM's one can use time-warping techniques (e.g dynamic time warping) in order to account for the temporal variabilities. From an SSM we can calculate for each segment a fitness value, the fitness value explain/expresses "how well" a segment explains the whole song. The segment with the highest fitness value is considered to be a thumbnail [1]. We amend the process by not finding the highest score, but a highest score with a predefined length and we limited the search base to the first four minutes of a song due to computational limitations. 

## Attention-based approach (```pop_music_highlighter```)

As mentioned before chorus is a vey good candidate for thumbnailing a song. But this time it's not because it is repeated mutliple times in a song, but because most from the chorus most often on can get the main idea of the song, or it's the most memorable part of a song. Thus, being able do detect a chorus from a song may prove useful in an audio thumbnailing task. In order to facilitate this Huang <i> et al. </i> 2017 proposed to use a emotion classifier to which one introduces an attention layer that estimates the importance of each 3 second segment of a song in predicting the emotion of a song. This work was improved in 2018 [4], which we implemented. In order to get a predefined length segment thumbnail a window of with a predefined length size is run across the 3 second segments. 

## Web app (```app```)

- Streamlit app:
  - Upload any song (any file format).
  - After upload the song can be played.
  - Chooses one or both models
  - Choose a predefined length
  - Server will process the users song based on his choices
- Output:
  - One or two thumbnails of predefined length
  - Repetition-based: Visualizations of SSM with optimal paths and segments
  - Repetition-based: Visualizations of the fitness scape plot, with the top 5 segments as points.
  - Attention-based: Visualization of chroma features and attention score with the segment highlighted

# References 

[1]: M. Muller, "Fundamentals of Music Processing", 2nd ed. [S.I.]: Springer Nature, 2011 

[2]: FMP Notebooks: Educational Material for Teaching and Learning Fundamentals of Music Processing In Proceedings of the International Conference on Music Information Retrieval (ISMIR), 2019. 

[3]: N. Jjang and M. Muller, "Towards efficient audio thumbnailing", 2014 IEEE international Conference on Acoustics, Speech and Signal Processing (ICASSP), 2014. Available: 10.1109/icassp.2014.6854593

[4]: Y. Huang, S. Chou and Y. Yang, "Pop Music Highlighter: Marking the Emotion Keypoints", Transactions of the International Society for Music Information Retrieval, vol 1, no. 1, pp. 66-76, 2018. Available: 10.5334/tismir.14

[5] Y. Huang, S. Chou and Y.Yang, "Music Thumbnailing Via Neural Attention Modeling of Music Emotion", Asia-Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC), pp. 347-350, 2017

# Notes

- https://www.audiolabs-erlangen.de/resources/MIR/FMP/C0/C0.html
- https://github.com/remyhuang/pop-music-highlighter/
