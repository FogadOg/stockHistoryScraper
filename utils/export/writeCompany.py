import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from utils.export.export import Export
import csv
from scrapers.article import Article

class WriteCompany(Export):
    def __init__(self, article: Article, fileName:str = "stockData.csv"):
        super().__init__(article, fileName)


    def export(self):
        if self._doesFileExist(self.filePath):
            self._writeHeader("company", "News Article", "Close")

        for company in self.article.releventCompanies:
            history = self.article.getStockHistory(company)
            if history != None and self.article.content != "":
                data = history["stockDataForTimeframe"]
                with open(self.filePath, "a", newline="") as file:
                    closeData = '[' +','.join(map(str, data["Close"].values)) + ']'
                    csvWriter = csv.writer(file)
                    csvWriter.writerow([history.tickerSymbol, self.article.content, closeData])


if __name__ == "__main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    WriteCompany(article)

