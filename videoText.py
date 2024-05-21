import requests
#, bs4
from gazpacho import Soup

class rbbText:
    content = ""
    def __filter(self, text):
        return text.rstrip(' \xa0')
    
    def __init__(self, page):
        if page > 899 or page < 100:
            page = 100
        res = requests.get('https://www.rbbtext.de/'+str(page))
        res.raise_for_status()
        #gazpacho
        soup = Soup(res.text)
        peas = soup.find("span", {"class": "fg"}, partial=True)
        lines = [self.__filter(x.text) for x in peas]
        
        # process and prettify text
        for x in lines:
            if len(str(x)) > 1 :
                self.content += '\n' + str(x)
        if len(self.content) < 3:
            self.content += "Seite ist leer."
        self.content = self.content.replace('-\n', '')
