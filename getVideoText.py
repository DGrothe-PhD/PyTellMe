from videoText import rbbText
# todo: from ... import applied speaker

welcome = "Hallo, ich bin dein Videotext-Assistent.\n\n Eingabe Seitenzahl (dreistellig), Beenden durch die Eingabe 'stop'."
limitation = "Bis jetzt kann ich nur den RBB-Text."

class videotextStatus:
    isRunning = True
    page = 100

print(welcome)
print(limitation)

while videotextStatus.isRunning:
    print("...")
    #
    try:
        newpage = input("Welche Seite möchtest du lesen?")
        if newpage == "stop":
            videotextStatus.isRunning = False
            continue
        elif newpage[0] == '-':
            print(f"page: {videotextStatus.page}")
            videotextStatus.page = 100 if (videotextStatus.page <= 101) else videotextStatus.page - 1
            print(f"Zurückblättern zu Seite {videotextStatus.page}")
        elif newpage[0] == '+':
            print(f"page: {videotextStatus.page}")
            videotextStatus.page = 100 if (videotextStatus.page >= 899) else videotextStatus.page + 1 
            print(f"Vorblättern zu Seite {videotextStatus.page}")
        elif not newpage.isdigit():
            print("Sorry, das ist keine Seitenzahl.")
            continue
        else:
            videotextStatus.page = int(newpage)
        
        # browse page
        textNews = rbbText(int(videotextStatus.page))
        print(textNews.content)
        #
    except Exception as e:
        # HTTP error or anything
        print(f"Entschuldigung, etwas ist schiefgegangen.") 
        print(e)
