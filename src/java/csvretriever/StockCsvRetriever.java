package csvretriever;

import java.io.File;

import selenium.SeleniumWebReader;
import stocksymbols.StockSymbolWiki;
import date.MyDate;

public abstract class StockCsvRetriever {

    private static final String PREFIX = 
        "http://ichart.finance.yahoo.com/table.csv?s="; // get CSV for a stock
    
    // start from Jan. 01, 2008. before end month, 0-based
    private static final String INFIX_1 = "&a=00&b=1&c=2008&d="; 
    private static final String INFIX_2 = "&e="; // before end day, 1-based
    private static final String INFIX_3 = "&f="; // before end year
    private static final String SUFFIX = "&g=d&ignore=.csv";
    
    private static final String DOWNLOADS_FOLDER = 
        "/Users/masonwright/Downloads";
    private static final String STOCK_PRICES_FOLDER = "stockPrices";
    
    public static void main(final String[] args) {
        getCsvHistoricalData();
    }
    
    public static void getCsvHistoricalData() {
        for (String stockSymbol: StockSymbolWiki.getDjiaSymbols()) {
            getCsvHistoricalData(stockSymbol);
        }
    }
    
    public static void getCsvHistoricalData(final String stockSymbol) {
        MyDate myDate = MyDate.getCurrentDate();
        final int bias = 2000;
        final int year = myDate.getYear() + bias;
        final int monthInt = myDate.getMonth().getIndexOneBased() - 1;
        String month = "" + monthInt;
        if (month.length() == 1) {
            month = "0" + month;
        }
        
        final int day = myDate.getDay();
        
        String address =
            PREFIX 
            + stockSymbol
            + INFIX_1
            + month
            + INFIX_2
            + day
            + INFIX_3
            + year
            + SUFFIX;
        System.out.println(address);
        
        SeleniumWebReader.visit(address);
        renameTable(stockSymbol);
    }
    
    private static void renameTable(final String stockSymbol) {
     // File (or directory) with old name
        File oldFile = new File(DOWNLOADS_FOLDER + "/table.csv");

        // File (or directory) with new name
        File newFile = 
            new File(STOCK_PRICES_FOLDER + "/" + stockSymbol + ".csv");
        if (newFile.exists()) {
            throw new IllegalStateException("file exists");
        }

        // Rename file (or directory)
        boolean success = oldFile.renameTo(newFile);
        if (!success) {
            throw new IllegalStateException();
        }
    }
}
