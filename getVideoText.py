from videoText import rbbText, ardText, bayernText, ndrText
# todo: from ... import applied speaker

welcome = "Hallo, ich bin dein Videotext-Assistent.\n\n Eingabe Seitenzahl (dreistellig), Beenden durch die Eingabe 'stop'."
limitation = "Bis jetzt kann ich nur eine Auswahl von Videotexten."

class videotextStatus:
    isRunning = True
    page = 100
    sub = 1
    textNews = rbbText(page)


print(welcome)
print(limitation)

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
for k in stationlist_examples.keys():
    examples.append(f"{k}:  {', '.join(stationlist_examples[k])}")

tell_available_stations = "\n".join(examples)
station = input("Welchen Sendetext möchten Sie aufrufen?\n[  Beispiele:  ]\n" + tell_available_stations + "\n...:")
#
#
if station.lower() in stationlist_erste:
    videotextStatus.textNews = ardText(100)
elif station.lower() in stationlist_ndr:
    videotextStatus.textNews = ndrText(100)
elif station.lower() in stationlist_bayern:
    videotextStatus.textNews = bayernText(100)
else:
    pass

while videotextStatus.isRunning:
    print("...")
    #
    try:
        newpage = input("Welche Seite möchtest du lesen?")
        if newpage[0] == '>' or newpage == ' ':
            videotextStatus.sub += 1
            videotextStatus.textNews.extractAndPreparePage(int(videotextStatus.page), videotextStatus.sub)
            print(f"Blättern zu Seite {videotextStatus.page}")
            print(videotextStatus.textNews.content)
            continue
        
        # show new page
        videotextStatus.sub = 1
        if newpage == "stop":
            videotextStatus.isRunning = False
            continue
        elif newpage[0] == '/':
            videotextStatus.page = videotextStatus.textNews.bluePage
        elif newpage[0] == '*':
            videotextStatus.page = videotextStatus.textNews.yellowPage
        # forward and back
        elif newpage[0] == '-':
            videotextStatus.page = 100 if (videotextStatus.page <= 101) else videotextStatus.page - 1
        elif newpage[0] == '+':
            videotextStatus.page = 100 if (videotextStatus.page >= 899) else videotextStatus.page + 1 
        #
        elif not newpage.isdigit():
            print("Sorry, das ist keine Seitenzahl.")
            continue
        else:
            videotextStatus.page = int(newpage)
        
        # browse page
        videotextStatus.textNews.extractAndPreparePage(int(videotextStatus.page))
        print(f"Blättern zu Seite {videotextStatus.page}")
        print(videotextStatus.textNews.content)
        #
    except Exception as e:
        # HTTP error or anything
        print(f"Entschuldigung, etwas ist schiefgegangen.") 
        print(e)
