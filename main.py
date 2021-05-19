import glob
import myller.extractor as me
import pop_music_highlighter.extractor as pmhe
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extractor test code')
    parser.add_argument("-filename", help="Song path location", default="data/Pink Floyd - The Great Gig in The Sky.wav")
    parser.add_argument("-me", help="Run myller", default='y')
    parser.add_argument("-pmhe", help="Run pop music highlighter", default='y')
    parser.add_argument("-length", help="Length of audio thumbnail", default=15, type=int)
    args = parser.parse_args()

    fs = glob.glob(args.filename)
    print(fs)

    if args.me:
        me.extract(fs, length=args.length, save_SSM=True, save_thumbnail=True, save_wav=True, save_SP=True, st=None)

    if args.pmhe:
        pmhe.extract(fs, length=args.length, save_score=True, save_thumbnail=True, save_wav=True)
