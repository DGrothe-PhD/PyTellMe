import re
import requests
from gazpacho import Soup

class videoTextUtils:
    PAGE_NOT_ACCESSIBLE = "Diese Seite kann nicht angezeigt werden."
    wochentage = { \
     "Mo" : "Montag", "Di": "Dienstag", "Mi": "Mittwoch", \
     "Do":"Donnerstag", "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag" \
    }

class rbbText:
    content = ""
    yellowPage = 100
    bluePage = 100
    soup = Soup()
    lines = []
    peas = None
    peas_style = None
    
    api = 'https://www.rbbtext.de/'
    #
    def linefilter(self, text):
        return text.rstrip(' \xa0')
    #
    def clearValues(self):
        self.content = ""
        self.yellowPage = 100
        self.bluePage = 100
        self.lines = []
        self.peas = None
        self.peas_style = None
    #
    def checkSoup(self, contents):
        return type(contents) == list and len(contents) > 0
    #
    def validateSoup(self, contents):
        if type(contents) == list and len(contents) > 0:
            return contents
        if type(contents) == Soup:
            return [contents]
        return []
    #
    def extractPage(self, page, sub=1):
        try:
            self.clearValues()
            if page > 899 or page < 100:
                page = 100
            if '#' in self.api:
                res = requests.get(self.api.replace('#', str(page)))
            else:
                res = requests.get(self.api+str(page)+(f"&sub={sub}" if sub >1 else ""))
            res.raise_for_status()
            #gazpacho
            self.soup = Soup(res.text)
            peas = self.soup.find("span", {"class": "fg"}, partial=True)
            peas_style = self.soup.find("span", {"class" : "style"}, partial=True)
            #
            self.lines += [self.linefilter(x.text) for x in self.validateSoup(peas)]
            # gather info like 'Thema xyz on page 123'
            for x in self.validateSoup(peas_style):
                addline = self.linefilter(x.text)
                alist = x.find("a")
                alist = self.validateSoup(alist)
            #
                for y in alist:
                    if len(y.html) > 1:
                        linked_pages = re.findall("\d+", y.html)
                        addline += " " + linked_pages[-1]
                self.lines.append(addline)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP Fehlermeldung: {http_err}')
        except requests.exceptions.ConnectionError:
            print(videoTextUtils.PAGE_NOT_ACCESSIBLE)
        except requests.exceptions.Timeout:
            print("Zeitüberschreitung")
        except requests.exceptions.RequestException as e:
            print(f"Konnte Seite {self.api}... nicht aufrufen. \nFehler: {e}")
        except Exception as e:
            print("Something went wrong.")
            print(f"Fehlermeldung: {e}")
    #
    def extractJumpingPages(self):
        yellowbean = self.soup.find("span", {"class": "block_yellow"})
        if len(self.validateSoup(yellowbean)) > 0:
            yellowlink = self.validateSoup(yellowbean.find("a"))[0]
            if len(yellowlink.text) > 1:
                self.yellowPage = int(yellowlink.attrs.get("href").strip('/'))
                self.content += f"\nSternchen blättert zu {yellowlink.text}" + \
                 f" auf Seite {self.yellowPage}"
        #
        bluebean = self.soup.find("span", {"class": "block_blue"})
        
        if len(self.validateSoup(bluebean)) > 0:
            bluelink = self.validateSoup(bluebean.find("a"))[0]
            if len(bluelink.text) > 1:
                self.bluePage = int(bluelink.attrs.get("href").strip('/'))
                self.content += f"\nDivisions-Taste blättert zu {bluelink.text} " + \
                 f"auf Seite {self.bluePage}"
    #
    def appendContent(self):
        # process and prettify text
        for x in self.lines:
            if len(str(x)) > 1 :
                self.content += '\n' + str(x)
        if len(self.content) < 3:
            self.content += "Seite ist leer."
        self.content = self.content.replace('-\n', '')
    #
    def extractAndPreparePage(self, page, sub=1):
        self.extractPage(page, sub)
        self.appendContent()
        self.extractJumpingPages()
    #
    def __init__(self, page):
        self.extractAndPreparePage(page)



class ardText(rbbText):
    api = 'https://www.ard-text.de/index.php?page='

class ndrText(rbbText):
    #api = https://www.ndr.de/public/teletext/521_01.htm
    #api = 'https://www.ndr.de/fernsehen/videotext/index.html'
    api = 'https://www.ndr.de/fernsehen/videotext/ndr5478.html?seite='

class bayernText(rbbText):
    api = 'https://www.br.de/fernsehen/brtext/brtext-100.html?vtxpage='

class rbbWeather(rbbText):
    tablepattern = "\xa0\xa0\xa0\xa0"
    weekdays = []
    mintemps = []
    maxtemps = []
    rainexpect = []
    isRainForecast = False
    
    
    # preparation talk a table in clear sentences.
    '''
    # just in case (bs4 style-dependent)
    # '\xa0...' can read '&nbsp;&nbsp;&nbsp;&nbsp;'
    '''
    def extractTable(self, text, tabpattern='&nbsp;&nbsp;&nbsp;&nbsp;'):
        if "Sa" in text or "Mo" in text:
            self.weekdays = text.strip('\xa0').split(tabpattern)
        elif text.startswith("Max"):
            self.maxtemps = text.strip('\xa0').split(tabpattern)[1:]
        elif text.startswith("Min"):
            self.mintemps = text.strip('\xa0').split(tabpattern)[1:]
            self.isRainForecast = True
        elif self.isRainForecast:
            self.rainexpect = text.strip('\xa0').rstrip('%').split(tabpattern)
            self.isRainForecast = False
    
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
            #for i in range(0, len(self.weekdays)):
            for i, w in enumerate(self.weekdays):
                self.content += f"\n{videoTextUtils.wochentage[w]} morgens {self.mintemps[i]}, "
                self.content += f"maximal {str(self.maxtemps[i])} Grad, Niederschlagswahrscheinlichkeit " + \
                 f"{self.rainexpect[i]} Prozent."
        else:
            self.appendContent()
        self.content = self.content.replace('-\n', '')
        self.extractJumpingPages()