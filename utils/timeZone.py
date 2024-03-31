import pytz
from datetime import datetime


class TimeZone():
    def __init__(self, datetimeObject: datetime):
        self.datetimeObject = datetimeObject
    
    def convert(self, timeZone: str) -> datetime:
        targetTimezone = pytz.timezone(timeZone)
        convertedDatetime = self.datetimeObject.astimezone(targetTimezone)

        return convertedDatetime



if __name__ == "__main__":
    time = datetime(2024, 3, 31, 12, 0, 0)
    convert = TimeZone(time).convert("EST")
    print(convert)



