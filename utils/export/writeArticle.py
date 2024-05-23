import sys
import os
import csv
from scrapers.article import Article

class WriteArticle():
    def __init__(self, article: Article, fileName:str = "data"):
        self.article = article
        self.filePath = f"{fileName}.csv"
        self.export()

    def export(self):
        if self._doesFileExist(self.filePath):
            self._writeHeader(self.filePath)

        for company in self.article.releventCompanies:
            if self.article.content != "":
                with open(self.filePath, "a", newline="") as file:
                    csvWriter = csv.writer(file)
                    csvWriter.writerow([self.article.title, self.article.content, self.article.publishTime])
    
    def _doesFileExist(self, csvFile):
        return not os.path.exists(csvFile)

    def _writeHeader(self, csvFile):        
        with open(csvFile, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["Article Title", "News Article", "Publish Date"])


if __name__ == "__main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    WriteArticle(article)

