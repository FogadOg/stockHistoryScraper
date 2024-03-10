import requests, spacy
from bs4 import BeautifulSoup
nlp = spacy.load("en_core_web_sm")

class Artical():
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")
        
        self.title = self.getTitle()
        self.content = self.getContent()

        self.releventCompanies = self.extractCompanies()
    
    def getTitle(self) -> str:
        titleElement = self.soup.find(class_="ArticleHeader-headline")
        return titleElement.text

    def getContent(self) -> str:
        textContainers = self.soup.find_all(class_="group")
        articalText = ""

        for textContainer in textContainers:
            articalText += textContainer.text
        
        return articalText
    
    def extractCompanies(self):
        doc = nlp(self.content)
        companies = [entity.text for entity in doc.ents if entity.label_ == "ORG"]
        return list(set(companies))
    
    def __str__(self):
        return self.url


