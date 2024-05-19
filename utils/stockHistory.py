import  sys, os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(currentDir, '../'))
sys.path.append(parentDir)


import yfinance as yf
import datetime
import mplfinance as mpf
from utils.dependencies.stockSymbol import stockSymbole
from utils.dependencies.productTicker import productTicker

class StockHistory():
    def __init__(self, companyName: str, publishTime: datetime.datetime, timeFrameInDays: int = 1):
        self.companyName = companyName.lower()
        self.publishTime = publishTime
        self.timeFrameInDays = timeFrameInDays

        self.tickerSymbol = self._getCompanysTicker()

        self.stockDataForTimeframe = self._getStockDataForTimeframe()
        if len(self.stockDataForTimeframe) == 0:
            raise KeyError(f'Ticker for company "{self.companyName}" not found might be due to delisting.')



    def __getitem__(self, attribute):
        attributeData = self.stockDataForTimeframe[attribute]
        return attributeData.values

    def _getCompanysTicker(self):
        try:
            return stockSymbole[self.companyName]
        except KeyError:
            try:
                return productTicker[self.companyName]
            except KeyError:
                raise KeyError(f'"{self.companyName}" company ticker not found')

    def _getStockDataForTimeframe(self):
        if self.isFriday():
            days = self.timeFrameInDays + 2
            endTime = self.publishTime + datetime.timedelta(days=days)
        else:
            endTime = self.publishTime + datetime.timedelta(days=self.timeFrameInDays)
        
        data = yf.download(self.tickerSymbol, period='1d', interval='1m', start=self.publishTime, end=endTime)
        return data
    
    
    def isFriday(self) -> bool:
        return self.publishTime.weekday() == 4
    
    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True, title=self.companyName)


if __name__ == "__main__":
    stockHistory = StockHistory('Apple', datetime.datetime(2024, 5, 7, 9, 30, 0))
    print(stockHistory.stockDataForTimeframe)
