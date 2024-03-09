import yfinance as yf
import datetime
import mplfinance as mpf
from stringToDatetime import StringToDatetime
from stockSymbol import stockSymbole

class StockHistory():
    def __init__(self, companyName, articalPublishTimeString, timeFrameInHours = 1):
        self.articalPublishTimeString = articalPublishTimeString
        self.timeFrameInHours = timeFrameInHours

        tickerSymbol = stockSymbole[companyName]

        self.data = yf.download(tickerSymbol, period='1d', interval='1m')

        self.data.index = self.data.index.tz_convert('America/New_York')

        self.data['Datetime'] = self.data.index

        self.stockDataForTimeframe = self.getStockDataForTimeframe()

    def getStockDataForTimeframe(self):
        articalPublishTime = StringToDatetime(self.articalPublishTimeString).getDatetime()

        startTime = articalPublishTime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-5)))
        endTime = startTime + datetime.timedelta(hours=self.timeFrameInHours)
        return self.data[(self.data['Datetime'] >= startTime) & (self.data['Datetime'] <= endTime)]


    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True)


if __name__ == "__main__":
    StockHistory('Apple', "FRI, MAR 8 202410:00 AM EST").renderChart()
