import sys
from speakerSetup import SpeakerStatus as speaker
from videoText import RbbWeather

# pylint: disable=W0718

speaker.initializeSpeaker()

def printAndSay(text):
    """first print, then say (if speaker/module is working)"""
    print(text)
    speaker.talk(text)

# Tonight and tomorrow
try:
    textHeute = RbbWeather()
    printAndSay(textHeute.content)
except KeyboardInterrupt:
    print("Auf Wiedersehen!")
    sys.exit()