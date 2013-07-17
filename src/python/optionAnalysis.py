from math import log, sqrt, exp
from scipy.stats import norm
        
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
#
# result: the Black-Scholes-Merton model value of a call option on one share of the underlying stock
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
    return (log(x / float(k)) + t * (r + ((sigma ** 2) / 2.0))) / (float(sigma) * sqrt(t))

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
def d2(x, k, r, t, sigma):
    return d1(x, k, r, t, sigma) - sigma * sqrt(t)

# c = current price of the call option on 1 share of the underlying
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
#
# result: implied volatility of the underlying, to a tolerance of 0.001,
# based on the Black-Scholes-Merton model
def impliedSigma(c, x, k, r, t):
    tolerance = 0.001
    myMin = tolerance
    myMax = 2.0
    while (myMax - myMin > tolerance):
        guess = (myMax + myMin) / 2.0
        guessResult = w(x, k, r, t, guess)
        if guessResult < c:
            myMin = guess
        else:
            if guessResult > c:
                myMax = guess
            else:
                return guess        
    return (myMax + myMin) / 2.0
    
'''
def impliedSigma(c, x, k, r, t):
    tolerance = 0.001
    guess = random.random()
    
    # use Newton's method to find a zero of (w - c)
    tries = 0
    while fabs(w(x, k, r, t, guess) - c) > tolerance:
        myVega = vega(x, k, r, t, guess)
        if myVega == 0:
            guess = random.random()
            tries += 1
            continue
        guess -= (w(x, k, r, t, guess) - c) / myVega
        tries += 1
        if tries % 20 == 0:
            guess = random.random()
            if tries >= 100:
                return -5.0
    return guess
    
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
#
# result: the partial derivative of the black-scholes value of a call option
# on one share of the underlying, with respect to the volatility (sigma)
def vega(x, k, r, t, sigma):
    return x * norm.pdf(d1(x, k, r, t, sigma)) * sqrt(t)
'''

# prices = array of daily closing prices in dollars, all prices >= 0
# result: mean log rate of return from one price to the next
def sampleMeanLogReturn(prices):
    return log(prices[len(prices) - 1] / prices[0]) / (len(prices) - 1)

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
    return sqrt(252 * total / float((len(prices) - 2)))

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

if __name__ == '__main__':
    #print interestData.continuousInterest(dateHandler.getDate(2013, 6, 24), dateHandler.getDate(2015, 1, 17))
    #print w(81.52, 145, 0.006, 572.0 / 252.0, 0.22)
    #print impliedSigma(8.2, 23.58, 16, 0.004, 26 / 252.0)
    #print w(23.58, 16, 0.004, 26 / 252.0, 2)
    pass
