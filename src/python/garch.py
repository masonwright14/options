from scipy.optimize import minimize
from scipy import stats
from numpy import mean, var
from math import log, exp, sqrt
from random import randint, uniform
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
    # myGuess = [0.000001347, 0.08339, 0.9101]
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

# like garchParams, but uses my own stochastic hill-climbing search with restarts to find
# parameters.
def myNaiveGarchParams(sList):
    # initial guess taken from Hull, chapter 22 on volatility estimation with GARCH(1,1)
    initialGuess = [0.000001347, 0.08339, 0.9101]
    initialLikelihood = listLikelihood(initialGuess, sList)

    bestGuess = initialGuess
    bestLikelihood = initialLikelihood

    # how many times to restart from the initial guess
    restarts = 30
    
    # how many steps to take from the start. each step changes just one parameter of the three,
    # in the direction in which likelihood increases most (or none, if both directions lead to decreases)
    stepsPerRun = 50
    while restarts > 0:
        # restart from the initial guess
        currentGuess = initialGuess
        currentLikelihood = initialLikelihood
        # reset number of steps to take for this restart
        stepsLeft = stepsPerRun
        while stepsLeft > 0:
            # pick a random parameter to change: 0 for omega, 1 for alpha, 2 for beta
            direction = randint(0,2)
            # pick a random multiplier as the step size (1 - stepSize for "down", 1 + stepSize for "up")
            stepSize = uniform(0.01, 0.2)
            # get a 2-tuple of the parameters of the better of the 2 steps, up or down, and the likelihood with those parameters
            # NB: currentGuess and currentLikelihood will be returned unchanged if neither step direction is an improvement.
            result = updateGuessAndLikelihood(currentGuess, stepSize, currentLikelihood, direction, sList)
            currentGuess = result[0]
            currentLikelihood = result[1]
            stepsLeft -= 1
        # at the end of a run, update the best guess and its likelihood, if there is an improvement
        if currentLikelihood > bestLikelihood:
            bestLikelihood = currentLikelihood
            bestGuess = currentGuess
        restarts -= 1
    return bestGuess

def updateGuessAndLikelihood(currentGuess, stepSize, currentLikelihood, index, sList):
    oldValue = currentGuess[index]
    lower = oldValue * (1 - stepSize)
    if lower < 0:
        lower = oldValue / 2
        
    higher = oldValue * (1 + stepSize)
    if higher > 1:
        higher = (1 + oldValue) / 2.0

    currentGuess[index] = lower
    lowResult = listLikelihood(currentGuess, sList)
    currentGuess[index] = higher
    highResult = listLikelihood(currentGuess, sList)
    if lowResult > currentLikelihood or highResult > currentLikelihood:
        if lowResult > highResult:
            currentGuess[index] = lower
            currentLikelihood = lowResult
        else:
            currentGuess[index] = higher
            currentLikelihood = highResult
    else:
        currentGuess[index] = oldValue
        
    return (currentGuess, currentLikelihood)
    
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
'''
            uList                vList
0           u[0]^2               u[0]^2
1           u[1]^2               w + a u[1]^2 + b v[0]^2
2           u[2]^2               w + a u[2]^2 + b u[1]^2

to compare:
            u[1]^2               v[0]^2
            u[2]^2               v[1]^2
'''
def listLikelihood(x, sList):
    # get list of daily percent changes
    uList = getUList(sList)
    
    # get list of GARCH(1,1) sigma(i)^2 estimates for each day
    vList = getVList(x, uList)
    
    i = 0
    mySum = 0
    while i < len(uList) - 1:
        mySum += logLikelihoodFunction(uList[i + 1], vList[i])
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

# values: a time series of values to find the autocorrelation
# lag: the number of steps between values in the autocorrelation
#
# result: autocorrelation of values with offset of "lag"
# result = E((xi - x-bar) (xi+lag - x-bar)) / sigma^2
# where x-bar is the sample mean, sigma^2 is the variance
def autocorr(values, lag):
    total = 0
    myMean = mean(values)
    i = lag
    while i < len(values):
        total += (values[i] - myMean) * (values[i-lag] - myMean)
        i += 1
    cov = float(total) / (len(values) - lag)
    return cov / var(values)

# values: a time series of values to find the autocorrelation
# maxLag: the maximum number of steps between values in the autocorrelation.
#
# result: a list of autocorrelations, with lags from 1 to maxLag.
def autocorrSeries(values, maxLag):
    result = []
    i = 1
    while i <= maxLag:
        result.append(autocorr(values, i))
        i += 1
    return result

# values: a time series of values to find the autocorrelation
# maxLag: the maximum number of steps between values to analyze.
#
# result: the Ljung-Box statistic, a measure of autocorrelation.
# result = m (m + 2) Sum i:1->maxLag (ni^2 / (m-i))
# where:
# m = number of observations in time series
# maxLag = number of lags considered
# ni = autocorrelation of the data points for lag of i
def ljungBox(values, maxLag):
    m = len(values)
    total = 0
    i = 1
    while i <= maxLag:
        corr = autocorr(values, i)
        total += (corr ** 2) / float(m - i)
        i += 1
    return m * (m + 2) * total

# values: a time series of values to find the autocorrelation
# maxLag: the maximum number of steps between values to analyze.
#
# result: the p-value for the hypothesis that there is autocorrelation
# within a lag of maxLag or less in the data set of values.
# p-value = 1 - Pr(chi-squared value)
# note: Ljung-Box statistic has a chi-squared distribution, with
# degrees of freedom equal to the maximum lag
def ljungBoxPValue(values, maxLag):
    return 1 - stats.chi2.cdf(ljungBox(values, maxLag), maxLag)

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

# sList: list of stock closing prices as a daily time series
#
# result: no return value.
# prints report evaluating quality of GARCH(1,1) estimates of volatility.
# omega: scalar parameter in GARCH(1,1) model
# alpha: ui^2 coefficient in GARCH(1,1) model
# beta: sigma-i^2 coefficient in GARCH(1,1) model
# sigma-i^2 = omega + alpha * ui-1^2 + beta * sigma-i-1^2
# autocorrelation:  E((xi - x-bar) (xi+lag - x-bar)) / sigma^2
# where x-bar is the sample mean, sigma^2 is the variance
# lists autocorrelation by lag, from 1-15, for u(i)^2 and u(i)^2/sigma(i)^2,
# where u(i)^2 is the square of the percent change in stock price from day to day,
# and sigma(i)^2 is the GARCH(1,1) estimate of variance from day to day.
# Ljung-Box is the Ljung-Box statistic with 15 degrees of freedom for 15 lags,
# for either u(i)^2 or u(i)^2/sigma(i)^2.
# the P-Value is obtained from the Ljung-Box statistic; if it is lower than 0.05, reject
# the hypothesis of no autocorrelation for lags less than or equal to 15.
def printGarchReport(sList):
    uList = getUList(sList)
    params = myNaiveGarchParams(sList)
    #params = garchParams(sList)
    likelihood = listLikelihood(params, sList)
    vList = getVList(params, uList)
    currentVolatility = sqrt(vList[len(vList) - 1] * 252)
    maxLag = 15
    i = 0
    while i < len(uList):
        uList[i] = uList[i] ** 2
        if uList[i] != 0:
            vList[i] = vList[i] / uList[i]
        i += 1
    uAutocorrs = autocorrSeries(uList, maxLag)
    quotientAutocorrs = autocorrSeries(vList, maxLag)
    i = 0
    print "omega: " + str(params[0]) + "\talpha: " + "%.3f" % params[1] + "\tbeta: " + "%.3f" % params[2]
    print "likelihood score: " + str(likelihood)
    print "Current volatility: " + str(currentVolatility)
    print ""
    print "autocorrelation:"
    print "lag \t\tu^2\t\tu^2/s^2"
    while i < maxLag:
        print str(i + 1) + "\t\t" + "%.3f" % uAutocorrs[i] + "\t\t" + "%.3f" % quotientAutocorrs[i]
        i += 1
    print ""
    uLjung = ljungBox(uList, maxLag)
    quotientLjung = ljungBox(vList, maxLag)
    uLjnugPValue = ljungBoxPValue(uList, maxLag)
    quotientLjnugPValue = ljungBoxPValue(vList, maxLag)
    print "Ljung-Box\t" + "%.3f" % uLjung + "\t\t" + "%.3f" % quotientLjung
    print "P-Value\t\t" + "%.6f" % uLjnugPValue + "\t" + "%.6f" % quotientLjnugPValue

if __name__ == '__main__':
    '''
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
    '''
    
    
    myDate = dateHandler.getDate(2012, 1, 1)
    prices = stockData.getLastYearClosingPrices("KO", myDate)
    printGarchReport(prices)
    
    
    '''
    myDate = dateHandler.getDate(2012, 1, 1)
    stocks = stockSymbols.getDjiaSymbols()
    
    for symbol in stocks:
        prices = stockData.getLastYearClosingPrices(symbol, myDate)
        params = garchParams(prices)
        print symbol
        print params
        print sqrt(garchZeroDaily(params[0], params[1], params[2], prices) * 252)
        print optionAnalysis.sigma(prices)
        params = myNaiveGarchParams(prices)
        print params
        print sqrt(garchZeroDaily(params[0], params[1], params[2], prices) * 252)
        print optionAnalysis.sigma(prices)
        print ""
    '''
    pass
