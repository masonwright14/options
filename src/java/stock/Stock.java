package stock;

import java.util.List;

public class Stock {

    private final String stockSymbol;
    
    private final List<Integer> closeInThousandths;
    
    public Stock(
        final String aStockSymbol,
        final List<Integer> aCloseInThousandths
    ) {
        if (aCloseInThousandths == null || aCloseInThousandths.isEmpty()) {
            throw new IllegalArgumentException();
        }
        
        if (aStockSymbol == null || aStockSymbol.length() == 0) {
            throw new IllegalArgumentException();
        }
        
        this.stockSymbol = aStockSymbol;
        this.closeInThousandths = aCloseInThousandths;
    }

    public String getStockSymbol() {
        return stockSymbol;
    }

    public List<Integer> getCloseInThousandths() {
        return closeInThousandths;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Stock [stockSymbol=");
        builder.append(stockSymbol);
        builder.append(", closeInThousandths=");
        builder.append(closeInThousandths);
        builder.append("]");
        return builder.toString();
    }
}
