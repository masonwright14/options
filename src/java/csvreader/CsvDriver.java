package csvreader;

import stock.StockModel;

public abstract class CsvDriver {
    
    public static void main(final String[] args) {
        /*
        final OptionModel optionModel = new OptionModel();
        optionModel.loadAllOptions();
        
        System.out.println(
            optionModel.getOptionsByOptionSymbol("BAC130817C00005000")
        );
        */
        
        final StockModel stockModel = new StockModel();
        stockModel.loadAllStocks();
        System.out.println(stockModel.getStocks().get(0));
    }
}
