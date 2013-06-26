package launcher;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import option.MyDate;
import option.OptionSnapshot;
import option.OptionSymbolUtil;
import option.OptionUtil;
import selenium.SeleniumWebReader;
import stocksymbols.StockSymbolWiki;
import web.WebStrings;


public abstract class StockPageVisitor {

    private static final String OPTION_PAGE_PREFIX = 
        "http://ca.finance.yahoo.com/q/op?s=";
    
    private static final String STACKED_VIEW_PREFIX = 
        "http://ca.finance.yahoo.com/q/op?s=";
    
    private static final String MONTH_PAGE_INFIX = "&m=";

    private static final String NO_OPTIONS = 
        "There is no Options data available";
    
    private static final String FILE_PREFIX = "options";
    
    private static final String CSV_SUFFIX = ".csv";
    
    public static void visitAllToPrint() {
        // create file for today; if already exists, throw exception and quit

        final String fileName = FILE_PREFIX + getDateAsYYMMDD() + CSV_SUFFIX;
        final File outputFile = new File(fileName);
        
        Writer output = null;
        try {
            if (!outputFile.createNewFile()) {
                throw new IllegalStateException();
            }
            
            output = new BufferedWriter(new FileWriter(outputFile));
            output.write(OptionSnapshot.getCSVHeader() + "\n");
            System.out.println(OptionSnapshot.getCSVHeader());
            output.close();
        } catch (IOException e) {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }
            e.printStackTrace();

            return;
        }
        
        for (String stockSymbol: StockSymbolWiki.getDjiaSymbols()) {
            printToCsv(visitBySymbol(stockSymbol), outputFile);
        }
    }
    
    private static void printToCsv(
        final List<OptionSnapshot> optionDataList, 
        final File csvFile
    ) {
        if (csvFile == null || optionDataList == null) {
            throw new IllegalArgumentException();
        }
        
        if (!csvFile.exists()) {
            throw new IllegalArgumentException();
        }
        
        Writer output = null;
        try {
            output = new BufferedWriter(new FileWriter(csvFile, true));

            for (OptionSnapshot optionSnapshot: optionDataList) {
                output.write(optionSnapshot.getCSVString() + "\n");
                System.out.println(optionSnapshot.getCSVString());
            }
            
            output.close();
        } catch (IOException e) {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }
            e.printStackTrace();

            return;
        }
    }
    
    
    public static List<OptionSnapshot> visitBySymbol(final String stockSymbol) {
        final String url = OPTION_PAGE_PREFIX + getUrlSymbol(stockSymbol);
        final String text = SeleniumWebReader.getText(url);
        final List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        
        if (!hasOptions(text)) {
            System.out.println("No options: " + stockSymbol);
            return result;
        }
        
        final List<MyDate> expirationDates = getExpirationDates(text);
        for (MyDate date: expirationDates) {
            result.addAll(visitBySymbolAndDate(stockSymbol, date));
        }
        
        return result;
    }
    
    public static List<OptionSnapshot> visitBySymbolAndDate(
        final String stockSymbol, 
        final MyDate date
    ) {
        final String url = 
            STACKED_VIEW_PREFIX + getUrlSymbol(stockSymbol)
            + MONTH_PAGE_INFIX + "20" + date.getYear() + "-" 
            + date.getMonth().getIndexOneBased();
        final String text = SeleniumWebReader.getText(url);
        
        final String callTableText = WebStrings.getStringFromThrough(
            "<table", 
            "</table>", 
            WebStrings.getStringAfter(
                "<table", 
                WebStrings.getStringAfter(">Call Options<", text)
            )
        );
        
        final List<List<String>> callTableData = 
            WebStrings.getTableContents(callTableText);

        final String putTableText = 
            WebStrings.getStringFromThrough("<table", "</table>", 
            WebStrings.getStringAfter(
                "<table", 
                WebStrings.getStringAfter(">Put Options<", text)
            )
        );
        final List<List<String>> putTableData = 
            WebStrings.getTableContents(putTableText);
        
        return handleOptionPageData(stockSymbol, callTableData, putTableData);
    }
    
    private static List<OptionSnapshot> handleOptionPageData(
        final String stockSymbol,
        final List<List<String>> callTableData,
        final List<List<String>> putTableData
    ) {
        if (
            callTableData == null || putTableData == null
            || callTableData.isEmpty() || putTableData.isEmpty()
        ) {
            throw new IllegalArgumentException();
        }
        
        final int optionSymbolIndex = callTableData.get(0).indexOf("Symbol");
        final int lastIndex = callTableData.get(0).indexOf("Last");
        final int bidIndex = callTableData.get(0).indexOf("Bid");
        final int askIndex = callTableData.get(0).indexOf("Ask");
        final int volumeIndex = callTableData.get(0).indexOf("Vol");
        final int openIntervalIndex = callTableData.get(0).indexOf("Open Int");
        
        List<OptionSnapshot> result = new ArrayList<OptionSnapshot>();
        for (int callIndex = 1; callIndex < callTableData.size(); callIndex++) {
            final List<String> c = callTableData.get(callIndex);
            if (OptionSymbolUtil.isMiniOptionSymbol(c.get(optionSymbolIndex))) {
                continue;
            }
            
            result.add(
                new OptionSnapshot(
                    c.get(optionSymbolIndex), 
                    stockSymbol, 
                    OptionUtil.getPriceInThousandths(c.get(bidIndex)), 
                    OptionUtil.getPriceInThousandths(c.get(askIndex)), 
                    OptionUtil.getPriceInThousandths(c.get(lastIndex)),
                    OptionUtil.getNumber(c.get(volumeIndex)), 
                    OptionUtil.getNumber(c.get(openIntervalIndex))
                )
            );
        }
        
        for (int putIndex = 1; putIndex < putTableData.size(); putIndex++) {
            final List<String> p = putTableData.get(putIndex);
            result.add(
                new OptionSnapshot(
                    p.get(optionSymbolIndex), 
                    stockSymbol, 
                    OptionUtil.getPriceInThousandths(p.get(bidIndex)), 
                    OptionUtil.getPriceInThousandths(p.get(askIndex)), 
                    OptionUtil.getPriceInThousandths(p.get(lastIndex)),
                    OptionUtil.getNumber(p.get(volumeIndex)), 
                    OptionUtil.getNumber(p.get(openIntervalIndex))
                )
            );
        }
        
        return result;
    }
    
    private static List<MyDate> getExpirationDates(final String source) {
        List<MyDate> result = new ArrayList<MyDate>();
        
        final String wrappedDates = WebStrings.getStringBetween(
            "View By Expiration:", 
            "<table", 
            source
        );
                
        Set<String> dateStrings = new HashSet<String>();
        dateStrings.addAll(WebStrings.getTagContents("b", wrappedDates));
        dateStrings.addAll(WebStrings.getTagContents("a", wrappedDates));
        dateStrings.addAll(WebStrings.getTagContents("strong", wrappedDates));
        
        for (String dateString: dateStrings) {
            result.add(
                new MyDate(
                    OptionUtil.getMonthFromMonthYear(dateString), 
                    OptionUtil.getYearFromMonthYear(dateString)
                )
            );
        }
       
        return result;
    }
    
    private static boolean hasOptions(final String source) {
        return !source.contains(NO_OPTIONS);
    }
    
    private static String getUrlSymbol(final String symbol) {
        return symbol.replaceAll("\\.", "-");
    }
    
    private static String getDateAsYYMMDD() {
        final DateFormat dateFormat = new SimpleDateFormat("yyMMdd");
        return dateFormat.format(new Date()); 
    }
}
