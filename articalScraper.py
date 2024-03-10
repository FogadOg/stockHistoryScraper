import re, spacy, requests
from bs4 import BeautifulSoup
from artical import Artical
nlp = spacy.load("enCore_web_sm")

class ArticalScraper():
    def __init__(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")





        




