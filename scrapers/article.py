import requests, spacy, datetime, csv
from bs4 import BeautifulSoup
from utils.stockHistory import StockHistory
from utils.stringToDatetime import StringToDatetime


nlp = spacy.load("en_core_web_sm")

class Article():
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        self.title = self.getTitle()
        self.timeZone = 'US/Eastern'
        self.publishTime: datetime.datetime = self.getPublishTime()
        # self.publishTime = datetime.datetime(2024, 3, 11, 12, 30, 0)
        self.content = self.title + " " + self.getContent()

        self.releventCompanies = self._extractCompanies()

    def _extractCompanies(self):
        doc = nlp(self.content)
        companies = [entity.text.lower() for entity in doc.ents if entity.label_ == "ORG"]
        return list(set(companies))

    def getStockHistory(self, company:str) -> StockHistory:
        if self.isWeekend():
            daysToAdd = 7 - self.publishTime.weekday()
            nextMonday = self.publishTime + datetime.timedelta(days=daysToAdd)
            newDate = nextMonday.replace(hour=9, minute=30)

            return StockHistory(company, newDate)
        return StockHistory(company, self.publishTime)
    
    def isWeekend(self) -> bool:
        return self.publishTime.weekday() >= 5
    
    def _getReplacementDate(self, objectTime: datetime):
        if self._isItPastTime() == False:
            return objectTime.replace(hour=9, minute=30)
        elif self._isItPastTime(16, 0):
            newTime = objectTime.replace(hour=9, minute=30)
            return newTime + datetime.timedelta(days=1)
        
        return objectTime
            
    
    def _isItPastTime(self, specificHour: int = 9, specificMinute: int = 30):
        hour = self.publishTime.hour
        minute = self.publishTime.minute

        return (hour, minute) > (specificHour, specificMinute)

    def __str__(self):
        return self.title


if __name__ == "Main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")

