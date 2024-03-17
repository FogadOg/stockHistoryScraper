from scraper import Scraper

subclasses = Scraper.__subclasses__()

instances = [cls() for cls in subclasses]

print(instances)