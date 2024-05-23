# PyTellMe
A simple speech assistant that performs a small set of simple tasks, including:

## Features
* teletext
  * get the weather forecast from teletext: Berlin https://www.rbbtext.de/162
  * step through any text page
  * if there's page 1/n step to next subpage via `>` or `<space>` to get to next page 
  * latest Bundesliga results

* Stock exchange (Börse)
  * All you can find in ARD-Text is available now
  
* date and time
  * what date and time is it
  * including weeknumber

* wikipedia
  * gather first few lines from an article on Wikipedia

## How it works
 
* Speaker functionality implemented using `pyttsx3`.
* Speech-recognition functionality:<br>
I am not reinventing the wheel, but starting from a German translation of [@riitikiitkgp](https://github.com/riitikiitkgp/)'s [Jarvis-Voice-Assistant](https://github.com/riitikiitkgp/Jarvis-Voice-Assistant).
