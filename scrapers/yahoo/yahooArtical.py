import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

import datetime
from utils.stringToDatetime import StringToDatetime
from scrapers.artical import Artical




class YahooArtical(Artical):
    def __init__(self, url):
        super().__init__(url)

    def getTitle(self) -> str:
        titleElement = self.soup.find("h1")

        return titleElement.text
    
    def getPublishTime(self) -> datetime:
        publishTime = self.soup.find('time').text

        return StringToDatetime(publishTime).getDatetimeYahoo()


    def getContent(self) -> str:
        textContainers = self.soup.find_all(class_="caas-body")
        content = ""
        for container in textContainers:
            content += container.text.strip()
        return content


if __name__ == "__main__":
    artical = YahooArtical("https://finance.yahoo.com/news/want-leave-assets-heirs-irs-105000681.html")
