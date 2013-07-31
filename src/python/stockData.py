from math import exp, log
from random import gauss
import fileHandler
import dateHandler
import optionAnalysis
import optionSymbolHandler
import interestData

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

# stockSymbol: a String that represents the ticker symbol of a stock
# lastDate: a datetime.date object
#
# result: the most recent stock closing price on or before lastDate
def getMostRecentClose(stockSymbol, lastDate):
    return getClosingPrices(stockSymbol, lastDate, 1)[0]

# optionSymbol: the ticker symbol of an option
# currentDate: a datetime.date object, representing the most recent date
# on which historical data should be used
# r: the risk free interest rate, annualized and continuously compounding
#
# result: a prediction of the final intrinsic value of the call option,
# calculated as e^(-r * years to maturity) * mean(current stock price * (xi / xj) - k)+,
# where i - j = trading days to maturity of the option, k = strike price, for all i
# in previous 756 trading days, or 3 years.
def getExpectedFinalIntrinsicValue2(optionSymbol, currentDate, r):
    stockSymbol = optionSymbolHandler.getStockSymbol(optionSymbol)
    dateRange = 756
    daysLeft = dateHandler.daysBetween(currentDate, optionSymbolHandler.getExpirationDate(optionSymbol))
    k = optionSymbolHandler.getStrikeInDollars(optionSymbol)
    return getExpectedFinalIntrinsicValue(stockSymbol, currentDate, dateRange, daysLeft, r, k)

# stockSymbol: ticker symbol of a stock
# currentDate: a datetime.date object, representing the most recent date
# on which historical data should be used
# date range: how many days in the past to examine stock prices
# daysLeft: days to maturity of the option
# r: the risk free interest rate, annualized and continuously compounding
# k: strike price of the call option
#
# result: a prediction of the final intrinsic value of the call option,
# calculated as e^(-r * daysLeft / 252.0) * mean(current stock price * (xi / xj) - k)+,
# where i - j = trading days to maturity of the option, for all i
# in previous dateRange trading days.
def getExpectedFinalIntrinsicValue(stockSymbol, currentDate, dateRange, daysLeft, r, k):
    x = getMostRecentClose(stockSymbol, currentDate)
    prices = getClosingPrices(stockSymbol, currentDate, dateRange)
    mySum = 0
    i = daysLeft
    while i < len(prices):
        mySum += max(0, x * (prices[i] / float(prices[i - daysLeft])) - k)
        i += 1
    meanIntrinsicValue = float(mySum) / (len(prices) - daysLeft)
    return meanIntrinsicValue * exp(-1 * r * daysLeft / 252.0)

def excessStockKurtosis(stockSymbol):
    howMany = 504
    return excessKurtosis(getLogReturnList(getClosingPrices(stockSymbol, dateHandler.today(), howMany)))

#    excess kurtosis = mu4 / sigma4 - 3
#    where:
#    mu4 = E( (X - mu)^4 )
#    sigma4 = ( E( (X - mu)^2 ) )^2
def excessKurtosis(values):
    myMean = sum(values) / len(values)
    mu4 = sum(map(lambda x: (x - myMean) ** 4, values)) / len(values)
    sigma4 = (sum(map(lambda x: (x - myMean) ** 2, values)) / len(values)) ** 2
    return mu4 / sigma4 - 3

# test the excessKurtosis function on a sample of a normal distribution.
# should return a value near 0.
def testExcessKurtosis():
    data = []
    points = 504
    while points > 0:
        data.append(gauss(0, 1))
        points -= 1
    print excessKurtosis(data)
    
def testExcessKurtosisHigh():
    data = []
    points = 504
    while points > 0:
        data.append(gauss(0, 1))
        points -= 1
    points = 100
    while points > 0:
        data.append(0)
        points -= 1
    points = 10
    while points > 0:
        data.append(4)
        points -= 1 
    points = 10  
    while points > 0:
        data.append(-4)
        points -= 1   
    print excessKurtosis(data)

# Y = ln(Xt+1) - ln(Xt)
# prices: list of stock prices in dollars
#
# result: list of log(prices[i] / prices[i-1]) for all i >= 1
def getLogReturnList(prices):
    result = []
    i = 1
    while i < len(prices):
        result.append(log(prices[i]) - log(prices[i - 1]))
        i += 1
    return result

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
        
    # handle stock splits in recent years:
    # KO 2:1 split on 8/13/12
    # halve stock prices before 8/13/12 if before-and-after prices are requested
    if stockSymbol == "KO":
        splitDate = dateHandler.getDate(2012, 8, 13)
        if lastDate >= splitDate and howMany > dateHandler.tradingDaysBetween(splitDate, lastDate) + 3:
            numberToCut = howMany - dateHandler.tradingDaysBetween(splitDate, lastDate) + 3
            i = 0
            while i < numberToCut:
                # 2:1 split
                result[i] = result[i] / 2.0
                i += 1
        
    return result

if __name__ == '__main__':
    #r = interestData.continuousInterest(dateHandler.getDate(2013, 6, 24), dateHandler.getDate(2013, 7, 20))
    #print getExpectedFinalIntrinsicValue2("AXP130720C00067500", dateHandler.getDate(2013, 6, 24), r)
    #testExcessKurtosis()
    #testExcessKurtosisHigh()
    print getClosingPrices("KO", dateHandler.today(), 504)
    #print max(getClosingPrices("KO", dateHandler.today(), 504))
    #print min(getClosingPrices("KO", dateHandler.today(), 504))
    #print excessStockKurtosis("AA")
    pass