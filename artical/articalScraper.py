import requests
from bs4 import BeautifulSoup
from artical import Artical
from utils.export import Export

class ArticalScraper():
    def __init__(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articals = self.getAllArticals(soup, "RiverPlus-riverPlusContainer", "RiverPlusBreaker-container")
    
        hrefs = self.findArticalHref(articals, ".RiverHeadline-headline.RiverHeadline-hasThumbnail a")

        articalObjects = self.createArticalObjects(hrefs)

        for articalObject in articalObjects:
            Export(articalObject)


    def getAllArticals(self, soup, parentElementClass, excludeClass):
        articals = []
        parentElements = soup.find_all(class_=parentElementClass)

        for parentElement in parentElements:
            for artical in parentElement.children:
                if excludeClass not in artical.get('class', []):
                    articals.append(artical)
        return articals
        
    def findArticalHref(self, articals, cssSelector):
        hrefs = []

        for artical in articals:
            aElements = artical.select(cssSelector)
            
            for element in aElements:
                href = element.get("href")
                if self.isHrefValid(href):
                    hrefs.append(href)

        return hrefs
    
    def isHrefValid(self, href):
        return "https" in href

    def createArticalObjects(self, hrefs):
        articalObjects =  []
        for href in hrefs:
            try:
                articalObject = Artical(href)
                articalObjects.append(articalObject)
            except AttributeError:
                pass
        return articalObjects




if __name__ == "__main__":
    scraper = ArticalScraper("https://www.cnbc.com/world/?region=world")