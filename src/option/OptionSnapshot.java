package option;

public final class OptionSnapshot {

    private final String optionSymbol;
    
    private final String stockSymbol;
    
    private final int bidInThousandths;
    
    private final int askInThousandths;
    
    private final int lastInThousandths;
    
    private final int volume;
    
    private final int openInterval;
    
    private static final String OPTION_SYMBOL = "OptionSymbol";
    private static final String STOCK_SYMBOL = "StockSymbol";
    private static final String BID_IN_THOUSANDTHS = "BidInThousandths";
    private static final String ASK_IN_THOUSANDTHS = "AskInThousandths";
    private static final String LAST_IN_THOUSANDTHS = "LastInThousandths";
    private static final String VOLUME = "Volume";
    private static final String OPEN_INTERVAL = "Open Interval";
    
    private static final String CSV_HEADER =
        OPTION_SYMBOL + "," + STOCK_SYMBOL + "," + BID_IN_THOUSANDTHS 
        + "," + ASK_IN_THOUSANDTHS + "," + LAST_IN_THOUSANDTHS
        + "," + VOLUME + "," + OPEN_INTERVAL;

    public OptionSnapshot(
        final String aOptionSymbol, 
        final String aStockSymbol,
        final int aBidInThousandths, 
        final int aAskInThousandths, 
        final int aLastInThousandths,
        final int aVolume,
        final int aOpenInterval
    ) throws InstantiationException {
        if (!OptionSymbolUtil.isOptionSymbol(aOptionSymbol)) {
            throw new InstantiationException(aOptionSymbol);
        }
        
        if (aStockSymbol == null || aStockSymbol.length() == 0) {
            throw new InstantiationException(aOptionSymbol);
        }
        
        if (aBidInThousandths > aAskInThousandths) {
            throw new InstantiationException();
        }
        
        this.optionSymbol = aOptionSymbol;
        this.stockSymbol = aStockSymbol;
        this.bidInThousandths = aBidInThousandths;
        this.askInThousandths = aAskInThousandths;
        this.lastInThousandths = aLastInThousandths;
        this.volume = aVolume;
        this.openInterval = aOpenInterval;
    }

    public String getOptionSymbol() {
        return this.optionSymbol;
    }

    public String getStockSymbol() {
        return this.stockSymbol;
    }

    public int getBidInThousandths() {
        return this.bidInThousandths;
    }

    public int getAskInThousandths() {
        return this.askInThousandths;
    }

    public int getLastInThousandths() {
        return this.lastInThousandths;
    }
    
    public int getVolume() {
        return this.volume;
    }

    public int getOpenInterval() {
        return this.openInterval;
    }

    public static String getCSVHeader() {
        return CSV_HEADER;
    }
    
    public String getCSVString() {
        StringBuilder builder = new StringBuilder();
        builder.append(optionSymbol).append(',')
            .append(stockSymbol).append(',')
            .append(bidInThousandths).append(',')
            .append(askInThousandths).append(',')
            .append(lastInThousandths).append(',')
            .append(volume).append(',')
            .append(openInterval);
        
        return builder.toString();
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("OptionSnapshot [optionSymbol=");
        builder.append(optionSymbol);
        builder.append(", stockSymbol=");
        builder.append(stockSymbol);
        builder.append(", bidInThousandths=");
        builder.append(bidInThousandths);
        builder.append(", askInThousandths=");
        builder.append(askInThousandths);
        builder.append(", lastInThousandths=");
        builder.append(lastInThousandths);
        builder.append(", volume=");
        builder.append(volume);
        builder.append(", openInterval=");
        builder.append(openInterval);
        builder.append("]");
        return builder.toString();
    }
}
