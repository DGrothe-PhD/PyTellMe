#!/usr/bin/python3
# -*- coding: utf-8 -*-

from speakerSetup import SpeakerStatus as speaker
from videoText import RbbText, ARDText, BayernText, NDRText, VideoTextUtils

# pylint: disable=W0718

speaker.initializeSpeaker()

def printAndSay(text):
    """first print, then say (if speaker/module is working)"""
    print(text)
    speaker.talk(text)

class VTextStatus(VideoTextUtils):
    """settings and start"""
    welcome = "Hallo, ich bin dein Videotext-Assistent.\n" + \
     "Eingabe Seitenzahl (dreistellig)," + \
     "Beenden durch die Eingabe 'stop'."
    limitationNotice = "Auswahl: Das Erste, Bayern, RBB."
    isRunning = True
    hasrun = False
    page = 100
    sub = 1
    textNews = RbbText(page)
    aliasesErste = {"1", "das erste", "ard"}
    aliasesNdr = {"nord", "ndr"}
    aliasesBayern = {"6", "bayern", "br"}
    aliasesRbb = {"3", "rbb", "berlin"}
    #
    stationlist = { \
     "Das Erste" : aliasesErste,
     #"NDR" : aliasesNdr,
     "BR" : aliasesBayern,
     "rbb" : aliasesRbb
    }
    #
    @staticmethod
    def start():
        """let user choose TV station for teletext """
        printAndSay(VTextStatus.welcome)
        printAndSay(VTextStatus.limitationNotice)
        examples = []
        for station, aliases in VTextStatus.stationlist.items():
            examples.append(f"{station}:  {', '.join(aliases)}")
        tellAvailableStations = "\n".join(examples)
        userWhichVideotext = "Welchen Sendetext möchten Sie aufrufen?\n[  Beispiele:  ]\n"
        station = input(userWhichVideotext + tellAvailableStations + "\n...:")
        #
        if station.lower() in VTextStatus.aliasesErste:
            VTextStatus.textNews = ARDText(100)
        elif station.lower() in VTextStatus.aliasesNdr:
            VTextStatus.textNews = NDRText(100)
        elif station.lower() in VTextStatus.aliasesBayern:
            VTextStatus.textNews = BayernText(100)
        else:
            pass
    #
    mapping = [ ('Ã¼', 'ü'), ('Ã¤', 'ä'), ('Ã¶', 'ö'), \
     ( 'Ã„', 'Ä'), ('Ã–', 'Ö'), ('Ãœ', 'Ü'), ('ÃŸ', 'ß') \
    ]
    aftermapping = [ ('Ã', 'ß') ]
    #
    @staticmethod
    def output(text : str):
        """Prepare and output the text.
        Output: write in console, speak.
        Replace utf-8 double-byte (or, in fact, four-byte) umlauts right ones
        """
        txConv = text
        for k, v in VTextStatus.mapping:
            txConv = txConv.replace(k,v)
        for k, v in VTextStatus.aftermapping:
            txConv = txConv.replace(k,v)
        printAndSay(txConv)
    #
    @staticmethod
    def browsePage():
        """get content of videotext page at current page number"""
        VTextStatus.textNews.extractAndPreparePage(int(VTextStatus.page))
        VTextStatus.output(f"Blättern zu Seite {VTextStatus.page}")
        VTextStatus.output(VTextStatus.textNews.content)

VTextStatus.start()

while VTextStatus.isRunning:
    printAndSay("...")
    #
    try:
        newpage = input("Welche Seite lesen?")
        if newpage == "stop":
            VTextStatus.isRunning = False
            continue
        if newpage == "++":
            speaker.speakFaster()
            continue
        if newpage == "--":
            speaker.speakSlower()
            continue
        if newpage == "":
            continue
        if VTextStatus.hasrun and (newpage == "."):
            printAndSay("Seite wird neu geladen")
            VTextStatus.browsePage()
            continue
        #
        if newpage[0] == '>' or newpage == ' ':
            VTextStatus.sub += 1
            VTextStatus.textNews.extractAndPreparePage(\
             int(VTextStatus.page), VTextStatus.sub \
            )
            printAndSay(f"Blättern zu Seite {VTextStatus.page}")
            printAndSay(VTextStatus.textNews.content)
            continue
        # show new page
        VTextStatus.sub = 1
        #
        if newpage[0] == '/':
            VTextStatus.page = VTextStatus.textNews.bluePage
        elif newpage[0] == '*':
            VTextStatus.page = VTextStatus.textNews.yellowPage
        # forward and back
        elif newpage[0] == '-':
            if VTextStatus.page > 100:
                VTextStatus.page -= 1
        elif newpage[0] == '+':
            if VTextStatus.page < 899:
                VTextStatus.page += 1
        elif VTextStatus.textNews.hasTopicPage(newpage[0]):
            VTextStatus.hasrun = True
            VTextStatus.textNews.browseTopicPage(newpage[0])
            VTextStatus.page = VTextStatus.textNews.currentPage
            printAndSay(f"Blättern zu Seite {VTextStatus.page}")
            printAndSay(VTextStatus.textNews.content)
            continue
        elif not newpage.isdigit():
            printAndSay("Sorry, das ist keine Seitenzahl.")
            continue
        else:
            #arriving here, newpage is a number
            VTextStatus.hasrun = True
            VTextStatus.page = int(newpage)
        #
        VTextStatus.browsePage()
    except KeyboardInterrupt:
        printAndSay("\nProgramm wird beendet.")
        VTextStatus.isRunning = False
    except Exception as e:
        # HTTP error or anything
        printAndSay(f"Entschuldigung, etwas ist schiefgegangen.\nFehlermeldung:\n{e}")

# pylint: enable=W0718