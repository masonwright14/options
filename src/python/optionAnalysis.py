from math import log, sqrt, exp
from scipy.stats import norm
        
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
#
# result: the blackScholes model value of a call option on one share of the underlying stock
def w(x, k, r, t, sigma):
    return x * norm.cdf(d1(x, k, r, t, sigma)) - k * exp(-1 * r * t) * norm.cdf(d2(x, k, r, t, sigma))

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
#
# result: number of shares of the underlying needed to balance a call option on 1 share
def w1(x, k, r, t, sigma):
    return norm.cdf(d1(x, k, r, t, sigma))

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
def d1(x, k, r, t, sigma):
    return log(x / float(k)) + t * (r + (sigma ** 2) / 2.0) / (float(sigma) * sqrt(t))

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
def d2(x, k, r, t, sigma):
    return d1(x, k, r, t, sigma) - sigma * sqrt(t)

# m = times per year compounded. m >= 1
# rm = annual interest with incremental compounding. rm > 0.
#
# result: the continuous interest rate corresponding to annual interest
# rate rm, compounded m times per year
def rContinuous(m, rm):
    return m * log(1 + rm / m)

# prices = array of daily closing prices in dollars, all prices >= 0
# result: mean log rate of return from one price to the next
def sampleMeanLogReturn(prices):
    return log(prices[len(prices) - 1] / prices[0]) / len(prices)

# prices = array of daily closing prices in dollars
# result: volatility of the price range, where sigma is estimated as:
# sqrt( 252 * (1/(n-1)) Sum i=1->n (log(prices[i] / prices[i-1]) - "sample mean log return")^2 )
# based on 252 trading days per year and unbiased variant of MLE for standard deviation
#
# sigma = estimated historical standard deviation in log return of the underlying stock
def sigma(prices):
    total = 0
    meanLogReturn = sampleMeanLogReturn(prices)
    i = 1
    while i < len(prices):
        total += (log(prices[i] / float(prices[i-1])) - meanLogReturn) ** 2
        i += 1
    return sqrt(252 * total / float((len(prices) - 1)))

# xf = new market value of stock
# xi = previous market value of stock
# ti = initial time to maturity in years of the call option
# w1 = number of shares of the underlying needed to short balance 1 call option held (option to buy 1 share)
# r = risk free interest rate with continuous compounding
# sigma = estimated historical standard deviation of the log return of the underlying stock
#
# result: paper profit from holding one call option and being short the proper hedge in the underlying stock, 
# since the previous trading day's end
def excessDailyDollarReturn2(xf, xi, ti, k, r, sigma):
    myWf = w(xf, k, r, ti + 1 / 252.0, sigma)
    myWi = w(xi, k, r, ti, sigma)
    myW1 = w1(xi, k, r, ti, sigma)
    return excessDailyDollarReturn(myWf, myWi, xf, xi, myW1, r)

# wf = new model value of call option on 1 share of stock
# wi = previous model value of call option on 1 share of stock
# xf = new market value of stock
# xi = previous market value of stock
# w1 = number of shares of the underlying needed to short balance 1 call option held (option to buy 1 share)
# r = risk free interest rate with continuous compounding
#
# result: paper profit from holding one call option and being short the proper hedge in the underlying stock, 
# since the previous trading day's end
def excessDailyDollarReturn(wf, wi, xf, xi, w1, r):
    return (wf - wi) - w1 * (xf - xi) - (wf - w1 * xf) * (exp(r / 252.0) - 1)
