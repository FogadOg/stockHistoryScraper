import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../../'))
sys.path.append(parentDir)

from datetime import datetime
from utils.stringToDatetime import StringToDatetime
from scrapers.article import Article
from utils.timeZone import TimeZone



class ExportArticle(Article):
    def __init__(self, title: str, content: str, publishTime: str):

        self.title = title
        self.timeZone = 'US/Eastern'
        self.publishTime: datetime = self.convertStringToDatetime(publishTime)
        self.content = content

        self.releventCompanies = self._extractCompanies()
    
    def convertStringToDatetime(self, datetimeStr) -> datetime:
        return datetime.fromisoformat(datetimeStr)

