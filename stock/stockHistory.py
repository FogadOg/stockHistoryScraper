import yfinance as yf
import datetime
import mplfinance as mpf
from .stockSymbol import stockSymbole

class StockHistory():
    def __init__(self, companyName: str, articalPublishTime: datetime.datetime, timeFrameInHours = 1):
        self.companyName = companyName.lower()
        self.articalPublishTime = articalPublishTime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
        self.timeFrameInHours = timeFrameInHours

        tickerSymbol = self.getCompanysTicker()

        self.data = yf.download(tickerSymbol, period='1d', interval='1m')

        self.data.index = self.data.index.tz_convert('America/New_York')

        self.data['Datetime'] = self.data.index

        self.stockDataForTimeframe = self.getStockDataForTimeframe()
        print("stockDataForTimeframe: ",self.stockDataForTimeframe)

    def getCompanysTicker(self):
        try:
            return stockSymbole[self.companyName]
        except KeyError:
            print("cant find: ",self.companyName)
            raise KeyError("company not found in dictonary")


    def getStockDataForTimeframe(self):
        if self.articalPublishTime.hour<15:
            endTime = self.articalPublishTime + datetime.timedelta(hours=self.timeFrameInHours)
            return self.data[(self.data['Datetime'] >= self.articalPublishTime) & (self.data['Datetime'] <= endTime)]
        
        raise IndexError(f"youre trying to get date for after closing times. your time is {self.articalPublishTime}")

    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True, title=self.companyName)


if __name__ == "__main__":
    StockHistory('Apple', datetime.datetime(2024, 3, 8, 14, 30, 0)).renderChart()
