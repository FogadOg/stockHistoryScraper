import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from utils.export.export import Export
import csv
from scrapers.article import Article

class WriteArticle(Export):
    def __init__(self, article: Article, fileName:str = "articleData"):
        super().__init__(article, fileName)


    def export(self):
        if self._doesFileExist(self.filePath):
            self._writeHeader("Article Title", "News Article", "Publish Date")

        if self.article.content != "":
            with open(self.filePath, "a", newline="") as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow([self.article.title, self.article.content, self.article.publishTime])
    



if __name__ == "__main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")
    WriteArticle(article)

