import yfinance as yf
import datetime
import mplfinance as mpf
from .stockSymbol import stockSymbole
from .productCompanyTicker import productsTickers

class StockHistory():
    def __init__(self, companyName: str, articlePublishTime: datetime.datetime, timeFrameInHours = 5):
        self.companyName = companyName.lower()
        self.articlePublishTime = articlePublishTime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
        self.timeFrameInHours = timeFrameInHours

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
                return productsTickers[self.companyName]
            except KeyError:
                raise KeyError(f'"{self.companyName}" company ticker not found')

    def _getStockDataForTimeframe(self):
        marketOpenHour = 9
        marketCloseHour = 14

        if marketOpenHour <= self.articlePublishTime.hour < marketCloseHour:
            endTime = self.articlePublishTime + datetime.timedelta(hours=self.timeFrameInHours)

            data = yf.download(self.tickerSymbol, period='1d', interval='1m', start=self.articlePublishTime, end=endTime)
            return data
        else:
            raise IndexError(f"You're trying to get data for after market closing hours. Your time is {self.articlePublishTime}")

    
    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True, title=self.companyName)


if __name__ == "__main__":
    stockHistory = StockHistory('Apple', datetime.datetime(2024, 3, 11, 12, 30, 0))
    print(stockHistory["Open"])
