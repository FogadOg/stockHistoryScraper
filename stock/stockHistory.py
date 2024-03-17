import yfinance as yf
import datetime
import mplfinance as mpf
from stockSymbol import stockSymbole

class StockHistory():
    def __init__(self, companyName: str, articalPublishTime: datetime.datetime, timeFrameInHours = 1):
        self.companyName = companyName.lower()
        self.articalPublishTime = articalPublishTime.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
        self.timeFrameInHours = timeFrameInHours

        self.tickerSymbol = self.getCompanysTicker()

        self.stockDataForTimeframe = self.getStockDataForTimeframe()

    def __getitem__(self, attribute):
        data = self.stockDataForTimeframe.drop(columns=['Datetime'])[[attribute]]
        data.reset_index(drop=True, inplace=True)
        return [value for sublist in data.values.tolist() for value in sublist]

    def getCompanysTicker(self):
        try:
            return stockSymbole[self.companyName]
        except KeyError:
            raise KeyError("company not found in dictonary")

    def getStockDataForTimeframe(self):
        marketOpenHour = 9
        marketCloseHour = 15


        if marketOpenHour <= self.articalPublishTime.hour < marketCloseHour:
            endTime = self.articalPublishTime  + datetime.timedelta(hours=self.timeFrameInHours)

            data = yf.download(self.tickerSymbol, period='1d', interval='1m', start=self.articalPublishTime, end=endTime)
            return data
        raise IndexError(f"You're trying to get data for after market closing hours. Your time is {self.articalPublishTime}")

    def renderChart(self):
        mpf.plot(self.stockDataForTimeframe, type='candle', style='charles', volume=True, title=self.companyName)


if __name__ == "__main__":
    stockHistory = StockHistory('Apple', datetime.datetime(2024, 3, 11, 12, 30, 0))
    print(stockHistory)

