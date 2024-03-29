import sys
import os
import csv
from scrapers.article import Article

class Export():
    def __init__(self, article: Article, fileName:str = "data"):
        self.article = article
        self.filePath = f"{fileName}.csv"
        self.export()

    def export(self, csvFile="stockData.csv"):
        if self._doesFileExist(csvFile):
            self._writeHeader(csvFile)

        for company in self.article.releventCompanies:
            history = self.article.getStockHistory(company)
            if history != None:
                with open(csvFile, "a", newline="") as file:
                    openData = '[' +','.join(map(str, history["Open"])) + ']'
                    closeData = '[' +','.join(map(str, history["Close"])) + ']'
                    csvWriter = csv.writer(file)
                    csvWriter.writerow([history.tickerSymbol, self.article.content, openData, closeData])
    
    def _doesFileExist(self, csvFile):
        return not os.path.exists(csvFile)

    def _writeHeader(self, csvFile):        
        with open(csvFile, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["company", "News Article", "Open", "Close"])


if __name__ == "__main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    Export(article)

