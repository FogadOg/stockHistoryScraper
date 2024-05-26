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
            csvWriter.writerow(args)
    
    def csvToDict(self) -> dict:
        with open(self.filePath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            titleDict = {}
            
            for row in reader:
                title = row.pop("Article Title")
                titleDict[title] = row
                    
        return titleDict






