import dateHandler

# optionSymbol: the symbol of an exchange traded option
#
# result: the stock symbol of the option, assuming it has not had punctuation removed
# to get to the option symbol prefix
def getStockSymbol(optionSymbol):
    firstDigitIndex = 0
    for c in optionSymbol:
        if ("".join(c)).isdigit():
            firstDigitIndex = optionSymbol.find(c)
            break
    return optionSymbol[:firstDigitIndex]

# optionSymbol: the symbol of an exchange traded option
#
# result: true if the option is a call option, false if it is a put option
def isCall(optionSymbol):
    firstDigitIndex = 0
    for c in optionSymbol:
        if ("".join(c)).isdigit():
            firstDigitIndex = optionSymbol.find(c)
            break
    indicatorIndex = optionSymbol.find("C", firstDigitIndex)
    return indicatorIndex > 0

# optionSymbol: the symbol of an exchange traded option
#
# result: strike price of the option in dollars
def getStrikeInDollars(optionSymbol):
    i = len(optionSymbol) - 1
    while not (("".join(optionSymbol[i])).isalpha()):
        i -= 1
    return float(optionSymbol[i + 1:]) / 1000

# optionSymbol: the symbol of an exchange traded option
# startDate: the date to start counting from
#
# result: number of trading days on the NYSE including startDate,
# up to but EXCLUDING the expiration date
def tradingDaysLeft(optionSymbol, startDate):
    return dateHandler.tradingDaysBetween(getExpirationDate(optionSymbol), startDate)

# optionSymbol: the symbol of an exchange traded option
#
# result: date object representing the expiration date of the option
def getExpirationDate(optionSymbol):
    firstDigitIndex = 0
    for c in optionSymbol:
        if ("".join(c)).isdigit():
            firstDigitIndex = optionSymbol.find(c)
            break
    dateString = optionSymbol[firstDigitIndex:firstDigitIndex + 6]
    year = int(dateString[:2]) + 2000
    month = int(dateString[2:4])
    day = int(dateString[4:])
    return dateHandler.getDate(year, month, day)

if __name__ == '__main__':
    #print getExpirationDate("ABC120601C00151500")
    pass
