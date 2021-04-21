import librosa
import sys
from argparse import ArgumentParser

def getLength(filename):
    # output track duration
    return librosa.get_duration(filename=filename)

if __name__ == "__main__":
    # setup script args
    argParser = ArgumentParser(description="Get sound tracks duration in seconds")
    argParser.add_argument("file", metavar="FILE", help="Sound track", action="store")
    options = vars(argParser.parse_args())

    length = str(getLength(options['file']))

    sys.stdout.write(length)