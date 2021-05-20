# AudioThumbnail Project

This is a project for the music information retrieval (LTAT.02.015) course in Tartu University. The goal of this project is to implement audio thumbnailing methodologies and from that develop a web app. 

The web application is available at: https://share.streamlit.io/aloaas/mir-1/main/app.py 

Requirements to run manually ```main.py``` or ```streamlit run app.py```.
- for ```main.py``` songs can called out with ```python main.py -filename "****"```
- seperate venv python 3.7
- ```pip install -r requirements.txt```

# Description / Report 
## Introduction

Audio thumbnailing is a process of determining the most representative continous segment that represents the whole song. It can be thought of as a 'preview' of the song [1]. Audio thumbnails are an important piece in MIR by providing a first impression to a listener to either continue listening or choose another song. We explore two ways of audio thumbnailing. Firstly, a repetition-based approach [1] [2] [3] using self-similarity matrices and scape plots. Secondly, a neural network that finds the segment of a song that most contributes to classify emotion [4] [5]. With these methodologies in mind we implemented a Streamlit app that showcases these methods. 

## Repetition-based approach (```myller```)

Chorus or main theme of a song are very good canditates thumbnailing, due to being repeated multiple times in a song. But repeating sections can differ from one another by dynamics, instruments and/or tempo, thus the applied methodology has to be robust enough to work with these differences. The repetition-based approach uses chroma features of a song, from which self-similarity matrices (SSM) can be derived from. From SSM's one can use time-warping techniques (e.g dynamic time warping) in order to account for the temporal variabilities. From an SSM we can calculate for each segment a fitness value, the fitness value explain/expresses "how well" a segment explains the whole song. The segment with the highest fitness value is considered to be a thumbnail [1]. We amend the process by not finding the highest score, but a highest score with a predefined segment length and downsample more the longer songs. 

## Attention-based approach (```pop_music_highlighter```)

As mentioned before chorus is a vey good candidate for thumbnailing a song. But this time it's not because it is repeated mutliple times in a song, but because most often from the chorus one can get the main idea of the song, or it's the most memorable part of a song. Thus, being able do detect a chorus from a song may prove useful in an audio thumbnailing task. In order to facilitate this Huang <i> et al. </i> 2017 [5] proposed to use a emotion classifier to which one introduces an attention layer that estimates the importance of each 3 second segment of a song in predicting the emotion of a song. This work was improved in 2018 [4], which we implemented. In order to get a predefined length segment thumbnail a window of with a predefined length size is run across the 3 second segments. 

## Web app (```app```)

Both methodologies were implemented in a web app which's flow is the following:

- Streamlit:
  - Upload any song (any file format);
  - after upload, the song can be played;
  - choose one or both models;
  - choose a predefined length;
  - serverside will process the users song based on his choices.
- Output:
  - one or two thumbnails of predefined length;
  - repetition-based: Visualizations of SSM with optimal paths and segments;
  - repetition-based: Visualizations of the fitness scape plot, with points at the optimal paths and segments;
  - attention-based: Visualization of attention score with the segment highlighted.


## Conclusions 

The repetition-based approach in a subjective manner is the most visually pleasing. But at the same time it is the most resource intensive implementation. One option for optimization for the future, because we are looking for predefined length segments, would be to not calculate the scape plot and only look for predefined-length segments. Furthermore, due to computational limitations and to speed up processing in our web app, we downsample songs to a feature rate of 2Hz and every 4 minutes of song length divide the sampling rate by 2. Overall the implementation can detect repetitive parts of a song, but has trouble finding best segments if a song has no chorus or even words. Luckily due to only looking for predefined length segments this is a non-issue for us. Secondly, the attention-based approach is a lot quicker and constructs thumbnails that have more emotion in them. In the end both implementations get us satisfactory results, work and the web app that uses those implementation works to a satisfactory level. 

# References 

[1]: M. Muller, "Fundamentals of Music Processing", 2nd ed. [S.I.]: Springer Nature, 2011 

[2]: FMP Notebooks: Educational Material for Teaching and Learning Fundamentals of Music Processing In Proceedings of the International Conference on Music Information Retrieval (ISMIR), 2019. 

[3]: N. Jjang and M. Muller, "Towards efficient audio thumbnailing", 2014 IEEE international Conference on Acoustics, Speech and Signal Processing (ICASSP), 2014. Available: 10.1109/icassp.2014.6854593

[4]: Y. Huang, S. Chou and Y. Yang, "Pop Music Highlighter: Marking the Emotion Keypoints", Transactions of the International Society for Music Information Retrieval, vol 1, no. 1, pp. 66-76, 2018. Available: 10.5334/tismir.14

[5] Y. Huang, S. Chou and Y.Yang, "Music Thumbnailing Via Neural Attention Modeling of Music Emotion", Asia-Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC), pp. 347-350, 2017

# Notes

- https://www.audiolabs-erlangen.de/resources/MIR/FMP/C0/C0.html
- https://github.com/remyhuang/pop-music-highlighter/
