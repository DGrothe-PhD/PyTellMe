import datetime
import locale
import re

import speech_recognition as sr
import pyttsx3
import pywhatkit

import wikipedia

#import traceback

from videoText import rbbWeather
from videoText import rbbText
from videoText import ARDText

## We'll set German wikipedia as default.
wikipedia.set_lang("de")
locale.setlocale(locale.LC_TIME, "de_DE")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

class status:
    isRunning = True
    engineUsed = ""
    wikifound = []


def talk(text):
    engine.say(text)
    engine.runAndWait()

def MakeReadable(text):
    return re.sub(r'^(\d+)\.(\d{2}\s)', r'\1,\2', text, flags=re.MULTILINE)

def take_command():
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
    @staticmethod
    def SearchWikipedia(text, showAll = False):
        status.engineUsed = "wikipedia"
        status.wikifound = wikipedia.search(text, results=3)
        if len(status.wikifound) > 1 and not showAll:
            answers_found = " oder ".join(status.wikifound)
            print(answers_found)
            talk(answers_found)
        else:
            info = wikipedia.summary(text, sentences = 2)
            print(info)
            talk(info)

def run_jarvis():
    command = take_command()
    print(command)

    if 'spiel' in command:
        song = command.replace('spiel', '')
        status.engineUsed = "YouTube"
        talk('Es läuft ' + song)
        pywhatkit.playonyt(song)

    elif 'zeit' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        print(time)
        talk(f"Es ist jetzt {time} Uhr.")

    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        utilities.SearchWikipedia(person)

    elif 'mdax' in command:
        TextMdax = ARDText(716)
        TextResult = MakeReadable(TextMdax.content)
        print(TextResult)
        talk(TextResult)
        TextMdax.extractAndPreparePage(716, 2)
        TextResult = MakeReadable(TextMdax.content)
        print(TextResult)
        talk(TextResult)
    #elif 'was' in command:
    #    person = command.replace('was', '')
    #    utilities.SearchWikipedia(person)
    #
    #elif 'wann' in command:
    #    person = command.replace('wann', '')
    #    utilities.SearchWikipedia(person)
    #
    #elif 'wo' in command:
    #    person = command.replace('wo', '')
    #    utilities.SearchWikipedia(person)
    
    elif 'zeige alle' in command:
        for person in status.wikifound:
            utilities.SearchWikipedia(person, True)
            status.wikifound.clear()
        else:
            talk("Keine Einträge")
    
    elif 'datum' in command:
        date = datetime.datetime.now().strftime('%W. KW, %A den %d. %B %Y')
        print(date)
        talk(date)
    
    elif 'wetter' in command:
        print("Wetter: ")
        textHeute = rbbWeather(162, False)
        print(textHeute.content)
        talk(textHeute.content)
        talk("Weiter zu den Aussichten mit beliebiger Taste.")
        input("Weiter zu den Aussichten mit beliebiger Taste: ")
        print("Aussichten: ")
        talk("Aussichten: ")
        textAussichten = rbbWeather(163, True)
        print(textAussichten.content)
        talk(textAussichten.content)

    elif 'stop listening'.__eq__(command):
        talk('Bye, until next time.')
        status.isRunning = False
    else:
        talk('Entschuldigung, ich habe nicht verstanden.')

while status.isRunning:
    print("...")# without it, it didn't stop listening
    try:
        run_jarvis()
    except Exception as e:
        talk(f"Entschuldigung, {status.engineUsed} konnte es nicht finden.") 
        print(e)
