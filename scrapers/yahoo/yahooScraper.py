import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from scrapers.yahoo.yahooArtical import YahooArtical
from scrapers.scraper import Scraper

class YahooScraper(Scraper):
    def __init__(self, artical = YahooArtical, url = "https://finance.yahoo.com") -> None:
        super().__init__(artical, url)


    def _getArticalObject(self):
        articals = self.getAllArticals()
        hrefs = self.findArticalHref(articals)
        return self._createArticalObjects(hrefs)

    def getAllArticals(self):
        articals = []
        parentElements = self.soup.find_all(class_="My(0) P(0) Wow(bw) Ov(h)")

        for parentElement in parentElements:
            for artical in parentElement.children:
                articals.append(artical)
        return articals
        
    def findArticalHref(self, articals):
        hrefs = []
        
        for artical in articals:
            try:
                aElement = artical.find('a', class_='js-content-viewer')

                href = aElement["href"]
                href = "https://finance.yahoo.com"+href

                if self._isHrefValid(href):
                    hrefs.append(href)
            except:
                pass

        return hrefs





if __name__ == "__main__":
    scraper = YahooScraper()