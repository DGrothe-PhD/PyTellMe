import datetime
import locale
import re


import speech_recognition as sr
import pywhatkit

import wikipedia

from speakerSetup import SpeakerStatus
from videoText import RbbWeather
from videoText import ARDText

## We'll set German wikipedia as default.
wikipedia.set_lang("de")
locale.setlocale(locale.LC_TIME, "de_DE")

listener = sr.Recognizer()

# pylint: disable=invalid-name
# pylint: disable=broad-exception-caught
# pylint: disable=too-few-public-methods


class JarvisStatus:
    """initialize Jarvis settings"""
    isRunning = True
    searchingEngine = ""
    countErrors = 0
    wikifound = []


speaker = SpeakerStatus()


def makeReadable(text):
    """Replace for better speaker functionality:
     - Float written with comma to speak stock exchange prices 
       as numbers instead of hours and minutes
    """
    return re.sub(r'^(\d+)\.(\d{2}\s)', r'\1,\2', text, flags=re.MULTILINE)

def takeCommand():
    """listens to user talking and returns command"""
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source, phrase_time_limit=20)
            command = listener.recognize_google(voice, language="de-DE").lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
            return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Request error")
        return ""
    except sr.WaitTimeoutError:
        print("Zeit abgelaufen")
        return ""
    #except KeyboardInterrupt:
    #    print("Programmende")
    #    JarvisStatus.isRunning = False
    except Exception:
        # rarely happening, however needs test before removal
        speaker.talk("Beim Einlesen des Sprachkommandos ist etwas schiefgelaufen.")
        JarvisStatus.countErrors += 1
        if JarvisStatus.countErrors >= 3:
            JarvisStatus.isRunning = False
        raise

# Wikipedia
class utilities:
    """basic functionality """
    @staticmethod
    def searchWikipedia(text, show_all = False):
        """get the first few lines of Wikipedia article"""
        JarvisStatus.searchingEngine = "wikipedia"
        JarvisStatus.wikifound = wikipedia.search(text, results=3)
        if len(JarvisStatus.wikifound) > 1 and not show_all:
            answersFound = " oder ".join(JarvisStatus.wikifound)
            print(answersFound)
            speaker.talk(answersFound)
        else:
            info = wikipedia.summary(text, sentences = 2)
            print(info)
            speaker.talk(info)

def runJarvis():
    """main function"""
    command = takeCommand()
    print(command)
    #
    if 'spiel' in command:
        song = command.replace('spiel', '')
        JarvisStatus.searchingEngine = "YouTube"
        speaker.talk('Es läuft ' + song)
        pywhatkit.playonyt(song)
    #
    elif 'zeit' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        print(time)
        speaker.talk(f"Es ist jetzt {time} Uhr.")
    #
    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        utilities.searchWikipedia(person)
    #
    elif 'mdax' in command:
        textMdax = ARDText(716)
        textResult = makeReadable(textMdax.content)
        print(textResult)
        speaker.talk(textResult)
        textMdax.extractAndPreparePage(716, 2)
        textResult = makeReadable(textMdax.content)
        print(textResult)
        speaker.talk(textResult)
    #
    elif 'zeige alle' in command:
        if len(JarvisStatus.wikifound) < 1:
            speaker.talk("Keine Einträge")
            return
        for person in JarvisStatus.wikifound:
            utilities.searchWikipedia(person, True)
        JarvisStatus.wikifound.clear()
    #
    elif 'datum' in command:
        date = datetime.datetime.now().strftime('%W. KW, %A den %d. %B %Y')
        print(date)
        speaker.talk(date)
    #
    elif 'wetter' in command:
        textHeute = RbbWeather()
        print(textHeute.content)
        speaker.talk(textHeute.content)
    #
    elif 'stop listening' in command or 'stop listing' in command \
    or (command.startswith('stop') and len(command)< 50):
        speaker.talk('Bye, until next time.')
        JarvisStatus.isRunning = False
    else:
        speaker.talk('Entschuldigung, ich habe nicht verstanden.')

while JarvisStatus.isRunning:
    print("...")# without it, it didn't stop listening
    try:
        runJarvis()
    except KeyboardInterrupt:
        print("Tschüs.")
        speaker.talk("Tschüs, bis zum nächsten Mal.")
        break
    except Exception as e:
        speaker.talk(f"Entschuldigung, {JarvisStatus.searchingEngine} konnte es nicht finden.")
        print(e)

# pylint: disable=invalid-name
# pylint: enable=broad-exception-caught
# pylint: enable=too-few-public-methods
