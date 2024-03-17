import requests
from bs4 import BeautifulSoup
from artical import Artical
from utils.export import Export

class Scraper():
    def __init__(self, artical, url) -> None:
        self.articalObject = artical

        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        for articalObject in self._getArticalObject():
            Export(articalObject)

    def _getArticalObject(self):
        articals = self.getAllArticals()
        hrefs = self.findArticalHref(articals)
        return self._createArticalObjects(hrefs)
    
    def _isHrefValid(self, href):
        return "https" in href

    def _createArticalObjects(self, hrefs):
        articalObjects =  []
        for href in hrefs:
            try:
                articalObject = self.articalObject(href)
                articalObjects.append(articalObject)
            except AttributeError:
                pass
        return articalObjects

