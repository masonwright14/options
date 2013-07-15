import fileHandler
import dateHandler
import optionAnalysis

# stockSymbol: a String that represents the ticker symbol of a stock
#
# result: the file name to use to get the stock's data
def getFileName(stockSymbol):
    return "stockPrices/" + stockSymbol + ".csv"

# stockSymbol: a String that represents the ticker symbol of a stock
#
# result: actual historical volatility for the 252 most recent trading days
# before today in our records
def getMostRecentYearSigma(stockSymbol):
    return getLastYearSigma(stockSymbol, dateHandler.today())

# stockSymbol: a String that represents the ticker symbol of a stock
#
# result: actual historical volatility for the 252 most recent trading days
# before lastDate in our records
def getLastYearSigma(stockSymbol, lastDate):
    return optionAnalysis.sigma(getLastYearClosingPrices(stockSymbol, lastDate))

# stockSymbol: a String that represents the ticker symbol of a stock
#
# result: a list of closing prices in cents, as integers, starting
# from the 252nd date before lastDate, and continuing in chronological order to
# on or just before lastDate. Assumes a 252 trading day year.
def getLastYearClosingPrices(stockSymbol, lastDate):
    return getClosingPrices(stockSymbol, lastDate, 252)

# stockSymbol:  a String that represents the ticker symbol of a stock
# lastDate: a datetime.date object. the closing prices returned will
# be on or before this date
# howMany: how many closing prices to return
#
# result: a list of closing prices in cents, as integers, starting
# from the howManyth date before lastDate, and continuing in chronological order to
# on or just before lastDate
def getClosingPrices(stockSymbol, lastDate, howMany):
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
        result.append(float(rows[i][4]))
        i -= 1
    return result
