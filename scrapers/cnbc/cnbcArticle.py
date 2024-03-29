import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

import datetime
from utils.stringToDatetime import StringToDatetime
from scrapers.article import Article




class CnbcArticle(Article):
    def __init__(self, url):
        super().__init__(url)

    def getTitle(self) -> str:
        try:
            titleElement = self.soup.find(class_="ArticleHeader-headline")

            if titleElement == None:
                return self.soup.find(class_="LiveBlogHeader-headline").text

            return titleElement.text
        except:
            raise AttributeError("Not valid article")

    def getPublishTime(self) -> datetime:
        publishTime = self.soup.find('time').text   
        time_parts = publishTime.split(' ', 1)

        timeString = time_parts[1].upper()


        return StringToDatetime(timeString).getDatetimeCnbc()

    def getContent(self) -> str:
        textContainers = self.soup.find_all(class_="group")
        articleText = ""

        for textContainer in textContainers:
            articleText += textContainer.text

        return articleText


if __name__ == "__main__":
    article = Article("https://www.cnbc.com/2024/03/07/stock-market-today-live-updates.html")

