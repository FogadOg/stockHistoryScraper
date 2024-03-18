import sys
import os
import csv
from scrapers.artical import Artical

class Export():
    def __init__(self, artical: Artical, fileName:str = "data"):
        self.artical = artical
        self.filePath = f"{fileName}.csv"
        self.export()

    def export(self, csvFile="stockData.csv"):
        if self._doesFileExist(csvFile):
            self._writeHeader(csvFile)

        for company in self.artical.releventCompanies:
            history = self.artical.getStockHistory(company)
            if history != None:
                with open(csvFile, "a", newline="") as file:
                    csvWriter = csv.writer(file)
                    csvWriter.writerow([history.tickerSymbol, self.artical.content, history["Open"], history["Close"]])
    
    def _doesFileExist(self, csvFile):
        return not os.path.exists(csvFile)

    def _writeHeader(self, csvFile):        
        with open(csvFile, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["company", "News Artical", "Open", "Close"])


if __name__ == "__main__":
    artical = Artical("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    Export(artical)

