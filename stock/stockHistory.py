import yfinance as yf
import datetime
import mplfinance as mpf
from stock.stockSymbol import stockSymbole

class StockHistory():
    def __init__(self, companyName: str, articalPublishTime: datetime, timeFrameInHours = 1):
        self.articalPublishTime = articalPublishTime
        self.timeFrameInHours = timeFrameInHours

        tickerSymbol = stockSymbole[companyName]

        self.data = yf.download(tickerSymbol, period='1d', interval='1m')

        self.data.index = self.data.index.tz_convert('America/New_York')

        self.data['Datetime'] = self.data.index

        self.stockDataForTimeframe = self.getStockDataForTimeframe()

    def getStockDataForTimeframe(self):

        startTime = self.articalPublishTime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
        endTime = startTime + datetime.timedelta(hours=self.timeFrameInHours)
        return self.data[(self.data['Datetime'] >= startTime) & (self.data['Datetime'] <= endTime)]


    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True)


if __name__ == "__main__":
    StockHistory('Apple', datetime.datetime(2024, 3, 8, 10, 0, 0)).renderChart()
