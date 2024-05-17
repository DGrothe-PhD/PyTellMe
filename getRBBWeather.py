import requests, bs4
#from gazpacho import Soup

wochentage = { \
 "Mo" : "Montag", "Di": "Dienstag", "Mi": "Mittwoch", \
 "Do":"Donnerstag", "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag" \
}

class rbbText:
    content = ""
    weekdays = []
    mintemps = []
    maxtemps = []
    rainexpect = []
    kgN = False
    
    def __filter(self, text):
        return text.rstrip(' \xa0')
    
    # preparation talk a table in clear sentences.
    '''
    # just in case (bs4 style-dependent)
    # '\xa0...' can read '&nbsp;&nbsp;&nbsp;&nbsp;'
    '''
    def extractTable(self, text, tabpattern='&nbsp;&nbsp;&nbsp;&nbsp;'):
        if text.__contains__("Sa") or text.__contains__("Mo"):
            self.weekdays = text.strip('\xa0').split(tabpattern)
        
        elif text.startswith("Max"):
            self.maxtemps = text.strip('\xa0').split(tabpattern)[1:]
        
        elif text.startswith("Min"):
            self.mintemps = text.strip('\xa0').split(tabpattern)[1:]
            self.kgN = True
            # safety, percent mark is too insignificant, use once.
        
        elif text.__contains__('%') and self.kgN:
            self.rainexpect = text.strip('\xa0').rstrip('%').split(tabpattern)
            self.kgN = False
    
    def __init__(self, page, expectTable=False):
        if page > 899 or page < 100:
            page = 100
        res = requests.get('https://www.rbbtext.de/'+str(page))
        res.raise_for_status()
        #bs4
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        peas = soup.find_all("span", class_=["fgw", "fgc", "fgy", "fgm", "fgr" ])
        
        lines = [self.__filter(x.text) for x in peas]
        #lines = [x for x in stuff]
        
        # make sentences from table
        if expectTable:
            for x in lines:
                if x.__contains__("&nbsp;&nbsp;&nbsp;&nbsp;"):
                    self.extractTable(x)
                elif x.__contains__("\xa0\xa0\xa0\xa0"):
                    self.extractTable(x, "\xa0\xa0\xa0\xa0")
                elif len(str(x)) > 1 :
                    self.content += '\n' + str(x)
            for i in range(0, len(self.weekdays)):
                self.content += '\n' + \
                 wochentage[self.weekdays[i]] + f" morgens {self.mintemps[i]}, "
                self.content += "maximal "+ str(self.maxtemps[i]) + " Grad, Niederschlagswahrscheinlichkeit " + \
                 f"{self.rainexpect[i]} Prozent."
        else:
            for x in lines:
                if len(str(x))>1:
                    self.content += '\n' + str(x)
        self.content = self.content.replace('-\n', '')

# Tonight and tomorrow
print("Wetter: ")

textHeute = rbbText(162, False)
print(textHeute.content)

print("Aussichten: ")
textAussichten = rbbText(163, True)
print(textAussichten.content)
