import datetime
import locale
import re

import speech_recognition as sr
import pyttsx3
import pywhatkit

import wikipedia

#import traceback

from videoText import RbbWeather
#from videoText import RbbText
from videoText import ARDText

## We'll set German wikipedia as default.
wikipedia.set_lang("de")
locale.setlocale(locale.LC_TIME, "de_DE")

listener = sr.Recognizer()
debugSwitchOffSpeaker = False

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
except Exception as e:
    print("Sorry, pyttsx3 is not working.")
    print(e)
    debugSwitchOffSpeaker = True

class JarvisStatus:
    isRunning = True
    engineUsed = ""
    wikifound = []


def talk(text):
    if debugSwitchOffSpeaker:
        return
    """lets system's voice speak the text"""
    engine.say(text)
    engine.runAndWait()

def makeReadable(text):
    return re.sub(r'^(\d+)\.(\d{2}\s)', r'\1,\2', text, flags=re.MULTILINE)

def takeCommand():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language="de-DE")
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)
    except:
        pass
    return command

# Wikipedia
class utilities:
    """basic functionality """
    @staticmethod
    def searchWikipedia(text, showAll = False):
        JarvisStatus.engineUsed = "wikipedia"
        JarvisStatus.wikifound = wikipedia.search(text, results=3)
        if len(JarvisStatus.wikifound) > 1 and not showAll:
            answersFound = " oder ".join(JarvisStatus.wikifound)
            print(answersFound)
            talk(answersFound)
        else:
            info = wikipedia.summary(text, sentences = 2)
            print(info)
            talk(info)

def runJarvis():
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
    elif 'stop listening' in command or 'stop listing' in command:
        talk('Bye, until next time.')
        JarvisStatus.isRunning = False
    else:
        talk('Entschuldigung, ich habe nicht verstanden.')

while JarvisStatus.isRunning:
    print("...")# without it, it didn't stop listening
    try:
        runJarvis()
    except Exception as e:
        talk(f"Entschuldigung, {JarvisStatus.engineUsed} konnte es nicht finden.")
        print(e)
