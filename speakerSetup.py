import platform
#import traceback
#import sys

import pyttsx3


# pylint: disable=invalid-name
# pylint: disable=broad-exception-caught
# pylint: disable=too-few-public-methods

### disable false positives of not callable
# pylint: disable=E1102

# pylint: disable=E0401
### E0401 as pylint (GitHub/Linux) cannot install Windows package


class SpeakerInitializeError(Exception):
    """Represent speaker initialization errors"""

class SpeakerStatus:
    """initialize speaker and other settings."""
    debugSwitchOffSpeaker = False
    engine = None
    speak = None
    #
    default_voice_id = None
    current_lang = "German"
    voices_dict = {}
    #
    @staticmethod
    def is_windows_platform() -> bool:
        """True if system is Windows"""
        return platform.system() == 'Windows'

    @classmethod
    def initializePyTTSSpeaker(cls) -> bool:
        """Tries to initialize py3-tts speaker"""
        try:
            cls.engine = pyttsx3.init()
            #voices = cls.engine.getProperty('voices')
            #cls.engine.setProperty('voice', voices[0].id)
            voices = cls.prepareLanguages()
            cls.default_voice_id = voices[0].id
            cls.engine.setProperty('voice', cls.default_voice_id)
        except (RuntimeError, Exception):
            print("Sorry, pyttsx3 is not working.")
            # goal: if debug mode tell me, else keep quiet
            #traceback.print_exc(limit=2, file=sys.stdout)
            cls.engine = None
            return False
        return True

    @classmethod
    def initializeSpVoiceSpeaker(cls) -> bool:
        """Tries to initialize Windows speaker"""
        if not cls.is_windows_platform():
            raise SpeakerInitializeError("Cannot initialize SpVoice. Windows platform required")
        from win32com.client import Dispatch
        try:
            cls.speak = Dispatch("SAPI.SpVoice").Speak
        except Exception as exc:
            #traceback.print_exc(limit=2, file=sys.stdout)
            raise SpeakerInitializeError("Cannot initialize SpVoice") from exc
        return True

    @classmethod
    def initializeSpeaker(cls) -> bool:
        """setup of speaking functionality"""
        try:
            # second member will be evaluated only if first will fail
            return cls.initializePyTTSSpeaker() \
             or  cls.initializeSpVoiceSpeaker()
        except SpeakerInitializeError:
            print("No speaker has been configured.")
            cls.debugSwitchOffSpeaker = True
            return False

    #def __init__(self):
    #    SpeakerStatus.initializeSpeaker()

    @classmethod
    def talk(cls, text):
        """lets system's voice speak the text"""
        try:
            if cls.engine:
                #and not SpeakerStatus.debugSwitchOffSpeaker:
                if not cls.current_lang in {"German", "system_default"} :
                    cls.engine.setProperty('voice', cls.default_voice_id)
                cls.engine.say(text)
                cls.engine.runAndWait()
            elif cls.speak:
                cls.speak(text)
        except KeyboardInterrupt:
            if cls.engine:
                cls.engine.stop()
            else:
                pass

    @classmethod
    def talkInLanguage(cls, text, lang="system_default", rate = 200):
        if not cls.engine:
            if cls.speak:
                cls.speak(text)
                return
        c = cls.voices_dict.get(lang)
        if c:
            cls.current_lang = lang
            cls.engine.setProperty('voice', c)
            cls.engine.setProperty('rate', rate)
        else:
            cls.engine.setProperty('voice', cls.default_voice_id)
        cls.engine.say(text)
        cls.engine.runAndWait()

    @classmethod
    def speakFaster(cls):
        """increase words per minute rate"""
        rate = cls.engine.getProperty('rate')
        cls.engine.setProperty('rate', rate+50)
        print("Geschwindigkeit auf "+str(cls.engine.getProperty('rate')))

    @classmethod
    def speakSlower(cls):
        """increase words per minute rate"""
        rate = cls.engine.getProperty('rate')
        print(cls.engine.getProperty('rate'))
        print(rate)
        cls.engine.setProperty('rate', rate-50)
        print("Geschwindigkeit auf "+str(cls.engine.getProperty('rate')))

    @classmethod
    def prepareLanguages(cls):
        """Gather voices and languages to be able to switch languages"""
        voices = cls.engine.getProperty('voices')
        foundvoices = 0
        for voice in voices:
            if foundvoices == 3:
                break
            if not "German" in cls.voices_dict and voice.name.__contains__("German"):
                cls.voices_dict["German"] = voice.id
                foundvoices += 1
            if not "French" in cls.voices_dict and voice.name.__contains__("French"):
                cls.voices_dict["French"] = voice.id
                foundvoices += 1
            elif not "English" in cls.voices_dict and voice.name.__contains__("English"):
                cls.voices_dict["English"] = voice.id
                foundvoices += 1
        return voices

# pylint: disable=invalid-name
# pylint: enable=broad-exception-caught
# pylint: enable=too-few-public-methods
# pylint: enable=E1102
# pylint: enable=E0401
### no issue on a real system though
