import sys
import platform
import traceback

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
    
    @staticmethod
    def is_windows_platform() -> bool:
        """True if system is Windows"""
        return platform.system() == 'Windows'

    @staticmethod
    def initializePyTTSSpeaker() -> bool:
        """Tries to initialize py3-tts speaker"""
        try:
            SpeakerStatus.engine = pyttsx3.init()
            voices = SpeakerStatus.engine.getProperty('voices')
            SpeakerStatus.engine.setProperty('voice', voices[0].id)
        except (RuntimeError, Exception):
            print("Sorry, pyttsx3 is not working.")
            # goal: if debug mode tell me, else keep quiet
            #traceback.print_exc(limit=2, file=sys.stdout)
            SpeakerStatus.engine = None
            return False
        return True

    @staticmethod
    def initializeSpVoiceSpeaker() -> bool:
        """Tries to initialize Windows speaker"""
        if not SpeakerStatus.is_windows_platform():
            raise SpeakerInitializeError("Cannot initialize SpVoice. Windows platform required")
        from win32com.client import Dispatch
        try:
            SpeakerStatus.speak = Dispatch("SAPI.SpVoice").Speak
        except Exception as exc:
            #traceback.print_exc(limit=2, file=sys.stdout)
            raise SpeakerInitializeError("Cannot initialize SpVoice") from exc
        return True

    @staticmethod
    def initializeSpeaker() -> bool:
        """setup of speaking functionality"""
        try:
            # second member will be evaluated only if first will fail
            return SpeakerStatus.initializePyTTSSpeaker() or SpeakerStatus.initializeSpVoiceSpeaker()
        except SpeakerInitializeError:
            print("No speaker has been configured.")
            SpeakerStatus.debugSwitchOffSpeaker = True
            return False

    def __init__(self):
        SpeakerStatus.initializeSpeaker()

    def talk(self, text):
        """lets system's voice speak the text"""
        if SpeakerStatus.engine:
            #and not SpeakerStatus.debugSwitchOffSpeaker:
            SpeakerStatus.engine.say(text)
            SpeakerStatus.engine.runAndWait()
        elif SpeakerStatus.speak:
            SpeakerStatus.speak(text)



# pylint: disable=invalid-name
# pylint: enable=broad-exception-caught
# pylint: enable=too-few-public-methods
# pylint: enable=E1102
# pylint: enable=E0401
### no issue on a real system though
