import fileHandler
import optionSymbolHandler
import dateHandler

# aDate: the datetime.date on which option data were collected
#
# result: name of the file with data from that date
def getFileName(aDate):
    return "options/options" + getFileNameDateString(aDate) + ".csv"

# aDate: the datetime.date on which option data were collected
#
# result: YYMMDD date string
def getFileNameDateString(aDate):
    return "".join([str(aDate.year - 2000).zfill(2), str(aDate.month).zfill(2), str(aDate.day).zfill(2)])

# aDate: datetime.date when option data were collected
# optionSymbol: string ticker symbol for the option to find
#
# result: last price of the option on the given date
def getLast(aDate, optionSymbol):
    rows = fileHandler.getRowsAfterHeader(getFileName(aDate))
    for row in rows:
        if row[0] == optionSymbol:
            return int(row[4]) / 1000.0
        
# fileName: base name of an option data file
#
# result: a datetime.date object for the day the data were collected
def getDate(fileName):
    year = int(fileName[7:9]) + 2000;
    month = int(fileName[9:11])
    day = int(fileName[11:13])
    return dateHandler.getDate(year, month, day)

# result: a list of all datetime.date objects, representing the dates
# when option data in the "options" directory were created
def getDates():
    result = []
    optionFileNames = fileHandler.getDirContents("options")
    for name in optionFileNames:
        result.append(getDate(name))
    return result

# stockSymbol: the ticker symbol for a stock
# aDate: a datetime.date on which option data were collected
#
# result: a list of ticker symbols for options on the underlying stock
# from the given date of option data collection
def getOptionSymbols(stockSymbol, aDate):
    rows = fileHandler.getRowsAfterHeader(getFileName(aDate))
    result = []
    for row in rows:
        symbol = optionSymbolHandler.getStockSymbol(row[0])
        if symbol == stockSymbol:
            result.append(row[0])
    return result

# aDate: the datetime.date on which option data were collected
#
# result: a list of all expiration dates for options on DJIA stocks from that date
def getExpirationDates(aDate):
    rows = fileHandler.getRowsAfterHeader(getFileName(aDate))
    result = []
    for row in rows:
        expirationDate = optionSymbolHandler.getExpirationDate(row[0])
        if not expirationDate in result:
            result.append(expirationDate)
    return result

if __name__ == '__main__':
    # util.printList(getExpirationDates(dateHandler.getDate(2013, 6, 24)))
    #print getLast(dateHandler.getDate(2013, 6, 24), "AA130720C00004000")
    pass
