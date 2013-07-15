package stocksymbols;

import java.util.Arrays;
import java.util.List;

public abstract class StockSymbolWiki {
    
    private static final String DJIA_SYMBOLS = "AA,AXP,BA,BAC,CAT,CSCO," 
        + "CVX,DD,DIS,GE,HD,HPQ,IBM,INTC,JNJ,JPM,KO,MCD,MMM," 
        + "MRK,MSFT,PFE,PG,T,TRV,UNH,UTX,VZ,WMT,XOM";
    
    public static List<String> getDjiaSymbols() {        
        return Arrays.asList(DJIA_SYMBOLS.split(","));
    }
    
    /*
    public static List<String> getSymbols() {
        List<List<String>> tableData = 
            WebStrings.getTableContents(getDataTable());
        
        final int fiveHundredOne = 501;
        if (tableData.size() != fiveHundredOne) {
            throw new IllegalStateException();
        }
        
        List<String> result = new ArrayList<String>();
        for (int i = 1; i < tableData.size(); i++) {
            result.add(tableData.get(i).get(0));
        }
        
        Collections.sort(result, String.CASE_INSENSITIVE_ORDER);
        return result;
    }

    private static String getWikiText() {
        return WebReader.getText(
            "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        );
    }
    
    private static String getDataTable() {
        final String source = getWikiText();
        final String startString = 
            "<table class=\"wikitable sortable\">\n" 
            + "<tr>\n<th><a href=\"/wiki/Ticker_symbol\"";
        int startIndex = source.indexOf(startString);
        if (startIndex < 0) {
            throw new IllegalArgumentException();
        }
        
        int endIndex = source.indexOf("</table>", startIndex);
        if (endIndex < 0) {
            throw new IllegalArgumentException();
        }
        final int endTableSize = 8;
        endIndex += endTableSize;
        
        return source.substring(startIndex, endIndex);
    }
    */
}
