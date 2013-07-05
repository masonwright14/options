package stock;

import java.util.ArrayList;
import java.util.List;

import date.DateUtil;


public abstract class StockFactory {

    public static Stock getStock(
        final String stockSymbol,
        final List<List<String>> data
    ) {
        List<Integer> closeInThousandths = new ArrayList<Integer>();
        try {
            // iterate over table from bottom row (earliest) to top row (most recent)
            for (int i = data.size() - 1; i >= 0; i--) {
                int currentCloseInThousandths = DateUtil.getPriceInThousandths(data.get(i).get(4));
                closeInThousandths.add(currentCloseInThousandths);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        
        return new Stock(
            stockSymbol, 
            closeInThousandths
        );
    }
}
