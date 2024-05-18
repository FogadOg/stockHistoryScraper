import pytz
from datetime import datetime


class TimeZone():
    def __init__(self, datetimeObject: datetime | str, localTime: str = "Europe/Paris"):

        if isinstance(datetimeObject, datetime):
            self.datetimeObject = datetimeObject
        else:
            self.datetimeObject = datetime.strptime(datetimeObject, "%Y-%m-%dT%H:%M:%S")

        self.datetimeObject = self.setLocalTime(localTime)

    def setLocalTime(self, localTime):
        try:
            timezone = pytz.timezone(localTime)
            convertedDatetime = self.datetimeObject = timezone.localize(self.datetimeObject)
            return convertedDatetime
        except:
            return self.datetimeObject
    
    def convert(self, timeZone: str = "GMT") -> datetime:
        targetTimezone = pytz.timezone(timeZone)
        convertedDatetime = self.datetimeObject.astimezone(targetTimezone)

        return convertedDatetime

    def __repr__(self) -> str:
        return self.datetimeObject.strftime("%Y-%m-%dT%H:%M:%S")
    



if __name__ == "__main__":
    time = datetime(2024, 3, 31, 17, 0, 0)
    convert = TimeZone(time,"GMT").convert('Europe/Paris')
    print(convert)