package option;

import java.util.ArrayList;
import java.util.List;

import date.MyDate;


public abstract class OptionSnapshotFactory {
    
    public static List<OptionSnapshot> getOptionSnapshots(
        final MyDate snapshotDate,
        final List<List<String>> data
    ) {
        List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        if (snapshotDate == null || data == null) {
            throw new IllegalArgumentException();
        }
        
        for (int i = 0; i < data.size(); i++) {
            OptionSnapshot newOption = 
                getOptionSnapshot(snapshotDate, data.get(i));
            if (newOption == null) {
                return null;
            }
            
            result.add(newOption);
        }
        
        return result;
    }

    public static OptionSnapshot getOptionSnapshot(
        final MyDate snapshotDate,
        final List<String> data
    ) {
        String optionSymbol = data.get(0);
        String stockSymbol = data.get(1);
        int bidInThous = 0;
        int askInThous = 0;
        int lastInThous = 0;
        try {
            bidInThous = OptionUtil.getNumber(data.get(2));
            askInThous = OptionUtil.getNumber(data.get(3));
            lastInThous = OptionUtil.getNumber(data.get(4));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

        int volume = 0;
        int openInterval = 0;
        if (data.size() == 5) {
            volume = OptionUtil.UNRECORDED_INT;
            openInterval = OptionUtil.UNRECORDED_INT;

        } else if (data.size() == 7) {
            try {
                volume = OptionUtil.getNumber(data.get(5));
                openInterval = OptionUtil.getNumber(data.get(6));
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }
        
        try {
            return new OptionSnapshot(
                optionSymbol,
                stockSymbol,
                bidInThous,
                askInThous,
                lastInThous,
                volume,
                openInterval,
                snapshotDate
            );
        } catch (InstantiationException e) {
            e.printStackTrace();
            return null;
        }
    }
}
