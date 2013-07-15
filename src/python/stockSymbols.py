djiaSymbols = "AA,AXP,BA,BAC,CAT,CSCO,CVX,DD,DIS,GE,HD,HPQ,IBM,INTC,JNJ,JPM,KO,MCD,MMM,MRK,MSFT,PFE,PG,T,TRV,UNH,UTX,VZ,WMT,XOM"

# result: a list of Dow Jones stock ticker symbols, as strings in alphabetical order
def getDjiaSymbols():
    return djiaSymbols.split(",")