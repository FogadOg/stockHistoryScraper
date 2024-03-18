import requests, spacy, datetime, csv
from bs4 import BeautifulSoup
from stock.stockHistory import StockHistory
from utils.stringToDatetime import StringToDatetime


nlp = spacy.load("en_core_web_sm")

class Artical():
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        self.title = self.getTitle()
        self.publishTime = self.getPublishTime()
        # self.publishTime = datetime.datetime(2024, 3, 11, 12, 30, 0)
        self.content = self.title + self.getContent()

        self.releventCompanies = self._extractCompanies()

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
        except:
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

