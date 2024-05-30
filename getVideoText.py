import requests
from videoText import rbbText, ardText, bayernText, ndrText, videoTextUtils
# todo: from ... import applied speaker

WELCOME = """Hallo, ich bin dein Videotext-Assistent.
Eingabe Seitenzahl (dreistellig),
Beenden durch die Eingabe 'stop'."""
LIMITATION = "Bis jetzt kann ich nur eine Auswahl von Videotexten."

class VTextStatus(videoTextUtils):
    isRunning = True
    page = 100
    sub = 1
    #
    textNews = rbbText(page)

print(WELCOME)
print(LIMITATION)

stationlist_erste = {"1", "das erste", "ard"}
stationlist_ndr = {"nord", "ndr"}
stationlist_bayern = {"bayern", "br"}
stationlist_examples = { \
 "Das Erste" : stationlist_erste,
 #"NDR" : stationlist_ndr,
 "BR" : stationlist_bayern
}
#
examples = []
for station, aliases in stationlist_examples.items():
    examples.append(f"{station}:  {', '.join(aliases)}")

TELL_AVAILABLE_STATIONS = "\n".join(examples)
user_which_videotext = "Welchen Sendetext möchten Sie aufrufen?\n[  Beispiele:  ]\n"
station = input(user_which_videotext + TELL_AVAILABLE_STATIONS + "\n...:")
#
#
if station.lower() in stationlist_erste:
    VTextStatus.textNews = ardText(100)
elif station.lower() in stationlist_ndr:
    VTextStatus.textNews = ndrText(100)
elif station.lower() in stationlist_bayern:
    VTextStatus.textNews = bayernText(100)
else:
    pass

while VTextStatus.isRunning:
    print("...")
    #
    try:
        newpage = input("Welche Seite möchtest du lesen?")
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
        #
        elif not newpage.isdigit():
            print("Sorry, das ist keine Seitenzahl.")
            continue
        else:
            VTextStatus.page = int(newpage)
        
        # browse page
        VTextStatus.textNews.extractAndPreparePage(int(VTextStatus.page))
        print(f"Blättern zu Seite {VTextStatus.page}")
        print(VTextStatus.textNews.content)
    except Exception as e:
        # HTTP error or anything
        print(f"Entschuldigung, etwas ist schiefgegangen.\nFehlermeldung:\n{e}") 