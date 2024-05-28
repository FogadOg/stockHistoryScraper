from scrapers.scraper import Scraper
from scrapers.cnbc.cnbcScraper import CnbcScraper
# from scrapers.yahoo.yahooScraper import YahooScraper
import csv
from utils.export.exportArticle import ExportArticle
from utils.export.writeCompany import WriteCompany

class Main():
    def __init__(self, createDataset: bool = False) -> None:

        if createDataset == False:
            self.scrapeArticals()
        else:        
            self.createDataset()  
    
    def scrapeArticals(self) -> None:
        subclasses = Scraper.__subclasses__()
        instances = [cls() for cls in subclasses]

        print(instances)
    
    def createDataset(self):
        with open("articleData.csv", mode="r") as file:
            csvFile = csv.reader(file)
            next(csvFile)
            for line in csvFile:
                try:
                    article = ExportArticle(*line)
                    WriteCompany(article)
                except Exception as e:
                    print("ERROR: ",e)


Main(True)