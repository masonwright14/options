package dividends;

import date.MyDate;

public final class Dividend {

    private final String stockSymbol;
    private final int thousandths;    
    private final MyDate exDividendDay;
    
    private static final String STOCK_SYMBOL = "StockSymbol";
    private static final String THOUSANDTHS = "Thousandths";
    private static final String EX_DIVIDEND_DATE = "ExDividendDate";
    private static final String CSV_HEADER = 
        STOCK_SYMBOL + "," + THOUSANDTHS + "," + EX_DIVIDEND_DATE;

    public Dividend(
        final String aStockSymbol,
        final int aThousandths, 
        final MyDate aExDividendDay
    ) {
        this.stockSymbol = aStockSymbol;
        this.thousandths = aThousandths;
        this.exDividendDay = aExDividendDay;
    }
    
    public String getStockSymbol() {
        return this.stockSymbol;
    }
    
    public int getThousdandths() {
        return this.thousandths;
    }

    public MyDate getExDividendDay() {
        return this.exDividendDay;
    }
    
    public static String getCSVHeader() {
        return CSV_HEADER;
    }
    
    public String getCSVString() {
        StringBuilder builder = new StringBuilder();
        builder.append(stockSymbol).append(',')
            .append(thousandths).append(',')
            .append(exDividendDay.getCSVString());
        return builder.toString();
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Dividend [stockSymbol=");
        builder.append(stockSymbol);
        builder.append(", cents=");
        builder.append(thousandths);
        builder.append(", exDividendDay=");
        builder.append(exDividendDay);
        builder.append("]");
        return builder.toString();
    }
}
