from datetime import datetime, timedelta


class StringToDatetime:
    def __init__(self, inputString: str) -> None:
        self.inputString = inputString

        self.month_map = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }

    def getDatetimeCnbc(self) -> datetime:
        month, day, year, hour, minute, amPm, timeZone = self._getDate()
        if amPm == "PM" and hour != 12:
            hour += 12

        return datetime(year, month, day, hour, minute), timeZone
    
    def getDatetimeYahoo(self) -> str:
        dateFormat = "%B %d, %Y at %I:%M %p"
        parseddate = datetime.strptime(self.inputString, dateFormat)
        return parseddate
    

    def _getDate(self) -> tuple[int, int, int, int, int, str]:
        parts = self.inputString.split()

        month = self.month_map[parts[1]]
        day = int(parts[2])
        year_and_time = parts[3]
        year = int(year_and_time[:4])
        time = year_and_time[4:]
        timeParts = time.split(":")
        hour = int(timeParts[0])
        minute = int(timeParts[1])
        amPm = parts[4]
        timeZone = parts[5]

        return month, day, year, hour, minute, amPm, timeZone