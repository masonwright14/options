package stock;

import java.util.ArrayList;
import java.util.List;

import csvreader.CsvReader;

import stocksymbols.StockSymbolWiki;


public final class StockModel {
    
    private final List<Stock> stocks;
    
    public StockModel() {
        this.stocks = new ArrayList<Stock>();
    }

    public void loadAllStocks() {
        stocks.clear();
        
        for (String stockSymbol: StockSymbolWiki.getDjiaSymbols()) {
            final String fileName = "stockPrices/" + stockSymbol + ".csv";
            stocks.add(
                StockFactory.getStock(stockSymbol, 
                CsvReader.getRowsAfterHeader(fileName)
            ));
        }
    }
    
    public List<Stock> getStocks() {
        return stocks;
    }
}
