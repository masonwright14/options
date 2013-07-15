import stockData
import util
import dateHandler

if __name__ == '__main__':
    #print excessDailyDollarReturn2(100, 100, 0.5, 100, 0.02, 0.2)
    #util.printList(fileHandler.getLines("stockPrices/XOM.csv"))
    #print dateHandler.getStockDate("1950-01-11")
    #print stockSymbols.getDjiaSymbols()
    util.printList(stockData.getClosingPricesInCents("MSFT", dateHandler.getDate(2013, 6, 1), 50))
    pass
