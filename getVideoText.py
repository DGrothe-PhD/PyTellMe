from videoText import rbbText
# todo: from ... import applied speaker

welcome = "Hallo, ich bin dein Videotext-Assistent."
limitation = "Bis jetzt kann ich nur den RBB-Text."

class videotextStatus:
    isRunning = True

print(welcome)
print(limitation)

while videotextStatus.isRunning:
    print("...")
    try:
        page = input("Welche Seite möchtest du lesen?")
        if not page.isdigit():
            print("Sorry, das ist keine Seitenzahl.")
            continue
        textNews = rbbText(int(page))
        print(textNews.content)
        #
        if input("Weiter oder stop?") == "stop":
            videotextStatus.isRunning = False
    except Exception as e:
        print(f"Entschuldigung, etwas ist schiefgegangen.") 
        print(e)
