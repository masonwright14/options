import datetime

# stringDate: YYYY-MM-DD
#
# result: a datetime.date object
def getStockDate(stringDate):
    year = int(stringDate[:4])
    month = int(stringDate[5:7])
    day = int(stringDate[8:])
    return datetime.date(year, month, day)

# year: int
# month: int
# day: int
#
# result: a datetime.date object
def getDate(year, month, day):
    return datetime.date(year, month, day)

# result: a datetime.date object
def today():
    return datetime.date.today()