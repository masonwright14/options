package stocksymbols;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import launcher.StockListFinder;
import launcher.Util;


public abstract class StockListRetriever {

    public static void printStockListToFileIfNeeded() {
        if (StockListFinder.isStockListSameAsMostRecent()) {
            return;
        }
        
        printStockListToFile();
    }

    public static void printStockListToFile() {        
        File file = new File(getNextFileName());

        try {
            if (!file.createNewFile()) {
                return;
            }
            
            FileWriter fw = new FileWriter(file);
            BufferedWriter bw = new BufferedWriter(fw);
            List<String> symbols = StockSymbolWiki.getDjiaSymbols();
            for (int i = 0; i < symbols.size(); i++) {
                if (i + 1 < symbols.size()) {
                    bw.write(symbols.get(i) + ',');
                } else {
                    bw.write(symbols.get(i) + '\n');
                }
            }
            bw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String getNextFileName() {
        return StockListFinder.STOCK_LIST_PREFIX 
            + Util.getDateDDMMYY() 
            + StockListFinder.CSV_EXTENSION;
    }
}
