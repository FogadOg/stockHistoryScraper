import os, csv
from scrapers.article import Article



class Export():
    def __init__(self, article: Article, fileName:str = "articleData"):
        self.article = article
        self.filePath = f"{fileName}.csv"
        self.export()

    def _doesFileExist(self, csvFile):
        return not os.path.exists(csvFile)

    def _writeHeader(self, *args):        
        with open(self.filePath, "w", newline="") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(*args)




