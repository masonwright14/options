import dateHandler
import optionData
import interestData
import stockSymbols
import stockData
import optionSymbolHandler
import optionAnalysis

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
# blackScholes: Black-Scholes-Merton model value of the option, based on 1 year historical volatility of the underlying
# lastOptionPrice: last price in dollars of the option that day
# strikePrice: strike price of the option 
# lastStockPrice: last price in dollars of the underlying that day
# volHist: historical volatility of the log rate of return of the underlying. NOT volatility of the stock price,
# but volatility of the log rate of return, as used in the Black-Scholes model.
# volImplied: implied volatility of the log rate of return of the underlying, from the Black-Scholes model.
# implied volatility is estimated to within 0.001 tolerance with binary search. a result of under about 0.002
# or above 1.98 indicates an unmeasurable implied volatility.
def printReport(aDate):
    fileName = "reports/report" + "".join([str(aDate.year - 2000).zfill(2), str(aDate.month).zfill(2), str(aDate.day).zfill(2)]) + ".csv"    
    outfile = open(fileName, 'w')
    
    header = "optionSymbol,stockSymbol,tradingDaysLeft,rContinous,blackScholes,lastOptionPrice,strikePrice,lastStockPrice,volHist,volImplied"
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
        for option in optionSymbols:
            if not optionSymbolHandler.isCall(option):
                continue
            expDate = optionSymbolHandler.getExpirationDate(option)
            tradingDaysLeft = dateHandler.daysBetween(expDate, aDate)
            if expDate < aDate or tradingDaysLeft == 0:
                continue
            strike = optionSymbolHandler.getStrikeInDollars(option)
            r = expDateToR.get(expDate)
            blackScholes = optionAnalysis.w(stockPrice, strike, r, tradingDaysLeft / 252.0, volatility)
            lastOptionPrice = optionData.getLast(aDate, option)
            impliedVol = "N/A"
            if lastOptionPrice > 0:
                impliedVol = optionAnalysis.impliedSigma(lastOptionPrice, stockPrice, strike, r, tradingDaysLeft / 252.0)
            outfile.write("".join([option, ",", symbol, ",",str(tradingDaysLeft), ",", "%.4f" % r, ",", "%.3f" % blackScholes, ",", str(lastOptionPrice), ",", str(strike), ",", str(stockPrice), ",", "%.3f" % volatility, ",", "%.3f" % impliedVol]) + '\n')
    outfile.close()
    
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
    #printReportsAfter(dateHandler.getDate(2013, 7, 16))
    printAllReports()
    pass
