
# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# m = number of intervals to use for underlying prices, between 0 and sMax
# n = number of intervals to use for time steps, between 0 (present) and t (maturity)
#
# result: present value in dollars of an American call option on the stock, where
# early exercise is allowed.
def explicitFiniteDifferenceCallAmerican(x, k, r, t, sigma, m, n):
    # let maximum price considered for the stock be twice the max of x and k
    sMax = 2.0 * max(x, k)
    deltaT = 1.0 * t / n
    deltaS = sMax / m
    
    # currentVals will hold the value of the option at a certain time, for each underlying price,
    # working backward from expiration time
    currentVals = []
    for sIndex in range(0, m + 1):
        # initialize to intrinsic value of the option at expiration
        val = max(sIndex * deltaS - k, 0)
        currentVals.append(val)
    #print ["%0.2f" % i for i in currentVals]
    
    # calculate values of parameters aj, bj, cj, for each value of the stock price index j from 1->m
    aVals = []
    bVals = []
    cVals = []
    for sIndex in range(0, m + 1):
        # reference: Hull chapter 20
        a = (-0.5 * r * sIndex * deltaT + 0.5 * (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        aVals.append(a)
        b = (1 - (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        bVals.append(b)
        c = (0.5 * r * sIndex * deltaT + 0.5 * (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        cVals.append(c)
    
    tIndex = n - 1
    while tIndex >= 0:
        # newVals will hold the value of the option at the preceding time interval, for each underlying price
        newVals = []
        for sIndex in range(0, m + 1):
            if sIndex == 0:
                # when s = 0, call value = 0
                newVals.append(0)
                continue
            if sIndex == m:
                # when s = sMax, call value = sMax - k
                newVals.append(sMax - k)
                continue
            f = aVals[sIndex] * currentVals[sIndex - 1] + bVals[sIndex] * currentVals[sIndex] + cVals[sIndex] * currentVals[sIndex + 1]
            intrinsicValue = sIndex * deltaS - k
            if intrinsicValue > 0:
                # value can never be below intrinsic value
                f = max(intrinsicValue, f)
            newVals.append(f)
        currentVals = newVals
        #print ["%0.2f" % i for i in currentVals]
        tIndex -= 1
    # return option value at time 0 (present), for closest underlying price to x
    sIndex = int(x / deltaS)
    return currentVals[sIndex]

# x = underlying price in dollars
# k = strike price in dollars
# r = risk free interest rate, adjusted as continuously compounding
# t = time to maturity in years
# sigma = square root of variance rate of return of the underlying
# m = number of intervals to use for underlying prices, between 0 and sMax
# n = number of intervals to use for time steps, between 0 (present) and t (maturity)
#
# result: present value in dollars of an American put option on the stock, where
# early exercise is allowed.
def explicitFiniteDifferencePutAmerican(x, k, r, t, sigma, m, n):
    # let maximum price considered for the stock be twice the max of x and k
    sMax = 2.0 * max(x, k)
    deltaT = 1.0 * t / n
    deltaS = sMax / m
    
    # currentVals will hold the value of the option at a certain time, for each underlying price,
    # working backward from expiration time
    currentVals = []
    for sIndex in range(0, m + 1):
        # initialize to intrinsic value of the option at expiration
        val = max(k - sIndex * deltaS, 0)
        currentVals.append(val)
    #print ["%0.2f" % i for i in currentVals]
    
    # calculate values of parameters aj, bj, cj, for each value of the stock price index j from 1->m
    aVals = []
    bVals = []
    cVals = []
    for sIndex in range(0, m + 1):
        # reference: Hull chapter 20
        a = (-0.5 * r * sIndex * deltaT + 0.5 * (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        aVals.append(a)
        b = (1 - (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        bVals.append(b)
        c = (0.5 * r * sIndex * deltaT + 0.5 * (sigma ** 2) * (sIndex ** 2) * deltaT) / (1 + r * deltaT)
        cVals.append(c)
    
    tIndex = n - 1
    while tIndex >= 0:
        # newVals will hold the value of the option at the preceding time interval, for each underlying price
        newVals = []
        for sIndex in range(0, m + 1):
            if sIndex == 0:
                # when s = 0, put value is k
                newVals.append(k)
                continue
            if sIndex == m:
                # when s = sMax, put value is 0
                newVals.append(0)
                continue
            f = aVals[sIndex] * currentVals[sIndex - 1] + bVals[sIndex] * currentVals[sIndex] + cVals[sIndex] * currentVals[sIndex + 1]
            intrinsicValue = k - sIndex * deltaS
            if intrinsicValue > 0:
                # value can never be below intrinsic value
                f = max(intrinsicValue, f)
            newVals.append(f)
        currentVals = newVals
        #print ["%0.2f" % i for i in currentVals]
        tIndex -= 1
    # return option value at time 0 (present), for closest underlying price to x
    sIndex = int(x / deltaS)
    return currentVals[sIndex]

if __name__ == '__main__':
    #print explicitFiniteDifferenceCallAmerican(42, 40, 0.1, 0.5, 0.2, 40, 20)
    print explicitFiniteDifferencePutAmerican(50, 50, 0.1, 0.4167, 0.4, 20, 10)
    pass