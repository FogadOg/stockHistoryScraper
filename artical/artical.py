import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '..'))
sys.path.append(parentDir)


import requests, spacy, datetime, csv
from bs4 import BeautifulSoup
from stock.stockHistory import StockHistory
from stringToDatetime import StringToDatetime

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '..'))

sys.path.append(parentDir)
nlp = spacy.load("en_core_web_sm")

class Artical():
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        self.title = self._getTitle()
        self.publishTime = self._getPublishTime()
        self.content = self.title + self._getContent()

        self.releventCompanies = self._extractCompanies()

    def _getTitle(self) -> str:
        try:
            titleElement = self.soup.find(class_="ArticleHeader-headline")

            if titleElement == None:
                return self.soup.find(class_="LiveBlogHeader-headline").text

            return titleElement.text
        except:
            raise AttributeError("Not valid artical")

    def _getPublishTime(self) -> datetime:
        publishTime = self.soup.find('time').text   
        time_parts = publishTime.split(' ', 1)

        timeString = time_parts[1].upper()


        return StringToDatetime(timeString).getDatetime()

    def _getContent(self) -> str:
        textContainers = self.soup.find_all(class_="group")
        articalText = ""

        for textContainer in textContainers:
            articalText += textContainer.text

        return articalText

    def _extractCompanies(self):
        doc = nlp(self.content)
        companies = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        return list(set(companies))

    def getStockHistory(self, company:str) -> StockHistory:
        try:
            return StockHistory(company, self.publishTime)
        except IndexError:
            try:
                replacmentDate = self._getReplacementDate(self.publishTime)
                return StockHistory(company, replacmentDate)
            except:
                pass
        except KeyError:
            return None
    
    def _getReplacementDate(self, dt):
        if dt.time() < datetime.datetime.strptime('09:30', '%H:%M').time():
            if self._isItPastTime(self):
                return dt.replace(hour=9, minute=30, second=0, microsecond=0)
            
        raise IndexError(f"articel was published {self.publishTime} which is after closing time")
    
    def _isItPastTime(self, targetHour: int = 10, targetMinute: int = 30):
        currentTime = datetime.datetime.now().time()
        targetTime = datetime.datetime.strptime(f"{targetHour}:{targetMinute}", "%H:%M").time()
        return currentTime > targetTime

    def __str__(self):
        return self.title


if __name__ == "__main__":
    artical = Artical("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")

