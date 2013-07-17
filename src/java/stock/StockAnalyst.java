package stock;

import java.util.List;

import date.MyDate;

public abstract class StockAnalyst {

    /*
     * Interval means how many numbers are included in the range. 
     * 2 is the minimum,
     * i.e. you can't divide index i by index i for a range of 1.
     */
    public static double getMeanRatio(
        final List<Integer> values, 
        final int interval
    ) {
        if (values == null) {
            throw new IllegalArgumentException();
        }
        if (interval < 2) {
            throw new IllegalArgumentException();
        }
        if (values.size() / 2 < interval) {
            throw new IllegalArgumentException();
        }
        
        double totalRatio = 0;
        int count = 0;
        
        for (
            int startIndex = 0; 
            startIndex + interval <= values.size(); 
            startIndex++
        ) {
            totalRatio += 
                ((double) values.get(startIndex + interval - 1)) 
                    / values.get(startIndex);
            count++;
        }
        
        return totalRatio / count;
    }
    
    public static double getExpectedPresentValueAtExpiration(
        final Stock stock,
        final MyDate expirationDate,
        final MyDate currentDate,
        final double nominalInterestRate,
        final int numberOfHistoricalDatesToUse,
        final int strikeInThousandths
    ) {
        return getPresentValue(
            expirationDate, 
            currentDate, 
            nominalInterestRate, 
            getExpectedIntrinsicValueAtExpiration(
                stock, 
                expirationDate, 
                currentDate,
                numberOfHistoricalDatesToUse, 
                strikeInThousandths
            )
        );
    }
    
    public static double getPresentValue(
        final MyDate maturityDate,
        final MyDate currentDate,
        final double nominalInterestRate,
        final double valueAtMaturity
    ) {
        if (maturityDate == null || currentDate == null) {
            throw new IllegalArgumentException();
        }
        
        final int daysToMaturity = currentDate.daysFromThisToThat(maturityDate);
        if (daysToMaturity < 0) {
            throw new IllegalArgumentException();
        }
        
        return valueAtMaturity 
            * Math.pow(Math.E, -1 * (1 + nominalInterestRate) * daysToMaturity);
    }
    
    public static double getExpectedIntrinsicValueAtExpiration(
        final Stock stock,
        final MyDate expirationDate,
        final MyDate currentDate,
        final int numberOfHistoricalDatesToUse,
        final int strikeInThousandths
    ) {
        final List<Integer> pricesInThousandths = 
            stock.getClosesOnOrBeforeDate(
                currentDate, 
                numberOfHistoricalDatesToUse
            );
        
        if (pricesInThousandths == null) {
            throw new IllegalArgumentException();
        }
        
        final int slidingWindowWidth = 
            stock.tradingDaysFromStartToEnd(currentDate, expirationDate);
        if (slidingWindowWidth < 2) {
            throw new IllegalArgumentException();
        }
        if (pricesInThousandths.size() / 2 < slidingWindowWidth) {
            throw new IllegalArgumentException();
        }
        
        double totalValueOverStrike = 0;
        int count = 0;
        
        final int initialUnderlyingPriceInThousandths = 
            stock.getLastCloseOnOrBeforeDate(currentDate);
        for (
            int startIndex = 0; 
            startIndex + slidingWindowWidth <= pricesInThousandths.size(); 
            startIndex++
        ) {
            double ratio = 
                ((double) pricesInThousandths.get(
                    startIndex + slidingWindowWidth - 1)
                ) 
                    / pricesInThousandths.get(startIndex);
            double predictedUnderlyingPrice = 
                ratio * initialUnderlyingPriceInThousandths;
            if (predictedUnderlyingPrice > strikeInThousandths) {
                totalValueOverStrike += predictedUnderlyingPrice;
            }
            
            count++;
        }
        
        return totalValueOverStrike / count;
    }
}
