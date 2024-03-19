import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from scrapers.yahoo.yahooArticle import YahooArticle
from scrapers.scraper import Scraper

class YahooScraper(Scraper):
    def __init__(self, article = YahooArticle, url = "https://finance.yahoo.com") -> None:
        super().__init__(article, url)


    def _getArticleObject(self):
        articles = self.getAllArticles()
        hrefs = self.findArticleHref(articles)
        return self._createArticleObjects(hrefs)

    def getAllArticles(self):
        articles = []
        parentElements = self.soup.find_all(class_="My(0) P(0) Wow(bw) Ov(h)")

        for parentElement in parentElements:
            for article in parentElement.children:
                articles.append(article)
        return articles
        
    def findArticleHref(self, articles):
        hrefs = []
        
        for article in articles:
            try:
                aElement = article.find('a', class_='js-content-viewer')

                href = aElement["href"]
                href = "https://finance.yahoo.com"+href

                if self._isHrefValid(href):
                    hrefs.append(href)
            except:
                pass

        return hrefs





if __name__ == "__main__":
    scraper = YahooScraper()