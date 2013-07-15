import fileHandler
import dateHandler

# stockSymbol: a String that represents the ticker symbol of a stock
#
# result: the file name to use to get the stock's data
def getFileName(stockSymbol):
    return "stockPrices/" + stockSymbol + ".csv"

# stockSymbol:  a String that represents the ticker symbol of a stock
# lastDate: a datetime.date object. the closing prices returned will
# be on or before this date
# howMany: how many closing prices to return
#
# result: a list of closing prices in cents, as integers, starting
# from the howManyth date before lastDate, and continuing in chronological order to
# on or just before lastDate
def getClosingPricesInCents(stockSymbol, lastDate, howMany):
    rows = fileHandler.getRowsAfterHeader(getFileName(stockSymbol))
    
    lowestIndex = -1
    i = 0
    for row in rows:
        currentDate = dateHandler.getStockDate(row[0])
        if currentDate <= lastDate:
            lowestIndex = i
            break
        i += 1
    if lowestIndex == -1:
        return None
    
    highestIndex = lowestIndex + howMany - 1;
    
    i = highestIndex
    result = []
    while i >= lowestIndex:
        result.append(int(float(rows[i][4]) * 100))
        i -= 1
    return result
