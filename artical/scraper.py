import requests
from bs4 import BeautifulSoup
from artical import Artical
from utils.export import Export

class Scraper():
    def __init__(self, url) -> None:
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")

        for articalObject in self._getArticalObject():
            Export(articalObject)

    def _getArticalObject(self):
        articals = self.getAllArticals()
        hrefs = self.findArticalHref(articals)
        return self._createArticalObjects(hrefs)

    def getAllArticals(self):
        articals = []
        parentElements = self.soup.find_all(class_="RiverPlus-riverPlusContainer")

        for parentElement in parentElements:
            for artical in parentElement.children:
                if "RiverPlusBreaker-container" not in artical.get('class', []):
                    articals.append(artical)
        return articals
        
    def findArticalHref(self, articals):
        hrefs = []

        for artical in articals:
            aElements = artical.select(".RiverHeadline-headline.RiverHeadline-hasThumbnail a")
            
            for element in aElements:
                href = element.get("href")
                if self._isHrefValid(href):
                    hrefs.append(href)

        return hrefs
    
    def _isHrefValid(self, href):
        return "https" in href

    def _createArticalObjects(self, hrefs):
        articalObjects =  []
        for href in hrefs:
            try:
                articalObject = Artical(href)
                articalObjects.append(articalObject)
            except AttributeError:
                pass
        return articalObjects




if __name__ == "__main__":
    scraper = Scraper("https://www.cnbc.com/world/?region=world")