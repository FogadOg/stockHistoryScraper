from scrapers.scraper import Scraper
from scrapers.cnbc.cnbcScraper import CnbcScraper
from scrapers.yahoo.yahooScraper import YahooScraper

subclasses = Scraper.__subclasses__()

instances = [cls() for cls in subclasses]

print(instances)