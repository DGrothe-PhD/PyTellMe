# PyTellMe
Ziel dieses kleinen Projekts ist eine 
Verbesserung der Nutzbarkeit alltäglicher Infoquellen wie Videotext für Sehbehinderte.

Bisher ist der Videotext am TV-Gerät nur für Lesende oder unter Zuhilfenahme elektronischer Sehhilfen zu nutzen. 
Das ist sehr umständlich. Ebenso wie der (häufig anfangs ungewohnte) Ungang mit alles umfassenden Sprachassistenzprogrammen wie NVDA.
 
Da Videotext häufig auch online abrufbar ist, braucht man nur einen PC mit Python und dieses Projekt.

So lassen sich Fußballergebnisse, der Wetterbericht oder Aktienkurse abfragen und werden vorgelesen.

A simple speech and typing assistant that performs a small set of simple tasks, including:

## Features
teletext: interactive assistant with typed commands &rarr; `getVideoText.py`
* ARD-Text, rbbText, NDR, BR
* step through any text page
* if there's page 1/n step to next subpage via `>` or `<space>` to get to next page

Through teletext, the following things are available
* Weather
  * weather forecast from teletext: Berlin https://www.rbbtext.de/162
* Sports
  * latest Bundesliga results
  * UEFA Euro 2024
* Stock exchange (Börse)
  * All you can find in ARD-Text (page 700) is available now

Further features &rarr; `jarvis.py`
* date and time
  * what date and time is it
  * including weeknumber
* wikipedia
  * gather first few lines from an article on Wikipedia

## How it works

* Run a python file via command-line (powershell or cmd), e. g. `python jarvis.py`
* Speaker functionality implemented using `pyttsx3`.
* Speech-recognition functionality:<br>
I am not reinventing the wheel, but starting from a German translation of [@riitikiitkgp](https://github.com/riitikiitkgp/)'s [Jarvis-Voice-Assistant](https://github.com/riitikiitkgp/Jarvis-Voice-Assistant).
