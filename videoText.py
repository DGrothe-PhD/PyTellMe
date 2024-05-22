import requests
#, bs4
from gazpacho import Soup

class videoTextUtils:
    wochentage = { \
     "Mo" : "Montag", "Di": "Dienstag", "Mi": "Mittwoch", \
     "Do":"Donnerstag", "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag" \
    }

class rbbText:
    content = ""
    soup = Soup()
    lines = []
    
    def linefilter(self, text):
        return text.rstrip(' \xa0')
    
    def extractPage(self, page):
        if page > 899 or page < 100:
            page = 100
        res = requests.get('https://www.rbbtext.de/'+str(page))
        res.raise_for_status()
        #gazpacho
        self.soup = Soup(res.text)
        peas = self.soup.find("span", {"class": "fg"}, partial=True)
        self.lines = [self.linefilter(x.text) for x in peas]
    
    def appendContent(self):
        # process and prettify text
        for x in self.lines:
            if len(str(x)) > 1 :
                self.content += '\n' + str(x)
        if len(self.content) < 3:
            self.content += "Seite ist leer."
        self.content = self.content.replace('-\n', '')
        
    def __init__(self, page):
        self.extractPage(page)
        self.appendContent()

class rbbWeather(rbbText):
    tablepattern = "\xa0\xa0\xa0\xa0"
    weekdays = []
    mintemps = []
    maxtemps = []
    rainexpect = []
    kgN = False
    
    
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
        self.extractPage(page)
        
        # process and prettify text
        # make sentences from table
        if expectTable:
            for x in self.lines:
                if x.__contains__("&nbsp;&nbsp;&nbsp;&nbsp;"):
                    self.extractTable(x)
                elif x.__contains__(self.tablepattern):
                    self.extractTable(x, self.tablepattern)
                # by line: fluent text? append this line.
                elif len(str(x)) > 1 :
                    self.content += '\n' + str(x)
            for i in range(0, len(self.weekdays)):
                self.content += f"\n{videoTextUtils.wochentage[self.weekdays[i]]} morgens {self.mintemps[i]}, "
                self.content += f"maximal {str(self.maxtemps[i])} Grad, Niederschlagswahrscheinlichkeit " + \
                 f"{self.rainexpect[i]} Prozent."
        else:
            self.appendContent()