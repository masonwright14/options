package stock;

import java.util.ArrayList;
import java.util.List;

import date.MyDate;

public final class Stock {

    private final String stockSymbol;
    
    private final List<Integer> closeInThousandths;
    
    private final List<MyDate> dates;
    
    public Stock(
        final String aStockSymbol,
        final List<Integer> aCloseInThousandths,
        final List<MyDate> aDates
    ) {
        if (aCloseInThousandths == null || aCloseInThousandths.isEmpty()) {
            throw new IllegalArgumentException();
        }
        
        if (aStockSymbol == null || aStockSymbol.length() == 0) {
            throw new IllegalArgumentException();
        }
        
        if (aDates == null || aDates.size() != aCloseInThousandths.size()) {
            throw new IllegalArgumentException();
        }
        
        this.stockSymbol = aStockSymbol;
        this.closeInThousandths = aCloseInThousandths;
        this.dates = aDates;
    }

    public String getStockSymbol() {
        return stockSymbol;
    }

    public List<Integer> getCloseInThousandths() {
        return closeInThousandths;
    }
    
    public List<MyDate> getDates() {
        return dates;
    }
    
    private MyDate getLastDateOnOrBefore(final MyDate target) {
        if (dates.get(0).compareTo(target) > 0) {
            // none are on or before target
            throw new IllegalArgumentException();
        }
        
        for (int i = 1; i < dates.size(); i++) {
            if (dates.get(i).compareTo(target) > 0) {
                return dates.get(i - 1);
            }
        }
        
        return dates.get(dates.size() - 1);
    }
    
    private MyDate getFirstDateOnOrAfter(final MyDate target) {
        if (dates.get(dates.size() - 1).compareTo(target) < 0) {
            // none are on or after target
            throw new IllegalArgumentException();
        }
        
        for (int i = dates.size() - 1; i >= 0; i--) {
            if (dates.get(i).compareTo(target) < 0) {
                return dates.get(i + 1);
            }
        }
        
        return dates.get(0);
    }
    
    public int tradingDaysFromStartToEnd(
        final MyDate start,
        final MyDate end
    ) {
        if (start == null || end == null) {
            throw new IllegalArgumentException();
        }
                
        MyDate startTradingDate = getFirstDateOnOrAfter(start);
        MyDate endTradingDate = getLastDateOnOrBefore(end);
        
        if (startTradingDate.compareTo(endTradingDate) > 0) {
            throw new IllegalArgumentException();
        }
        
        return dates.indexOf(endTradingDate) 
            - dates.indexOf(startTradingDate) + 1;
    }
    
    public Integer getLastCloseOnOrBeforeDate(final MyDate date) {
        if (date == null) {
            throw new IllegalArgumentException();
        }
        int endIndex = -1;
        for (int i = dates.size() - 1; i >= 0; i--) {
            if (dates.get(i).compareTo(date) <= 0) {
                endIndex = i;
                break;
            }
        }
        
        if (endIndex == -1) {
            throw new IllegalArgumentException();
        }
       
        return closeInThousandths.get(endIndex);
    }
    
    public List<Integer> getClosesOnOrBeforeDate(
        final MyDate endDate, 
        final int howMany
    ) {
        if (howMany <= 0 || endDate == null) {
            throw new IllegalArgumentException();
        }
        
        int endIndex = -1;
        for (int i = dates.size() - 1; i >= 0; i--) {
            if (dates.get(i).compareTo(endDate) <= 0) {
                endIndex = i;
                break;
            }
        }
        
        final int startIndex = endIndex - howMany + 1;
        if (startIndex < 0) {
            throw new IllegalArgumentException();
        }
        
        List<Integer> result = new ArrayList<Integer>();
        for (int i = startIndex; i <= endIndex; i++) {
            result.add(closeInThousandths.get(i));
        }
        
        return result;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Stock [stockSymbol=");
        builder.append(stockSymbol);
        builder.append(", closeInThousandths=");
        builder.append(closeInThousandths);
        builder.append(", dates=");
        builder.append(dates);
        builder.append("]");
        return builder.toString();
    }
}
