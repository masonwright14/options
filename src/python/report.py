from math import sqrt
import dateHandler
import optionData
import interestData
import stockSymbols
import stockData
import optionSymbolHandler
import optionAnalysis
import dividendData
import garch

# aDate: the datetime.date when option data were collected
#
# no return value.
#
# prints a report for each option based on data from the given date.
# double values in the report are printed with 3 digits after the decimal place,
# except for interest rates, which get 4.
# report includes:
# optionSymbol: ticker symbol of each option. only call options are included
# stockSymbol: ticker symbol of the underlying stock for the option
# tradingDaysLeft: number of NYSE trading days before the option expires, from the date
# when the option data were collected
# rContinous: continuously compounded annual interest rate (NOT in percentage form),
# estimated from either LIBOR or Eurodollar futures, whichever expires closer to the option
# expiration date.
# dividends: present value on aDate in dollars of any dividends to have their ex dividend date from aDate to the expiration date
# of the call option.
# blackScholes: Black-Scholes-Merton model value of the option, based on 1 year historical volatility of the underlying
# blackScholesDiv: Black-Scholes model value, with correction for dividends to be paid before expiration
# blackScholesDivAmer: Black-Scholes model value, with correction for dividends and for possible early exercise of the call,
# using the simplification of taking the max of the actual expiration value and the value that results when treating 
# the last ex dividend date as the expiration date
# blackScholesDivGarch: Black-Scholes model value, with correction for dividends and using the GARCH(1,1) estimate of volatility
# instead of the exact historical volatility over the past year
# lastOptionPrice: last price in dollars of the option that day
# strikePrice: strike price of the option 
# lastStockPrice: last price in dollars of the underlying that day
# volHist: historical volatility of the log rate of return of the underlying. NOT volatility of the stock price,
# but volatility of the log rate of return, as used in the Black-Scholes model.
# volGarch: GARCH(1,1) estimate of the volatility, based on the previous year of stock prices.
# volImpliedWithDivAmer: implied volatility of the log rate of return of the underlying, from the Black-Scholes model,
# with the dividend correction, and the early exercise approximation.
# implied volatility is estimated to within 0.001 tolerance with binary search. a result of under about 0.002
# or above 1.98 indicates an unmeasurable implied volatility.
# exp3Yr: expected value of the call option at expiration, based on past 3 years of stock price movements
# over a window equal to the number of trading days to maturity. calculated as the e^(-rt) * mean(x * (xi/xj) - k)+,
# where i - j = days to maturity, for all i in past 3 years; x = stock price at aDate, k = strike price, t = years to maturity.
def printReport(aDate):
    fileName = "reports/report" + "".join([str(aDate.year - 2000).zfill(2), str(aDate.month).zfill(2), str(aDate.day).zfill(2)]) + ".csv"    
    outfile = open(fileName, 'w')
    
    header = "optionSymbol,stockSymbol,tradingDaysLeft,rContinous,dividends,blackScholes,blackScholesDiv,blackScholesDivAmer,blackScholesDivGarch,lastOptionPrice,strikePrice,lastStockPrice,volHist,volGarch,volImpliedWithDivAmer,exVal3Yr"
    outfile.write(header + '\n')
    
    expDates = optionData.getExpirationDates(aDate)
    expDateToR = {}
    for d in expDates:
        expDateToR[d] = interestData.continuousInterest(aDate, d)
    stocks = stockSymbols.getDjiaSymbols()
    for symbol in stocks:
        stockPrice = stockData.getMostRecentClose(symbol, aDate)
        volatility = stockData.getLastYearSigma(symbol, aDate)
        optionSymbols = optionData.getOptionSymbols(symbol, aDate)
        
        lastYearPrices = stockData.getLastYearClosingPrices(symbol, aDate)
        garchParams = garch.myNaiveGarchParams(lastYearPrices)
        expDateToGarchSigma = {}
        
        for option in optionSymbols:
            if not optionSymbolHandler.isCall(option):
                continue
            expDate = optionSymbolHandler.getExpirationDate(option)
            tradingDaysLeft = dateHandler.tradingDaysBetween(expDate, aDate)
            if expDate < aDate or tradingDaysLeft == 0:
                continue
            if expDate not in expDateToGarchSigma:
                expDateToGarchSigma[expDate] = sqrt(garch.garchAverage(garchParams[0], garchParams[1], garchParams[2], lastYearPrices, tradingDaysLeft))
            strike = optionSymbolHandler.getStrikeInDollars(option)
            r = expDateToR.get(expDate)
            d = dividendData.presentDividendValue(aDate, expDate, symbol, r)
            blackScholes = optionAnalysis.w(stockPrice, strike, r, tradingDaysLeft / 252.0, volatility)
            blackScholesDiv = optionAnalysis.wWithDividends(stockPrice, strike, r, tradingDaysLeft / 252.0, volatility, d)
            blackScholesDivGarch = optionAnalysis.wWithDividends(stockPrice, strike, r, tradingDaysLeft / 252.0, expDateToGarchSigma[expDate], d)
            lastDivDate = dividendData.lastExDividendDate(aDate, expDate, symbol)
            blackScholesDivAmer = blackScholesDiv
            td = None
            d2 = None
            if lastDivDate != None:
                td = dateHandler.tradingDaysBetween(lastDivDate, aDate)
                d2 = dividendData.presentDividendValue(aDate, dateHandler.dayBefore(lastDivDate), symbol, r)
                if (d2 == d):
                    print "error: " + option
                if (td > 0):
                    blackScholesDivAmer = optionAnalysis.wWithDividendsAmerican(stockPrice, strike, r, td / 252.0, tradingDaysLeft / 252.0, volatility, d, d2)
            lastOptionPrice = optionData.getLast(aDate, option)
            impliedVol = "N/A"
            if lastOptionPrice > 0:
                if lastDivDate != None:
                    if (td > 0):
                        impliedVol = optionAnalysis.impliedSigmaWithDividendAmerican(lastOptionPrice, stockPrice, strike, r, td / 252.0, tradingDaysLeft / 252.0, d, d2)
                    else:
                        impliedVol = optionAnalysis.impliedSigmaWithDividend(lastOptionPrice, stockPrice, strike, r, tradingDaysLeft / 252.0, d)
                else:
                    impliedVol = optionAnalysis.impliedSigmaWithDividend(lastOptionPrice, stockPrice, strike, r, tradingDaysLeft / 252.0, d)
            exp3Yr = stockData.getExpectedFinalIntrinsicValue2(option, aDate, r)
            impliedVolStr = "N/A"
            if (impliedVol != "N/A"):
                impliedVolStr = "%.3f" % impliedVol
            outfile.write("".join([option, ",", symbol, ",",str(tradingDaysLeft), ",", "%.4f" % r, ",", "%.3f" % d, ",", "%.3f" % blackScholes, ",", "%.3f" % blackScholesDiv, ",", "%.3f" % blackScholesDivAmer, ",", "%.3f" % blackScholesDivGarch, ",", str(lastOptionPrice), ",", str(strike), ",", str(stockPrice), ",", "%.3f" % volatility, ",", "%.3f" % expDateToGarchSigma[expDate], ",", impliedVolStr, ",", "%.3f" % exp3Yr]) + '\n')
    outfile.close()
    
def printKurtosisReport():
    stocks = stockSymbols.getDjiaSymbols()
    header = "stockSymbol,excessKurtosis"
    print header
    for symbol in stocks:
        print symbol + "," + str(stockData.excessStockKurtosis(symbol))
    
# prints report for all option data dates in the "options" directory. takes several minutes to complete.
def printAllReports():
    dates = optionData.getDates()
    for date in dates:
        printReport(date)
        print "Done with report: " + str(date)

# aDate: a datetime.date, through which reports have already been printed
#
# prints report for all option data dates in the "options" directory that are AFTER aDate
def printReportsAfter(aDate):
    dates = optionData.getDates()
    for date in dates:
        if date > aDate:
            printReport(date)
            print "Done with report: " + str(date)

if __name__ == '__main__':
    #printReport(dateHandler.getDate(2013, 6, 24))
    #printReportsAfter(dateHandler.getDate(2013, 7, 17))
    printAllReports()
    #printKurtosisReport()
    pass
