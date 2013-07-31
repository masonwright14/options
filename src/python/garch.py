from scipy.optimize import minimize
from math import log, exp, sqrt
import stockData
import dateHandler
import optionAnalysis
import stockSymbols

# omega = scalar parameter for GARCH(1,1)
# alpha = ui^2 coefficient for GARCH(1,1)
# beta = sigma-i^2 coefficient for GARCH(1,1)
# sigma(i)^2 = omega + alpha * u(i-1)^2 + beta * sigma(i-1)^2
# sList: list of stock closing prices as a daily time series
# tradingDays: how many trading days in the future to look
#
# result: average ANNUALIZED sigma^2 expected over the next "tradingDays" period
# in the future after the data in sList. useful for pricing options with tradingDays'
# time to maturity from the present.
#
# result = 252 * (Vl + (V0 - Vl) ( (1 - e^(-a T)) / (aT) ))
def garchAverage(omega, alpha, beta, sList, tradingDays):
    v0 = garchZeroDaily(omega, alpha, beta, sList)
    a = log(1 / (alpha + beta))
    Vl = getVl(omega, alpha, beta)
    return 252.0 * (Vl + ((1 - exp(-1.0 * a *  tradingDays)) / (a *  tradingDays)) * (v0 - Vl))

# omega = scalar parameter for GARCH(1,1)
# alpha = ui^2 coefficient for GARCH(1,1)
# beta = sigma-i^2 coefficient for GARCH(1,1)
# sigma(i)^2 = omega + alpha * u(i-1)^2 + beta * sigma(i-1)^2
# sList: list of stock closing prices as a daily time series
#
# result: GARCH(1,1) prediction for next day's daily sigma^2,
# i.e., for the day after the last price in sList
def garchZeroDaily(omega, alpha, beta, sList):
    x = [omega, alpha, beta]
    uList = getUList(sList)
    vList = getVList(x, uList)
    return vList[len(vList) - 1]

# omega = scalar parameter for GARCH(1,1)
# alpha = ui^2 coefficient for GARCH(1,1)
# beta = sigma-i^2 coefficient for GARCH(1,1)
# sigma(i)^2 = omega + alpha * u(i-1)^2 + beta * sigma(i-1)^2
# sList: list of stock closing prices as a daily time series
# tradingDays: how many trading days in the future to look
#
# result: GARCH(1,1) prediction for next day + tradingDays's daily sigma^2,
# i.e., for the "tradingDays + 1st" day after the last price in sList
# if tradingDays == 0, result is same as for garchZeroDaily.
#
# result = Vl + (alpha + beta)^t (sigma(0)^2 - Vl)
def garchFutureDaily(omega, alpha, beta, sList, tradingDays):
    Vl = getVl(omega, alpha, beta)
    return Vl + ((alpha + beta) ** tradingDays) * (garchZeroDaily(omega, alpha, beta, sList) - Vl)

# sList: list of stock closing prices as a daily time series
#
# result: [omega, alpha, beta], parameters of the GARCH(1,1) model as a list.
# omega = scalar parameter
# alpha = ui^2 coefficient
# beta = sigma-i^2 coefficient
# sigma(i)^2 = omega + alpha * u(i-1)^2 + beta * sigma(i-1)^2
def garchParams(sList):
    # initial guess taken from Hull, chapter 22 on volatility estimation with GARCH(1,1)
    myGuess = [0.000001347, 0.08339, 0.9101]

    # 0 < omega, alpha, beta. alpha < 1, beta < 1
    myBounds = ((0, None), (0, 1), (0, 1))

    # 1 - (alpha + beta) > 0
    myConstraints = ({'type': 'ineq', 'fun': lambda x:  1 - (x[1] + x[2])})

    # sList = list of Si's, 1 <= i <= n
    myArgs = (sList,)

    result = minimize(negativeLikelihood, x0=myGuess, method='COBYLA', constraints=myConstraints, bounds=myBounds, args=myArgs).x
    # make sure parameters are non-negative, even though this should have been a constraint
    if result[0] < 0:
        result[0] = 0
    if result[1] < 0:
        result[1] = 0
    if result[2] < 0:
        result[2] = 0
    # make sure the result is as good as the initial guess, even though this should happen anyway
    if listLikelihood(result, sList) < listLikelihood(myGuess, sList):
        return myGuess
    return result
    
# minimize the negative of likelihood, to maximize likelihood
def negativeLikelihood(x, sList):
    return -1.0 * listLikelihood(x, sList)

# x: [omega, alpha, beta], parameters for GARCH(1,1) as a list.
# sList: list of daily stock closing prices in dollars
#
# result: likelihood score for the parameter set. will be higher
# if the parameters are a better match for sList. uses MLE method,
# taking the sum of the log likelihood function results instead of the
# product of the likelihood function results.
def listLikelihood(x, sList):
    # get list of daily percent changes
    uList = getUList(sList)
    
    # get list of GARCH(1,1) sigma(i)^2 estimates for each day
    vList = getVList(x, uList)
    
    i = 0
    mySum = 0
    while i < len(vList):
        mySum += logLikelihoodFunction(uList[i], vList[i])
        i += 1
    return mySum

# u: current value of daily percent change, ui
# v: current value of daily sigma(i)^2
#
# result: log likelihood score for current day.
# result = -ln(vi) - ui^2 / vi
def logLikelihoodFunction(u, v):
    if v <= 0:
        return 0
    return -1.0 * log(v) - (u ** 2) / v

# ui = (Si - Si-1) / (Si-1)
def getUList(sList):
    result = []
    i = 1
    while i < len(sList):
        result.append((sList[i] - sList[i-1]) / sList[i-1])
        i += 1
    return result

# v3 = sigma(3)^2 = u2^2
# vi = sigma(i)^2 = omega + alpha u(i-1)^2 + beta sigma(i-1)^2, i >= 4
def getVList(x, uList):
    result = []
    result.append(uList[0] ** 2)
    i = 2
    while i <= len(uList):
        result.append(x[0] + x[1] * (uList[i-1] ** 2) + x[2] * result[i-2])
        i += 1
    return result

# omega: scalar parameter in GARCH(1,1) model
# alpha: ui^2 coefficient in GARCH(1,1) model
# beta: sigma-i^2 coefficient in GARCH(1,1) model 
# sigma-i^2 = omega + alpha * ui-1^2 + beta * sigma-i-1^2
# where omega = gamma * Vl
# and gamma + alpha + beta = 1
# so 1 - alpha - beta = gamma
#
# result: Vl. Vl = omega / (1 - alpha - beta)
def getVl(omega, alpha, beta):
    return omega / (1 - alpha - beta)

if __name__ == '__main__':
    myDate = dateHandler.getDate(2012, 1, 1)
    stocks = stockSymbols.getDjiaSymbols()
    
    for symbol in stocks:
        prices = stockData.getLastYearClosingPrices(symbol, myDate)
        params = garchParams(prices)
        print symbol
        print sqrt(garchZeroDaily(params[0], params[1], params[2], prices) * 252)
        print sqrt(garchAverage(params[0], params[1], params[2], prices, 252))
        print sqrt(garchFutureDaily(params[0], params[1], params[2], prices, 252) * 252)
        print optionAnalysis.sigma(prices)
        print ""
        
    prices = stockData.getLastYearClosingPrices("T", myDate)
    params = garchParams(prices)
    print params
    print getVl(params[0], params[1], params[2])
    
    #testPrices = [1221.13, 1229.35, 1235.20, 1227.04, 1233.68, 1229.03]
    testParams = [0.000001347, 0.08339, 0.9101]
    print testParams
    print getVl(testParams[0], testParams[1], testParams[2])
    #print sqrt(garchZeroDaily(testParams[0], testParams[1], testParams[2], testPrices) * 252)
    
    print listLikelihood(params, prices)
    print listLikelihood(testParams, prices)
    
    print sqrt(garchZeroDaily(testParams[0], testParams[1], testParams[2], prices) * 252)
    print sqrt(garchZeroDaily(params[0], params[1], params[2], prices) * 252)
    print optionAnalysis.sigma(prices)
    print optionAnalysis.simpleSigma(prices)
    #print garchAverage(params[0], params[1], params[2], prices, 252)
    #print garchFutureDaily(params[0], params[1], params[2], prices, 30) * 252
    pass
