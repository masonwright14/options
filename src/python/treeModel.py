from math import sqrt, exp

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# steps = number of steps in the binomial model. must be at least 2,
# i.e., a tree of height 1, with a root and 2 leaves.
#
# result: the Cox-Ross-Rubinstein value of a call option on the stock,
# obtained by working backwards through a binomial tree.
# assumes that u = 1 / d, where u = "up" multipier and d = "down" multiplier.
def coxRossRubinsteinW(x, k, r, t, sigma, steps):
    dt = t / steps
    u = exp(sigma * sqrt(dt))
    d = exp(-1 * sigma * sqrt(dt))
    p = (exp(r * dt) - d) / (u - d)
    callValues = []
    for i in range(0, steps):
        s = x * (u ** (steps - i)) * (d ** i)
        callValues.append(max(0, s - k))
    while len(callValues) > 1:
        newCallValues = []
        tempSteps = len(callValues) - 1
        for i in range(0, tempSteps):
            upperFuture = callValues[i]
            lowerFuture = callValues[i + 1]
            temp = (p * upperFuture + (1 - p) * lowerFuture) * exp(-1 * r * dt)
            s = x * (u ** (tempSteps - i)) * (d ** i)
            temp = max(temp, s - k)
            newCallValues.append(temp)
        callValues = newCallValues
    return callValues[0]

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# steps = number of steps in the binomial model. must be at least 2,
# i.e., a tree of height 1, with a root and 2 leaves.
#
# result: the value of a call option on the stock,
# obtained by working backwards through a binomial tree.
# assumes that p = 0.5, where p = probability of an "up" movement.
def equalProbabilityW(x, k, r, t, sigma, steps):
    dt = t / steps
    u = exp(((r - (sigma ** 2) / 2) * dt) + sigma * sqrt(dt))
    d = exp(((r - (sigma ** 2) / 2) * dt) - sigma * sqrt(dt))
    p = 0.5
    callValues = []
    for i in range(0, steps):
        s = x * (u ** (steps - i)) * (d ** i)
        callValues.append(max(0, s - k))
    while len(callValues) > 1:
        newCallValues = []
        tempSteps = len(callValues) - 1
        for i in range(0, tempSteps):
            upperFuture = callValues[i]
            lowerFuture = callValues[i + 1]
            temp = (p * upperFuture + (1 - p) * lowerFuture) * exp(-1 * r * dt)
            s = x * (u ** (tempSteps - i)) * (d ** i)
            temp = max(temp, s - k)
            newCallValues.append(temp)
        callValues = newCallValues
    return callValues[0]

if __name__ == '__main__':
    #print coxRossRubinsteinW(81.52, 145, 0.006, 572.0 / 252.0, 0.22, 60)
    #print coxRossRubinsteinW(23.58, 16, 0.004, 26 / 252.0, 2, 60)
    #print equalProbabilityW(81.52, 145, 0.006, 572.0 / 252.0, 0.22, 60)
    #print equalProbabilityW(23.58, 16, 0.004, 26 / 252.0, 2, 60)
    #print coxRossRubinsteinW(300.0, 300.0, 0.08, 0.3333, 0.3, 30)
    #print equalProbabilityW(300.0, 300.0, 0.08, 0.3333, 0.3, 30)
    print equalProbabilityW(42, 40, 0.1, 0.5, 0.2, 100)
    pass
