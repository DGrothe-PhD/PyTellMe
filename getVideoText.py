from videoText import rbbText
# todo: from ... import applied speaker

welcome = "Hallo, ich bin dein Videotext-Assistent.\n\n Eingabe Seitenzahl (dreistellig), Beenden durch die Eingabe 'stop'."
limitation = "Bis jetzt kann ich nur den RBB-Text."

class videotextStatus:
    isRunning = True
    page = 100
    textNews = rbbText(page)

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
