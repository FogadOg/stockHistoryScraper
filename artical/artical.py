import requests, spacy, csv, datetime, sys, os
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
        self.publishTime = self.getPublishTime()
        self.content = self.getContent()

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
    
    def export(self, csvFile="mlData.csv"):
        self.writeHeader(csvFile)

        for company in self.releventCompanies:
            with open(csvFile, "a", newline="") as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow([company, "Stock"])

    def writeHeader(self, csvFile):        
        with open(csvFile, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["News Artical", "Stock"])

    def getStockHistory(self, company):
        StockHistory(company, self.publishTime)

    def __str__(self):
        return self.title


if __name__ == "__main__":
    artical = Artical("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    print(artical.publishTime)