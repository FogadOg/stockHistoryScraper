from datetime import datetime, timedelta

# Define the input string
class StringToDatetime:
    def __init__(self, inputString):
        self.inputString = inputString

        self.month_map = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }

    def getDatetime(self):
        month, day, year, hour, minute, amPm = self.getDate()
        if amPm == "PM" and hour != 12:
            hour += 12

        return datetime(year, month, day, hour, minute)
    

    def getDate(self):
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

        return month, day, year, hour, minute, amPm