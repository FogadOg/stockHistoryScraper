import requests, spacy
from bs4 import BeautifulSoup
nlp = spacy.load("en_core_web_sm")

class Artical():
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")
        
        self.title = self.getTitle()

    
    def getTitle(self) -> str:
        titleElement = self.soup.find(class_="ArticleHeader-headline")
        return titleElement.text



    
    def __str__(self):
        return self.url


