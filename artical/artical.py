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

        self.title = self.getTitle()
        self.publishTime = datetime.datetime(2024, 3, 14, 12, 00, 0)
        self.content = self.title + self.getContent()

        self.releventCompanies = self.extractCompanies()

    def getTitle(self) -> str:
        try:
            titleElement = self.soup.find(class_="ArticleHeader-headline")

            if titleElement == None:
                return self.soup.find(class_="LiveBlogHeader-headline").text

            return titleElement.text
        except:
            raise AttributeError("Not valid artical")

    def getPublishTime(self) -> datetime:
        publishTime = self.soup.find('time').text   
        time_parts = publishTime.split(' ', 1)

        timeString = time_parts[1].upper()


        return StringToDatetime(timeString).getDatetime()


    def getContent(self) -> str:
        textContainers = self.soup.find_all(class_="group")
        articalText = ""

        for textContainer in textContainers:
            articalText += textContainer.text

        return articalText

    def extractCompanies(self):
        doc = nlp(self.content)
        companies = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        return list(set(companies))

    def export(self, csvFile="stockData.csv"):
        if self.doesFileExist(csvFile):
            self.writeHeader(csvFile)

        for company in self.releventCompanies:
            history = self.getStockHistory(company)
            if history != None:
                with open(csvFile, "a", newline="") as file:
                    csvWriter = csv.writer(file)
                    csvWriter.writerow([history.getCompanysTicker(), self.content, history["Open"], history["Close"]])
    
    def doesFileExist(self, csvFile):
        return not os.path.exists(csvFile)

    def writeHeader(self, csvFile):        
        with open(csvFile, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["company", "News Artical", "Open", "Close"])

    def getStockHistory(self, company:str) -> StockHistory:
        try:
            return StockHistory(company, self.publishTime)
        except IndexError:
            replacmentDate = self.getReplacementDate(self.publishTime)
            return StockHistory(company, replacmentDate)
        except KeyError:
            return None
    
    def getReplacementDate(self, dt):
        if dt.time() < datetime.datetime.strptime('09:30', '%H:%M').time():
            if self.isItPastTime(self, 10, 30):
                return dt.replace(hour=9, minute=30, second=0, microsecond=0)
        return None
    
    def isItPastTime(self, targetHour, targetMinute):
        current_time = datetime.now().time()
        target_time = datetime.strptime(f"{targetHour}:{targetMinute}", "%H:%M").time()
        return current_time > target_time

    def __str__(self):
        return self.title


if __name__ == "__main__":
    artical = Artical("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    artical.export()
