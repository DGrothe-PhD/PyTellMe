#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from videoText import rbbText, ARDText, BayernText, NDRText, videoTextUtils
# todo: from ... import applied speaker


class VTextStatus(videoTextUtils):
    WELCOME = "Hallo, ich bin dein Videotext-Assistent." + \
     "Eingabe Seitenzahl (dreistellig)," + \
     "Beenden durch die Eingabe 'stop'."
    LIMITATION = "Bis jetzt kann ich nur eine Auswahl von Videotexten."
    isRunning = True
    page = 100
    sub = 1
    textNews = rbbText(page)
    stationlist_erste = {"1", "das erste", "ard"}
    stationlist_ndr = {"nord", "ndr"}
    stationlist_bayern = {"6", "bayern", "br"}
    stationlist_rbb = {"3", "rbb", "berlin"}
    
    stationlist_examples = { \
     "Das Erste" : stationlist_erste,
     #"NDR" : stationlist_ndr,
     "BR" : stationlist_bayern,
     "rbb" : stationlist_rbb
    }
    
    @staticmethod
    def start():
        print(VTextStatus.WELCOME)
        print(VTextStatus.LIMITATION)
        examples = []
        for station, aliases in VTextStatus.stationlist_examples.items():
            examples.append(f"{station}:  {', '.join(aliases)}")
        TELL_AVAILABLE_STATIONS = "\n".join(examples)
        userWhichVideotext = "Welchen Sendetext möchten Sie aufrufen?\n[  Beispiele:  ]\n"
        station = input(userWhichVideotext + TELL_AVAILABLE_STATIONS + "\n...:")
        #
        if station.lower() in VTextStatus.stationlist_erste:
            VTextStatus.textNews = ARDText(100)
        elif station.lower() in VTextStatus.stationlist_ndr:
            VTextStatus.textNews = NDRText(100)
        elif station.lower() in VTextStatus.stationlist_bayern:
            VTextStatus.textNews = BayernText(100)
        else:
            pass
    
    mapping = [ ('Ã¼', 'ü'), ('Ã¤', 'ä'), ('Ã¶', 'ö'), \
     ( 'Ã„', 'Ä'), ('Ã–', 'Ö'), ('Ãœ', 'Ü'), ('ÃŸ', 'ß'), ('Ã', 'ß') 
    ]
    
    @staticmethod
    def output(Text):
        txConv = Text
        for k, v in VTextStatus.mapping:
            txConv = txConv.replace(k,v)
        print(txConv)

VTextStatus.start()

while VTextStatus.isRunning:
    print("...")
    #
    try:
        newpage = input("Welche Seite lesen?")
        if newpage[0] == '>' or newpage == ' ':
            VTextStatus.sub += 1
            VTextStatus.textNews.extractAndPreparePage(\
             int(VTextStatus.page), VTextStatus.sub \
            )
            print(f"Blättern zu Seite {VTextStatus.page}")
            print(VTextStatus.textNews.content)
            continue
        # show new page
        VTextStatus.sub = 1
        if newpage == "stop":
            VTextStatus.isRunning = False
            continue
        if newpage == ".":
            print("Seite wird neu geladen")
        elif newpage[0] == '/':
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
        #
        elif not newpage.isdigit():
            print("Sorry, das ist keine Seitenzahl.")
            continue
        else:
            VTextStatus.page = int(newpage)
        
        # browse page
        VTextStatus.textNews.extractAndPreparePage(int(VTextStatus.page))
        VTextStatus.output(f"Blättern zu Seite {VTextStatus.page}")
        VTextStatus.output(VTextStatus.textNews.content)
    except Exception as e:
        # HTTP error or anything
        print(f"Entschuldigung, etwas ist schiefgegangen.\nFehlermeldung:\n{e}") 