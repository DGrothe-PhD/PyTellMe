import datetime
import locale
import re

import sys
import platform
import traceback

import speech_recognition as sr
import pyttsx3
import pywhatkit

import wikipedia

from videoText import RbbWeather
#from videoText import RbbText
from videoText import ARDText

## We'll set German wikipedia as default.
wikipedia.set_lang("de")
locale.setlocale(locale.LC_TIME, "de_DE")

listener = sr.Recognizer()

# pylint: disable=C0103
# pylint: disable=W0718
# pylint: disable=R0903
# pylint: disable=E0211
# pylint: disable=E1102

# pylint: disable=E0401
### E0401 as pylint (GitHub/Linux) cannot install Windows package

def is_windows_platform() -> bool:
    return platform.system() == 'Windows'

class SpeakerInitializeError(Exception):
    """ Represent speaker initialization errors"""


class JarvisStatus:
    """initialize speaker and other settings"""
    debugSwitchOffSpeaker = False
    engine = None
    isRunning = True
    engineUsed = ""
    countErrors = 0
    wikifound = []
    speak = None

    @staticmethod
    def initializePyTTSSpeaker() -> bool:
        try:
            JarvisStatus.engine = pyttsx3.init()
            voices = JarvisStatus.engine.getProperty('voices')
            JarvisStatus.engine.setProperty('voice', voices[0].id)
        except (RuntimeError, Exception):
            print("Sorry, pyttsx3 is not working.")
            # goal: if debug mode tell me, else keep quiet
            traceback.print_exc(limit=2, file=sys.stdout)
            JarvisStatus.engine = None
            return False
        return True

    @staticmethod
    def initializeSpVoiceSpeaker() -> bool:
        if not is_windows_platform():
            raise SpeakerInitializeError("Cannot initialize SpVoice. Windows platform required")
        from win32com.client import Dispatch
        try:
            JarvisStatus.speak = Dispatch("SAPI.SpVoice").Speak
        except Exception:
            traceback.print_exc(limit=2, file=sys.stdout)
            raise SpeakerInitializeError("Cannot initialize SpVoice")
        return True

    @staticmethod
    def initializeSpeaker() -> bool:
        """setup of speaking functionality"""
        try:
            # second member will be evaluated only if first will fail
            return JarvisStatus.initializePyTTSSpeaker() or JarvisStatus.initializeSpVoiceSpeaker()
        except SpeakerInitializeError:
            JarvisStatus.debugSwitchOffSpeaker = True
            return False


JarvisStatus.initializeSpeaker()

def talk(text):
    """lets system's voice speak the text"""
    if JarvisStatus.engine:
        #and not JarvisStatus.debugSwitchOffSpeaker:
        JarvisStatus.engine.say(text)
        JarvisStatus.engine.runAndWait()
    elif JarvisStatus.speak:
        JarvisStatus.speak(text)
    ''' legacy code
    if JarvisStatus.debugSwitchOffSpeaker and JarvisStatus.speak:
        JarvisStatus.speak(text)
    elif not JarvisStatus.debugSwitchOffSpeaker:
        JarvisStatus.engine.say(text)
        JarvisStatus.engine.runAndWait()
    '''

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
        talk("Beim Einlesen des Sprachkommandos ist etwas schiefgelaufen.")
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
        JarvisStatus.engineUsed = "wikipedia"
        JarvisStatus.wikifound = wikipedia.search(text, results=3)
        if len(JarvisStatus.wikifound) > 1 and not show_all:
            answersFound = " oder ".join(JarvisStatus.wikifound)
            print(answersFound)
            talk(answersFound)
        else:
            info = wikipedia.summary(text, sentences = 2)
            print(info)
            talk(info)

def runJarvis():
    """main function"""
    command = takeCommand()
    print(command)
    #
    if 'spiel' in command:
        song = command.replace('spiel', '')
        JarvisStatus.engineUsed = "YouTube"
        talk('Es läuft ' + song)
        pywhatkit.playonyt(song)
    #
    elif 'zeit' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        print(time)
        talk(f"Es ist jetzt {time} Uhr.")
    #
    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        utilities.searchWikipedia(person)
    #
    elif 'mdax' in command:
        textMdax = ARDText(716)
        textResult = makeReadable(textMdax.content)
        print(textResult)
        talk(textResult)
        textMdax.extractAndPreparePage(716, 2)
        textResult = makeReadable(textMdax.content)
        print(textResult)
        talk(textResult)
    #elif 'was' in command:
    #    person = command.replace('was', '')
    #    utilities.searchWikipedia(person)
    #
    #elif 'wann' in command:
    #    person = command.replace('wann', '')
    #    utilities.searchWikipedia(person)
    #
    #elif 'wo' in command:
    #    person = command.replace('wo', '')
    #    utilities.searchWikipedia(person)
    #
    elif 'zeige alle' in command:
        if len(JarvisStatus.wikifound) < 1:
            talk("Keine Einträge")
            return
        for person in JarvisStatus.wikifound:
            utilities.searchWikipedia(person, True)
        JarvisStatus.wikifound.clear()
    #
    elif 'datum' in command:
        date = datetime.datetime.now().strftime('%W. KW, %A den %d. %B %Y')
        print(date)
        talk(date)
    #
    elif 'wetter' in command:
        textHeute = RbbWeather()
        print(textHeute.content)
        talk(textHeute.content)
    #
    elif 'stop listening' in command or 'stop listing' in command \
    or (command.startswith('stop') and len(command)< 50):
        talk('Bye, until next time.')
        JarvisStatus.isRunning = False
    else:
        talk('Entschuldigung, ich habe nicht verstanden.')

while JarvisStatus.isRunning:
    print("...")# without it, it didn't stop listening
    try:
        runJarvis()
    except KeyboardInterrupt:
        print("Tschüs.")
        talk("Tschüs, bis zum nächsten Mal.")
        break
    except Exception as e:
        talk(f"Entschuldigung, {JarvisStatus.engineUsed} konnte es nicht finden.")
        print(e)
# pylint: enable=C0103
# pylint: enable=W0718
# pylint: enable=R0903
# pylint: enable=E0211
# pylint: enable=E1102
# pylint: enable=E0401
### no issue on a real system though
