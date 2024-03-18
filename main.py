from scrapers.scraper import Scraper
from scrapers.cnbc.cnbcScraper import CnbcScraper

subclasses = Scraper.__subclasses__()

instances = [cls() for cls in subclasses]

print(instances)