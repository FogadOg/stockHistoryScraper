import requests
from bs4 import BeautifulSoup
from utils.export import Export

class Scraper(object):
    def __init__(self, article, url) -> None:
        self.articleObject = article

        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        for articleObject in self._getArticleObject():
            Export(articleObject)

    def _getArticleObject(self):
        articles = self.getAllArticles()
        hrefs = self.findArticleHref(articles)
        return self._createArticleObjects(hrefs)
    
    def _isHrefValid(self, href):
        return "https" in href

    def _createArticleObjects(self, hrefs):
        articleObjects =  []
        for href in hrefs:
            try:
                articleObject = self.articleObject(href)
                articleObjects.append(articleObject)
            except AttributeError:
                pass
        return articleObjects

