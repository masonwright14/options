from math import sqrt, exp
from random import gauss, random
from numpy import mean, std
from scipy.stats import norm

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# steps = number of steps in the binomial model. must be at least 2,
# i.e., a tree of height 1, with a root and 2 leaves.
# samples = number of sample runs to take
#
# result = list of result values of a call option
def gbmMonteCarlo(x, k, r, t, sigma, steps, samples):
    #S(t + dt) = S(t) e^((r - sigma^2 / 2) dt + sigma Z sqrt(dt))
    dt = t * 1.0 / steps
    a = (r - (sigma ** 2) / 2) * dt
    b = sigma * sqrt(dt)
    result = []
    iteration = 0
    while iteration < samples:
        s = x
        step = 0
        while step < steps:
            s *= exp(a + b * gauss(0, 1))
            step += 1
        result.append(s)
        iteration += 1
    for i in range(0, len(result) - 1):
        result[i] = max(0, result[i] - k)
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, using the stratified
# approach to variance reduction
def stratifiedOneStepGbmMonteCarlo(x, k, r, t, sigma, samples):
    # S(T) = S(0) e^((r - sigma^2 / 2) T + sigma Z sqrt(T))
    a = (r - (sigma ** 2) / 2) * t
    b = sigma * sqrt(t)
    result = []
    iteration = 0
    denom = samples + 1.0
    while iteration < samples:
        s = x * exp(a + b * norm.ppf((iteration + 1.0) / denom))
        s = max(0, s - k)
        result.append(s)
        iteration += 1
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, using the moment
# matching variance reduction technique, matching first and second moments,
# combined with the antithetic variable technique
def antitheticMomentMatchingOneStepGbmMonteCarlo(x, k, r, t, sigma, samples):
    # S(T) = S(0) e^((r - sigma^2 / 2) T + sigma Z sqrt(T))
    a = (r - (sigma ** 2) / 2) * t
    b = sigma * sqrt(t)
    result = []
    i = 0
    randomVariables = []
    while i < samples:
        randomVariables.append(gauss(0, 1))
        i += 1
    myMean = mean(randomVariables)
    myStd = std(randomVariables)
    i = 0
    while i < len(randomVariables):
        randomVariables[i] = (randomVariables[i] - myMean) / myStd
        i += 1
    iteration = 0
    while iteration < samples:
        bTemp = b * randomVariables[iteration]
        s1 = x * exp(a + bTemp)
        s2 = x * exp(a - bTemp)
        s1 = max(0, s1 - k)
        s2 = max(0, s2 - k)
        sMean = (s1 + s2) / 2.0
        result.append(sMean)
        iteration += 1
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, using the moment
# matching variance reduction technique, matching first and second moments
def momentMatchingOneStepGbmMonteCarlo(x, k, r, t, sigma, samples):
    # S(T) = S(0) e^((r - sigma^2 / 2) T + sigma Z sqrt(T))
    a = (r - (sigma ** 2) / 2) * t
    b = sigma * sqrt(t)
    result = []
    i = 0
    randomVariables = []
    while i < samples:
        randomVariables.append(gauss(0, 1))
        i += 1
    myMean = mean(randomVariables)
    myStd = std(randomVariables)
    i = 0
    while i < len(randomVariables):
        randomVariables[i] = (randomVariables[i] - myMean) / myStd
        i += 1
    iteration = 0
    while iteration < samples:
        s = x * exp(a + b * randomVariables[iteration])
        result.append(s)
        iteration += 1
    for i in range(0, len(result) - 1):
        result[i] = max(0, result[i] - k) 
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, using the antithetic
# approach to variance reduction
def antitheticOneStepGbmMonteCarlo(x, k, r, t, sigma, samples):
    # S(T) = S(0) e^((r - sigma^2 / 2) T + sigma Z sqrt(T))
    a = (r - (sigma ** 2) / 2) * t
    b = sigma * sqrt(t)
    result = []
    iteration = 0
    while iteration < samples:
        bTemp = b * gauss(0, 1)
        s1 = x * exp(a + bTemp)
        s2 = x * exp(a - bTemp)
        s1 = max(0, s1 - k)
        s2 = max(0, s2 - k)
        sMean = (s1 + s2) / 2.0
        result.append(sMean)
        iteration += 1
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option
def oneStepGbmMonteCarlo(x, k, r, t, sigma, samples):
    # S(T) = S(0) e^((r - sigma^2 / 2) T + sigma Z sqrt(T))
    a = (r - (sigma ** 2) / 2) * t
    b = sigma * sqrt(t)
    result = []
    iteration = 0
    while iteration < samples:
        s = x * exp(a + b * gauss(0, 1))
        result.append(s)
        iteration += 1
    for i in range(0, len(result) - 1):
        result[i] = max(0, result[i] - k) 
    return result

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, based on the Cox-Ross-Rubinstein
# binomial tree model
def crrMonteCarlo(x, k, r, t, sigma, steps, samples):
    dt = t / steps
    u = exp(sigma * sqrt(dt))
    d = exp(-1 * sigma * sqrt(dt))
    p = (exp(r * dt) - d) / (u - d)
    result = []
    iteration = 0
    while iteration < samples:
        s = x
        step = 0
        while step < steps:
            if random() < p:
                s *= u
            else:
                s *= d
            step += 1
        result.append(s)
        iteration += 1
    for i in range(0, len(result) - 1):
        result[i] = max(0, result[i] - k)
    return result
    
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# samples = number of sample runs to take
#
# result = list of result values of a call option, based on the equal probability
# binomial tree model
def eppMonteCarlo(x, k, r, t, sigma, steps, samples):
    dt = t / steps
    u = exp(((r - (sigma ** 2) / 2) * dt) + sigma * sqrt(dt))
    d = exp(((r - (sigma ** 2) / 2) * dt) - sigma * sqrt(dt))
    p = 0.5
    result = []
    iteration = 0
    while iteration < samples:
        s = x
        step = 0
        while step < steps:
            if random() < p:
                s *= u
            else:
                s *= d
            step += 1
        result.append(s)
        iteration += 1
    for i in range(0, len(result) - 1):
        result[i] = max(0, result[i] - k)
    return result

# values: list of values, from which to get the standard error of the mean
#
# result: standard error of the mean of the values, as s.d. / sqrt(number of values).
# assumes the values were sampled randomly with Monte Carlo methods
def standardError(values):
    return std(values) / sqrt(len(values))

# values: list of values, from which to get a confidence interval of the mean
# confidenceLevel: two-tailed percent confidence, 0 < confidenceLevel < 1
#
# result: a list with two elements, the lower bound and upper bound of the confidence
# interval
def confidenceInterval(values, confidenceLevel):
    result = []
    mu = mean(values)
    se = standardError(values)
    z = norm.ppf((1 + confidenceLevel) / 2.0)
    result.append(mu - z * se)
    result.append(mu + z * se)
    return result

# w: estimated value of the call option
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# confidenceLevel: two-tailed percent confidence, 0 < confidenceLevel < 1
#
# result: True if the estimate value falls within the confidence interval
# obtained from 100,000 runs of the one-step geometric Brownian motion
# Monte Carlo estimator, at the given confidence level
def checkCallOptionValue(w, x, k, r, t, sigma, confidenceLevel):
    result = oneStepGbmMonteCarlo(x, k, r, t, sigma, 100000)
    ci = confidenceInterval(result, confidenceLevel)
    return ci[0] <= w and ci[1] >= w

if __name__ == '__main__':
    '''
    result = gbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100, 1000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    result = oneStepGbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    result = crrMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100, 1000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    result = eppMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100, 1000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    print checkCallOptionValue(5.0, 42, 40, 0.1, 0.5, 0.2, 0.95)

    result = stratifiedOneStepGbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 10000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    '''
    result = antitheticOneStepGbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    result = momentMatchingOneStepGbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    
    result = antitheticMomentMatchingOneStepGbmMonteCarlo(42, 40, 0.1, 0.5, 0.2, 100000)
    print mean(result)
    print std(result)
    print standardError(result)
    ci = confidenceInterval(result, 0.95)
    print str(ci[0]) + " " + str(ci[1])
    pass
