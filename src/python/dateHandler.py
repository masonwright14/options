import datetime
from datetime import timedelta

# stringDate: YYYY-MM-DD
#
# result: a datetime.date object
def getStockDate(stringDate):
    year = int(stringDate[:4])
    month = int(stringDate[5:7])
    day = int(stringDate[8:])
    return datetime.date(year, month, day)

# stringDate: MMDD
#
# result: a datetime.date object
def getInterestDate(stringDate):
    year = int(stringDate[2:4]) + 2000
    month = int(stringDate[:2])
    return datetime.date(year, month, 1)

# stringDate: DDMMYY
#
# result: a datetime.date object
def getDividendDate(stringDate):
    day = int(stringDate[:2])
    month = int(stringDate[2:4])
    year = int(stringDate[4:]) + 2000
    return datetime.date(year, month, day)

# year: int
# month: int
# day: int
#
# result: a datetime.date object
def getDate(year, month, day):
    return datetime.date(year, month, day)

# initialDate: the datetime.date object to start from
#
# result: the datetime.date of the previous day
def dayBefore(initialDate):
    return initialDate - timedelta(days=1)

# result: a datetime.date object
def today():
    return datetime.date.today()

# howMany: the number of months
#
# result: a datetime.timedelta object representing the duration
# of howMany 31-day months
def monthsLength(howMany):
    return timedelta(days=(31 * howMany))

# howMany: the number of days
#
# result: a datetime.timedelta object representing the duration
# of howMany days
def daysLength(howMany):
    return timedelta(days=howMany)

# startDate: the initial datetime.date of the period
# duration: a datetime.timedelta object representing the length of the period
#
# result: the final datetime.date of the period
def endDate(startDate, duration):
    return startDate + duration

# date1: one of two datetime.date objects, not necessarily earlier than date2
# date2: another datetime.date object
#
# result: number of whole days from date1 to date2 (absolute value)
def daysBetween(date1, date2):
    return abs((date2 - date1).days)

# dateList: a list of datetime.date objects
# targetDate: a datetime.date object
#
# result: the datetime.date object from dateList
# nearest in time to targetDate
def nearestDate(dateList, targetDate):
    minDist = float("inf")
    result = None
    for d in dateList:
        if daysBetween(d, targetDate) < minDist:
            minDist = daysBetween(d, targetDate)
            result = d
    return result

# date1: one of two datetime.date objects, not necessarily earlier than date2
# date2: another datetime.date object
#
# result: number of days on which NYSE trading occurred from the earlier date,
# up to but NOT INCLUDING the later date.
def tradingDaysBetween(date1, date2):
    earlier = min(date1, date2)
    later = max(date1, date2)
    result = 0
    while earlier < later:
        if isTradingDay(earlier):
            result += 1
        earlier += datetime.timedelta(days=1)
    return result

# aDate: a datetime.date object
#
# result: True if the NYSE is open on at least part of that day, False otherwise.
# assumes the only NYSE holidays are weekends plus 1/1, 7/4, 12/25,
# MLK Day, President's Day, Memorial Day, Labor Day, and Thanksgiving Day
def isTradingDay(aDate):
    # Saturday or Sunday
    if aDate.weekday() >= 5:
        return False
    # New Year's Day
    if aDate.month == 1 and aDate.day == 1:
        return False
    # 4th of July
    if aDate.month == 7 and aDate.day == 4:
        return False
    # Christmas
    if aDate.month == 12 and aDate.day == 25:
        return False
    # MLK Day, 3rd Monday in January
    if aDate.month == 1 and aDate.weekday() == 1 and aDate.day >= 15 and aDate.day <= 21:
        return False
    # President's Day, 3rd Monday in February
    if aDate.month == 2 and aDate.weekday() == 1 and aDate.day >= 15 and aDate.day <= 21:
        return False
    # Memorial Day, last Monday in May
    if aDate.month == 5 and aDate.weekday() == 1 and aDate.day >= 25:
        return False
    # Labor Day, 1st Monday in September
    if aDate.month == 9 and aDate.weekday() == 1 and aDate.day <= 7:
        return False
    # Thanksgiving, 4th Thursday in November
    if aDate.month == 11 and aDate.weekday() == 4 and aDate.day >= 22 and aDate.day <= 28:
        return False
    # Good Friday (just check table of dates)
    if aDate.month == 3 and aDate.day == 21 and aDate.year == 2008:
        return False
    if aDate.month == 4 and aDate.day == 10 and aDate.year == 2009:
        return False
    if aDate.month == 4 and aDate.day == 2 and aDate.year == 2010:
        return False
    if aDate.month == 4 and aDate.day == 22 and aDate.year == 2011:
        return False
    if aDate.month == 4 and aDate.day == 6 and aDate.year == 2012:
        return False
    if aDate.month == 3 and aDate.day == 29 and aDate.year == 2013:
        return False
    if aDate.month == 4 and aDate.day == 18 and aDate.year == 2014:
        return False
    if aDate.month == 4 and aDate.day == 3 and aDate.year == 2015:
        return False
    return True

if __name__ == '__main__':
    #print tradingDaysBetween(getDate(2013, 1, 1), today())
    #print daysBetween(getDate(2013, 1, 1), today())
    #print tradingDaysBetween(getDate(2013, 1, 1), getDate(2014, 1, 1))
    #print daysBetween(getDate(2013, 1, 1), getDate(2014, 1, 1))
    #print dayBefore(getDate(2013, 1, 1))
    pass
