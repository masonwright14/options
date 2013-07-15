package option;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import csvreader.CsvReader;
import date.MyDate;


public final class OptionModel {
    
    private static final String[] FILE_NAMES = {
        "options130624.csv",
        "options130625.csv",
        "options130626.csv",
        "options130628.csv",
        "options130701.csv"
    };
    
    private static final List<String> FILE_NAME_LIST = 
        Arrays.asList(FILE_NAMES);

    private final List<OptionSnapshot> options;
    
    public OptionModel() {
        options = new ArrayList<OptionSnapshot>();
    }

    public void loadAllOptions() {
        for (String fileName: FILE_NAME_LIST) {
            options.addAll(OptionSnapshotFactory.getOptionSnapshots(
                CsvReader.getMyDate(fileName),
                CsvReader.getRowsAfterHeader(fileName)
            ));
        }
    }
    
    public List<OptionSnapshot> getOptionsByOptionSymbol(
        final String optionSymbol
    ) {
        List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        for (OptionSnapshot option: options) {
            if (option.getOptionSymbol().equals(optionSymbol)) {
                result.add(option);
            }
        }
        
        return result;
    }
    
    public List<OptionSnapshot> getOptionsByStockSymbol(
        final String stockSymbol
    ) {
        List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        for (OptionSnapshot option: options) {
            if (option.getStockSymbol().equals(stockSymbol)) {
                result.add(option);
            }
        }
        
        return result;
    }
    
    public List<OptionSnapshot> getOptionsBySnapshotDate(
        final MyDate snapshotDate
    ) {
        List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        for (OptionSnapshot option: options) {
            if (option.getSnapshotDate().equals(snapshotDate)) {
                result.add(option);
            }
        }
        
        return result;
    }
}
