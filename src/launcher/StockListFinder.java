package launcher;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import option.OptionUtil;
import option.MyDate;

import stocksymbols.StockSymbolWiki;

public abstract class StockListFinder {

    public static final String CSV_EXTENSION = ".csv";
    
    public static final String STOCK_LIST_PREFIX = "stockList";
   
    
    public static boolean isStockListSameAsMostRecent() {
        List<File> stockListFiles = getStockListFiles();
        if (stockListFiles.isEmpty()) {
            return false;
        }
        File mostRecentStockList = chooseByExtremeDate(stockListFiles, false);
        
        List<String> recentStockSymbols = 
            getCsvText(mostRecentStockList.getName()).get(0);
        List<String> currentSymbols = StockSymbolWiki.getDjiaSymbols();
        if (recentStockSymbols.size() != currentSymbols.size()) {
            return false;
        }
        
        for (int i = 0; i < recentStockSymbols.size(); i++) {
            if (!recentStockSymbols.get(i).equals(currentSymbols.get(i))) {
                return false;
            }
        }
        
        return true;
    }
    
    private static List<File> getStockListFiles() {
        List<File> result = new ArrayList<File>();
        
        for (File file: getFilesInPresentDirectory()) {
            if (
                file.getName().startsWith(STOCK_LIST_PREFIX)
                && file.getName().endsWith(CSV_EXTENSION)
            ) {
                result.add(file);
            }
        }
        
        return result;
    }
    
    private static File[] getFilesInPresentDirectory() {
        File file = new File(".");  
        return file.listFiles();  
    }
    
    private static List<List<String>> getCsvText(final String fileName) {
        BufferedReader bufferedReader = null;
        try {
            bufferedReader = new BufferedReader(new FileReader(fileName));

            List<List<String>> result = new ArrayList<List<String>>();
            String currentLine;
            while ((currentLine = bufferedReader.readLine()) != null) {
                List<String> newList = Arrays.asList(currentLine.split(","));
                result.add(newList);
            }
 
            return result;
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (bufferedReader != null) {
                    bufferedReader.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        
        throw new IllegalStateException();
    }
    
    private static String getDateString(final String fileName) {
        if (fileName == null) {
            throw new IllegalArgumentException();
        }
        
        Pattern datePattern = Pattern.compile("\\d\\d\\d\\d\\d\\d");
        Matcher matcher = datePattern.matcher(fileName);
        if (matcher.find()) {
            int dateIndex = matcher.start();
            final int dateLength = 6;
            return fileName.substring(dateIndex, dateIndex + dateLength);
        }
        
        throw new IllegalArgumentException();
    }
    
    /*
     * Returns - if first is less (earlier), 
     * 0 if same, + if first is greater (later)
     */
    private static int compareDateStrings(final String a, final String b) {
        if (!OptionUtil.isDateString(a) || !OptionUtil.isDateString(b)) {
            throw new IllegalArgumentException();
        }
        
        if (a.equals(b)) {
            return 0;
        }
        
        final int lessThan = -1;
        final int greaterThan = 1;
        
        final int yearA = getYear(a);
        final int yearB = getYear(b);
        if (yearA < yearB) {
            return lessThan;
        }
        if (yearA > yearB) {
            return greaterThan;
        }
        
        final int monthA = getMonth(a);
        final int monthB = getMonth(b);
        if (monthA < monthB) {
            return lessThan;
        }
        if (monthA > monthB) {
            return greaterThan;
        }
        
        final int dayA = getDay(a);
        final int dayB = getDay(b);
        if (dayA < dayB) {
            return lessThan;
        }
        if (dayA > dayB) {
            return greaterThan;
        }
        
        throw new IllegalStateException();
    }
    
    private static int getYear(final String dateString) {
        if (!OptionUtil.isDateString(dateString)) {
            throw new IllegalArgumentException();
        }
        
        int result = Integer.parseInt(dateString.substring(0, 2));
        if (result < MyDate.MIN_YEAR || result > MyDate.MAX_YEAR) {
            throw new IllegalArgumentException();
        }
        return result;
    }
    
    private static int getMonth(final String dateString) {
        if (!OptionUtil.isDateString(dateString)) {
            throw new IllegalArgumentException();
        }
        
        final int monthStart = 2;
        int result = Integer.parseInt(
            dateString.substring(monthStart, monthStart + 2)
        );
        if (result < 1 || result > MyDate.MAX_MONTH) {
            throw new IllegalArgumentException();
        }
        return result;
    }
    
    private static int getDay(final String dateString) {
        if (!OptionUtil.isDateString(dateString)) {
            throw new IllegalArgumentException();
        }
        
        final int dayStart = 4;
        int result = 
            Integer.parseInt(dateString.substring(dayStart, dayStart + 2));
        if (result < 1 || result > MyDate.MAX_DAY) {
            throw new IllegalArgumentException();
        }
        return result;
    }
    
    private static File chooseByExtremeDate(
        final List<File> files, 
        final boolean earliest
    ) {
        if (files.isEmpty()) {
            return null;
        }
        
        File result = files.get(0);
        String chosenDateString = getDateString(result.getName());
        for (final File file: files) {
            final String dateString = getDateString(result.getName());
            if (earliest) {
                if (compareDateStrings(dateString, chosenDateString) < 0) {
                    result = file;
                    chosenDateString = dateString;
                }
            } else {
                if (compareDateStrings(dateString, chosenDateString) > 0) {
                    result = file;
                    chosenDateString = dateString;
                }
            }
        }
        
        return result;
    }
}
