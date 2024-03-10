import requests
from bs4 import BeautifulSoup
from artical import Artical

class ArticalScraper():
    def __init__(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articals = self.getAllArticals(soup, "RiverPlus-riverPlusContainer")
    
        hrefs = self.findArticalHref(articals, ".RiverHeadline-headline.RiverHeadline-hasThumbnail a")
        # print("-----------hrefs: ",hrefs)

        articalObjects = self.createArticalObjects(hrefs)

        for articalObject in articalObjects:
            print(articalObject)


    def getAllArticals(self, soup, parentElementClass):
        articals = []

        parentElements= soup.find_all(class_=parentElementClass)

        for parentElement in parentElements:
            for artical in parentElement.children:
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
            articalObject = Artical(href)
            articalObjects.append(articalObject)
        return articalObjects

