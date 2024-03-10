import re, spacy, requests
from bs4 import BeautifulSoup
from artical import Artical
nlp = spacy.load("enCore_web_sm")

class ArticalScraper():
    def __init__(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")




    def createArticalObjects(self, hrefs):
        articalObjects =  []
        for href in hrefs:
            articalObject = Artical(href)
            articalObjects.append(articalObject)
        return articalObjects

        

    def extractCompanies(self, articalTitle):
        doc = nlp(articalTitle)
        companies = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        return companies


