import re
import requests
from gazpacho import Soup
from bs4 import BeautifulSoup

# pylint: disable=R0903
# pylint: disable=broad-except
# pylint: disable=too-many-instance-attributes

class VideoTextUtils:
    """general settings for videotext"""
    pageNotAccessible = "Diese Seite kann nicht angezeigt werden."
    wochentage = { \
     "Mo" : "Montag", "Di": "Dienstag", "Mi": "Mittwoch", \
     "Do":"Donnerstag", "Fr": "Freitag", "Sa": "Samstag", "So": "Sonntag" \
    }
    #
    topicKeys = { \
     "a" : "Abendprogramm", "d" : "DAX", "e" : "Wirtschaft", \
     "g" : "Gemischtes", \
     "b" : "Börse", "i" : "Indizes", "m" : "MDAX", \
     "p" : "Politik", \
     "s" : "Sport", \
     "t" : "TV-Programm", \
     "u" : "Unwetterwarnungen", "v" : "Verbrauchertipps", \
     "x" : "Extra", \
     "w" : "Wetter", \
    }

class RbbText:
    """Reads any RbbText page.

    Properties:
        content: the text of the videotext page.
        api      web page address
    """
    content = ""
    yellowPage = 100
    bluePage = 100
    currentPage = 100
    soup = Soup()
    lines = []
    peas = None
    peasStyle = None
    #
    topicPages = { \
     "a" : 303, "d" : 100, "e" : 125, "g" : 105, \
     "b" : 100, "i" : 100, "m" : 100, "p" : 100, \
     "s" : 200, \
     "t" : 300, \
     "u" : 190, "v" : 100, \
     "x" : 600, \
     "w" : 160, \
    }
    #
    ballgamescorepages = { \
     252, 276
    }
    listOfBallGames = { \
     "Fußball", "Handball", "Basketball", \
     "Eishockey", "Hockey", "Volleyball" \
    }
    #
    api = 'https://www.rbbtext.de/'
    #
    def linefilter(self, text : str):
        """remove symbols"""
        return text.rstrip(' \xa0')
    #
    def clearContent(self):
        """just clear page content"""
        self.content = ""
    #
    def clearValues(self):
        """reset to default values"""
        self.yellowPage = 100
        self.bluePage = 100
        self.lines = []
        self.peas = None
        self.peasStyle = None
    #
    def validateSoup(self, contents):
        """Validate Soup() object. 

        Args:
            `contents` (Soup(), list of Soup(), NoneType): return object of Soup.find()

        Returns:
            list of Soup() object(s) or empty list.\n
        """
        if isinstance(contents, list) and len(contents) > 0:
            return contents
        if isinstance(contents, Soup):
            return [contents]
        return []
    #
    def extractPage(self, page: int, sub=1):
        """Requests content of videotext at page `page`, subpage `sub`/n

        Args:
            page (int): a value between 100 and 899
            sub (int, optional): Number of subpage. Defaults to 1.
        """
        try:
            self.clearValues()
            if page > 899 or page < 100:
                page = 100
            if '#' in self.api:
                res = requests.get(self.api.replace('#', str(page)), timeout=20)
            else:
                res = requests.get(self.api+str(page)+(f"&sub={sub}" if sub >1 else ""), timeout=20)
            res.raise_for_status()
            #gazpacho
            self.soup = Soup(res.text)
            peas = self.soup.find("span", {"class": "fg"}, partial=True)
            peasStyle = self.soup.find("span", {"class" : "style"}, partial=True)
            #
            # gazpacho extraction got stuck on false page links
            # which are in fact numbers in disguise. The 690s (NBA) of ARD-Text have that.
            # so I use bs4 for less boilerplate code.
            for x in self.validateSoup(peas):
                addline = self.linefilter( \
                 BeautifulSoup(x.html, features="html.parser").text.strip() \
                )
                self.lines.append(addline)
            #
            # gather info like 'Thema xyz on page 123'
            for x in self.validateSoup(peasStyle):
                addline = self.linefilter(x.text)
                alist = x.find("a")
                alist = self.validateSoup(alist)
            #
                for y in alist:
                    if len(y.html) > 1:
                        linkedPages = re.findall(r'\d+', y.html)
                        addline += " " + linkedPages[-1]
                self.lines.append(addline)
        except requests.exceptions.HTTPError as httpErr:
            message = "Die Seite kann nicht angezeigt werden " + \
             f"(Fehler {httpErr.response.status_code})"
            self.lines.append(message)
        except requests.exceptions.ConnectionError:
            self.lines.append(VideoTextUtils.pageNotAccessible)
        except requests.exceptions.Timeout:
            self.lines.append("Zeitüberschreitung")
        except requests.exceptions.RequestException as e:
            self.lines.append(f"Konnte Seite {self.api}... nicht aufrufen. \nFehler: {e}")
        except Exception as e:
            self.lines.append("Etwas lief schief...")
            print(f"Fehlermeldung: {e}")
    #
    def extractJumpingPages(self):
        """Extracts topic and page number to jump to with yellow and blue remote button"""
        yellowbean = self.soup.find("span", {"class": "block_yellow"})
        if len(self.validateSoup(yellowbean)) > 0:
            yellowlink = self.validateSoup(yellowbean.find("a"))[0]
            if len(yellowlink.text) > 1:
                self.yellowPage = int(yellowlink.attrs.get("href").strip('/'))
                self.content += f"\nSternchen blättert zu {yellowlink.text}" + \
                 f" auf Seite {self.yellowPage}"
        #
        bluebean = self.soup.find("span", {"class": "block_blue"})
        #
        if len(self.validateSoup(bluebean)) > 0:
            bluelink = self.validateSoup(bluebean.find("a"))[0]
            if len(bluelink.text) > 1:
                self.bluePage = int(bluelink.attrs.get("href").strip('/'))
                self.content += f"\nDivisions-Taste blättert zu {bluelink.text} " + \
                 f"auf Seite {self.bluePage}"
    #
    def appendContent(self):
        """process and prettify extracted text lines and append these to content"""
        isBallGame = False
        for x in self.lines:
            xAsText = str(x)
            if len(xAsText) > 1 :
                # I am canceling the first line of the text with a timestamp here
                # as a timestamp is not a score.
                if any(sport in xAsText for sport in self.listOfBallGames):
                    isBallGame = True
                if isBallGame or self.currentPage in self.ballgamescorepages \
                 and not xAsText.strip().endswith(":"):
                    xAsText = xAsText.replace("--:--", "noch kein Ergebnis")
                    xAsText = re.sub(r"-\:-\s+\(-\:-\)", "noch kein Ergebnis", xAsText)
                    xAsText = xAsText.replace("-:-", "noch kein Ergebnis")
                    xAsText = re.sub(r"([0-9]{1,}):([0-9]{1,})", r"\1 zu \2", xAsText)
                self.content += '\n' + xAsText
        if len(self.content) < 3:
            self.content += "Seite ist leer."
        self.content = self.content.replace('-\n', '')
    #
    def extractAndPreparePage(self, page: int, sub=1):
        """Extracts page content, formats everything and writes text into `content`.

        Args:
            page (int): a value between 100 and 899
            sub (int, optional): Number of subpage. Defaults to 1.
        """
        self.currentPage = page
        self.clearContent()
        self.extractPage(page, sub)
        self.appendContent()
        self.extractJumpingPages()
    #
    def hasTopicPage(self, topicChar):
        """Returns true if there is a topic page which is referenced by the character `topicChar`.
        """
        try:
            return topicChar in self.topicPages
        except AttributeError:
            return False
    #
    def browseTopicPage(self, topicChar):
        """Opens the topic page which is referenced by the character `topicChar`.
            If that page does not exist, opens page 100.
        """
        chosenPage = self.topicPages.get(topicChar, 100)
        self.extractAndPreparePage(chosenPage)
    #
    def getPageNumber(self):
        """returns page number"""
        return self.currentPage
    #
    def __init__(self, page : int):
        self.currentPage = page
        self.extractAndPreparePage(page)


class ARDText(RbbText):
    """gets videotext from DasErste.de (ARD-Text)
    
    Attributes: 
        topicPages:   quick access topic text numbers
    """
    topicPages = { \
     "a" : 303, "d" : 715, "e" : 155, "g" : 135, \
     "b" : 700, "i" : 711, "m" : 716, "p" : 130, \
     "s" : 200, \
     "t" : 300, \
     "u" : 178, "v" : 165, \
     "x" : 600, \
     "w" : 171, \
    }
    #
    api = 'https://www.ard-text.de/index.php?page='

class NDRText(RbbText):
    """gets videotext from NDR Norddeutscher Rundfunk"""
    #api = https://www.ndr.de/public/teletext/521_01.htm
    #api = 'https://www.ndr.de/fernsehen/videotext/index.html'
    api = 'https://www.ndr.de/fernsehen/videotext/ndr5478.html?seite='

class BayernText(RbbText):
    """gets videotext from BR (Bayerischer Rundfunk)"""
    api = 'https://www.br.de/fernsehen/brtext/brtext-100.html?vtxpage='

class RbbWeather(RbbText):
    """gets and formats weather forecast from RbbText"""
    tablepattern = "\xa0\xa0\xa0\xa0"
    timeTermsList = ["Nachts", "Abends", "Nachmittags", "Heute", \
      "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Sonnabend", "Samstag", "Sonntag",
    ]
    weekdays = []
    mintemps = []
    maxtemps = []
    rainexpect = []
    isRainForecast = False
    #
    # preparation talk a table in clear sentences.
    '''
    # just in case (bs4 style-dependent)
    # '\xa0...' can read '&nbsp;&nbsp;&nbsp;&nbsp;'
    '''
    def extractTable(self, text : str, tabpattern='&nbsp;&nbsp;&nbsp;&nbsp;'):
        """Preparation to speak a weather table in clear sentences.

        Args:
            text: text line (string)
            tabpattern (str, optional): fill between videotext column cells. 
            Defaults to '&nbsp;&nbsp;&nbsp;&nbsp;'.
        """
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
    #
    def __init__(self):
        """read RBB Weather"""
        super().__init__(162)
        self.content += "\n\n"
        self.extractPage(163)
        # process and prettify text
        # make sentences from table
        for x in self.lines:
            if x.__contains__("&nbsp;&nbsp;&nbsp;&nbsp;"):
                self.extractTable(x)
            elif x.__contains__(self.tablepattern):
                self.extractTable(x, self.tablepattern)
            # by line: fluent text? append this line.
            elif len(str(x)) > 1 and any(timeterms in str(x) for timeterms in self.timeTermsList):
                self.content += '\n' + str(x)
            elif len(str(x)) > 1:
                self.content += '\n' + str(x.strip())
        #for i in range(0, len(self.weekdays)):
        for i, w in enumerate(self.weekdays):
            self.content += f"\n{VideoTextUtils.wochentage[w]} morgens {self.mintemps[i]}, "
            self.content += f"maximal {str(self.maxtemps[i])} Grad," + \
             f" Niederschlagswahrscheinlichkeit {self.rainexpect[i]} Prozent."
        self.content = self.content.replace('-\n', '')
        self.content = self.content.replace('343', '')
        self.content = self.content.replace('rbb-Programmhighlights', '')
        self.extractJumpingPages()
# pylint: enable=R0903
# pylint: enable=broad-except