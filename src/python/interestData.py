import fileHandler
import dateHandler
from math import log

liborFileName = "interestRates/libor.csv"

eurodollarFileName = "interestRates/eurodollarFutures.csv"

# startDate: datetime.date representing starting month for LIBOR loan
#
# result: list of datetime.date objects representing dates LIBOR loans could end,
# including only LIBOR rates on file
def liborEndDates(startDate):
    rows = fileHandler.getRowsAfterHeader(liborFileName)
    result = []
    for row in rows:
        currentDate = dateHandler.getInterestDate(row[0])
        if currentDate.month == startDate.month and currentDate.year == startDate.year:
            endDate = dateHandler.endDate(startDate, dateHandler.monthsLength(int(row[1])))
            result.append(endDate)
    return result

# startDate: datetime.date representing starting month for eurodollar future
#
# result: list of datetime.date objects representing dates eurodollar futures could end,
# including only rates on file
def eurodollarEndDates(startDate):
    rows = fileHandler.getRowsAfterHeader(eurodollarFileName)
    result = []
    for row in rows:
        currentDate = dateHandler.getInterestDate(row[0])
        if currentDate.month == startDate.month and currentDate.year == startDate.year:
            endDate = dateHandler.endDate(startDate, dateHandler.monthsLength(int(row[1])))
            result.append(endDate)
    return result

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: datetime.date object representing the LIBOR or eurodollar future
# ending date on file that is closest to endDate, starting on startDate
def closestEndDate(startDate, endDate):
    minDist = float("inf")
    result = None
    for liborDate in liborEndDates(startDate):
        if dateHandler.daysBetween(endDate, liborDate) < minDist:
            minDist = dateHandler.daysBetween(endDate, liborDate)
            result = liborDate
    for eurodollarDate in eurodollarEndDates(startDate):
        if dateHandler.daysBetween(endDate, eurodollarDate) < minDist:
            minDist = dateHandler.daysBetween(endDate, eurodollarDate)
            result = eurodollarDate
    return result

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: True if there is a LIBOR rate on file with these dates, else False
# (may be a eurodollar futures date)
def isLiborDate(startDate, endDate):
    for liborDate in liborEndDates(startDate):
        if liborDate.month == endDate.month and liborDate.year == endDate.year:
            return True
    return False

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: LIBOR interest rate for the given start and end months,
# * 100 to convert from percentage, or -1.0 if none on file
def libor(startDate, futureDate):
    rows = fileHandler.getRowsAfterHeader(liborFileName)
    for row in rows:
        currentDate = dateHandler.getInterestDate(row[0])
        if currentDate.month == startDate.month and currentDate.year == startDate.year:
            endDate = dateHandler.endDate(startDate, dateHandler.monthsLength(int(row[1])))
            if endDate.month == futureDate.month and endDate.year == futureDate.year:
                return float(row[2]) / 100.0
    return -1.0

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: eurodollar future interest rate for the given start and end months,
# * 100 to convert from percentage, or -1.0 if none on file
def eurodollar(startDate, futureDate):
    rows = fileHandler.getRowsAfterHeader(eurodollarFileName)
    for row in rows:
        currentDate = dateHandler.getInterestDate(row[0])
        if currentDate.month == startDate.month and currentDate.year == startDate.year:
            endDate = dateHandler.endDate(startDate, dateHandler.monthsLength(int(row[1])))
            if endDate.month == futureDate.month and endDate.year == futureDate.year:
                return float(row[2]) / 100.0
    return -1.0

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: LIBOR or eurodollar interest from startDate to futureDate,
# whichever has a closer time period on file, * 100 to convert from percentage
def interest(startDate, futureDate):
    endDate = closestEndDate(startDate, futureDate)
    if isLiborDate(startDate, endDate):
        return libor(startDate, endDate)
    else:
        return eurodollar(startDate, endDate)

# startDate: datetime.date representing start month for loan
# endDate: datetime.date representing end month of loan
#
# result: LIBOR or eurodollar interest from startDate to futureDate,
# whichever has a closer time period on file, adjusted to continuous compounding
def continuousInterest(startDate, futureDate):
    return rContinuous(1, interest(startDate, futureDate))
    
# m = times per year compounded. m >= 1
# rm = annual interest with incremental compounding. rm > 0.
#
# result: the continuous interest rate corresponding to annual interest
# rate rm, compounded m times per year
def rContinuous(m, rm):
    return m * log(1 + rm / m)
        
if __name__ == '__main__':
    #print closestEndDate(dateHandler.today(), dateHandler.getDate(2014, 11, 1))
    #print isLiborDate(dateHandler.today(), closestEndDate(dateHandler.today(), dateHandler.getDate(2014, 11, 1)))
    #print eurodollar(dateHandler.today(), dateHandler.getDate(2014, 9, 23))
    #print libor(dateHandler.today(), dateHandler.getDate(2013, 10, 1))
    #print continuousInterest(dateHandler.today(), dateHandler.getDate(2013, 10, 1))
    #print continuousInterest(dateHandler.today(), dateHandler.getDate(2014, 10, 1))
    pass
