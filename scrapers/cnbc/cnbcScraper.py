import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from scrapers.cnbc.cnbcArticle import CnbcArticle
from scrapers.scraper import Scraper

class CnbcScraper(Scraper):
    def __init__(self, article = CnbcArticle, url = "https://www.cnbc.com/world/?region=world") -> None:
        super().__init__(article, url)


    def _getArticleObject(self):
        articles = self.getAllArticles()
        hrefs = self.findArticleHref(articles)
        return self._createArticleObjects(hrefs)

    def getAllArticles(self):
        articles = []
        parentElements = self.soup.find_all(class_="RiverPlus-riverPlusContainer")

        for parentElement in parentElements:
            for article in parentElement.children:
                if "RiverPlusBreaker-container" not in article.get('class', []):
                    articles.append(article)
        return articles
        
    def findArticleHref(self, articles):
        hrefs = []

        for article in articles:
            aElements = article.select(".RiverHeadline-headline.RiverHeadline-hasThumbnail a")
            
            for element in aElements:
                href = element.get("href")
                if self._isHrefValid(href):
                    hrefs.append(href)

        return hrefs





if __name__ == "__main__":
    scraper = CnbcScraper()