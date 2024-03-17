import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from scrapers.cnbc.cnbcArtical import CnbcArtical
from scraper import Scraper

class CnbcScraper(Scraper):
    def __init__(self, artical = CnbcArtical, url = "https://www.cnbc.com/world/?region=world") -> None:
        super().__init__(artical, url)


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




if __name__ == "__main__":
    scraper = CnbcScraper()