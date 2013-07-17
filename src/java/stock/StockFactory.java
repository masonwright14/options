package stock;

import java.util.ArrayList;
import java.util.List;

import option.OptionUtil;
import date.Month;
import date.MyDate;


public abstract class StockFactory {

    public static Stock getStock(
        final String stockSymbol,
        final List<List<String>> data
    ) {
        List<Integer> closeInThousandths = new ArrayList<Integer>();
        List<MyDate> myDates = new ArrayList<MyDate>();
        try {
            // iterate over table from bottom row (earliest) 
            // to top row (most recent)
            for (int i = data.size() - 1; i >= 0; i--) {
                int currentCloseInThousandths = 
                    OptionUtil.getPriceInThousandths(data.get(i).get(4));
                closeInThousandths.add(currentCloseInThousandths);
                MyDate currentDate = getMyDate(data.get(i).get(0));
                myDates.add(currentDate);
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        
        return new Stock(
            stockSymbol, 
            closeInThousandths,
            myDates
        );
    }
    
    // format: 2013-07-01
    public static MyDate getMyDate(final String dateString) {        
        int monthIndex = Integer.parseInt(dateString.substring(5, 7));
        Month month = Month.getByIndexOneBased(monthIndex);

        int year = Integer.parseInt(dateString.substring(2, 4));
        int day = Integer.parseInt(dateString.substring(8, 10));
        
        try {
            return new MyDate(month, day, year);
        } catch (InstantiationException e) {
            e.printStackTrace();
            return null;
        } 
    }
}
