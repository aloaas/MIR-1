import glob
import myller.extractor as me
import pop_music_highlighter.extractor as pmhe

if __name__ == '__main__':
    fs = glob.glob("data/Pink Floyd - The Great Gig in The Sky.wav")  # glob.glob("data/Pink Floyd - The Great Gig in The Sky.wav") #+
    print(fs)
    me.extract(fs, length=15, save_SSM=True, save_thumbnail=True, save_wav=True, save_SP=True, st=None)
    pmhe.extract(fs, length=10, save_score=True, save_thumbnail=True, save_wav=True)
