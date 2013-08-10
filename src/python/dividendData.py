import fileHandler
import dateHandler
import stockData
from math import exp, log

fileName = "dividends/dividends.csv"

# stockSymbol: NYSE ticker symbol for a stock
#
# result: list of ints, representing cash dividends in thousandths
# of a dollar, in the order they appear in the file (same order as
# getDatesInOrder(stockSymbol)
def getThousandthsInOrder(stockSymbol):
    rows = fileHandler.getRowsAfterHeader(fileName)
    result = []
    for row in rows:
        if row[0] == stockSymbol:
            result.append(int(row[1]))
    return result
    pass

# stockSymbol: NYSE ticker symbol for a stock
#
# result: list of datetime.date objects, representing ex dividend dates
# in the order they appear in the file (same order as getDatesInOrder(stockSymbol)
def getDatesInOrder(stockSymbol):
    rows = fileHandler.getRowsAfterHeader(fileName)
    result = []
    for row in rows:
        if row[0] == stockSymbol:
            result.append(dateHandler.getDividendDate(row[2]))
    return result
    pass

# startDate: the current date for present value discounting purposes,
# also the first date when an ex dividend day would be counted
# endDate: the last date for which an ex dividend day would be counted
# stockSymbol: NYSE ticker symbol for a stock
# r: the risk free interest rate to use in present value analysis
#
# result: the present value in dollars of the dividends to be paid from startDate
# through endDate, evaluated at time startDate. the sum of the payments
# times e^(-r t), where t is the trading days after the startDate / 252.0
# for a certain payment's ex dividend date.
def presentDividendValue(startDate, endDate, stockSymbol, r):
    amountsInThous = getThousandthsInOrder(stockSymbol)
    dates = getDatesInOrder(stockSymbol)
    mySum = 0
    i = 0
    while i < len(amountsInThous):
        if (startDate <= dates[i] and dates[i] <= endDate):
            tradingDaysLeft = dateHandler.tradingDaysBetween(dates[i], startDate)
            mySum += (amountsInThous[i] / 1000.0) * exp(-1.0 * r * tradingDaysLeft / 252.0)
        i += 1
    return mySum

# startDate: the current date for present value discounting purposes,
# also the first date when an ex dividend day would be counted
# endDate: the last date for which an ex dividend day would be counted
# stockSymbol: NYSE ticker symbol for a stock
# r: the risk free interest rate to use in present value analysis
#
# result: the continuously compounding annual interest rate that would
# produce the same return, measured by present value at date startDate,
# as the dividends to be paid between startDate and endDate, when allowed
# to compound from startDate to endDate.
def getYield(startDate, endDate, stockSymbol, r):
    d = presentDividendValue(startDate, endDate, stockSymbol, r)
    dt = dateHandler.tradingDaysBetween(startDate, endDate) / 252.0
    s0 = stockData.getMostRecentClose(stockSymbol, startDate)
    return (log(s0 + d) - log(s0)) / dt

# startDate: the first date that could be returned
# endDate: the last date that could be returned
# stockSymbol: NYSE ticker symbol for a stock
#
# result: the last ex dividend date for the stock from
# startDate to endDate, or None
def lastExDividendDate(startDate, endDate, stockSymbol):
    dates = getDatesInOrder(stockSymbol)
    result = None
    for myDate in dates:
        if (startDate <= myDate and myDate <= endDate):
            if (result == None or myDate > result):
                result = myDate
    return result

if __name__ == '__main__':
    #print getDatesInOrder("AXP")
    #print getThousandthsInOrder("AXP")
    startDate = dateHandler.getDate(2013, 1, 1)
    endDate = dateHandler.getDate(2014, 1, 1)
    print presentDividendValue(startDate, endDate, "KO", 0.02)
    #print lastExDividendDate(startDate, endDate, "AXP")
    print getYield(startDate, endDate, "KO", 0.02)
    pass
