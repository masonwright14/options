package dividends;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import launcher.Logger;
import notifications.EmailSender;
import selenium.SeleniumWebReader;
import stocksymbols.StockSymbolWiki;
import web.WebStrings;

public abstract class DividendPageVisitor {

    private static final String FILE_PREFIX = "dividends";
    private static final String CSV_SUFFIX = ".csv";
    
    public static void main(final String[] args) {
        visitAllToPrint();
        
        /*
        try {
            System.out.println(doVisitByIndex(0));
        } catch (Exception e) {
            e.printStackTrace();
        }
        */
    }
    
    public static void visitAllToPrint() {
        final String fileName = FILE_PREFIX + getDateAsYYMMDD() + CSV_SUFFIX;
        final File outputFile = new File(fileName);
        
        Logger.clearMessages();
        Writer output = null;
        try {
            if (!outputFile.createNewFile()) {
                throw new IllegalStateException();
            }
            
            output = new BufferedWriter(new FileWriter(outputFile));
            output.write(Dividend.getCSVHeader() + "\n");
            System.out.println(Dividend.getCSVHeader());
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
        
        final int djiaSize = 30;
        for (int stockIndex = 0; stockIndex < djiaSize; stockIndex++) {
            try {
                printToCsv(doVisitByIndex(stockIndex), outputFile);
            } catch (Exception e) {
                Logger.logMessage("failed to visit index: " + stockIndex);
            }
        }
        
        if (Logger.getMessagesAsString() != null) {
            EmailSender.sendEmail(
                "masonwright14@gmail.com", 
                "ERROR", 
                Logger.getMessagesAsString()
            );
        } else {
            EmailSender.sendEmail(
                "masonwright14@gmail.com", 
                "SUCCESS", 
                "Job finished OK."
            );
        }
    }
    
    private static void printToCsv(
        final List<Dividend> dividendList, 
        final File csvFile
    ) {
        if (csvFile == null || dividendList == null) {
            throw new IllegalArgumentException();
        }
        
        if (!csvFile.exists()) {
            throw new IllegalArgumentException();
        }
        
        Writer output = null;
        try {
            output = new BufferedWriter(new FileWriter(csvFile, true));

            for (Dividend dividend: dividendList) {
                output.write(dividend.getCSVString() + "\n");
                System.out.println(dividend.getCSVString());
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
    
    private static List<Dividend> doVisitByIndex(
        final int symbolIndex
    ) throws Exception {
        final String url = DividendPages.getPages().get(symbolIndex);
        final String text = SeleniumWebReader.getText(url);
        
        final String dividendTableText = WebStrings.getStringFromThrough(
            "<table", 
            "</table>", 
            WebStrings.getStringAfter("Upcoming Dividend Payouts for", text)
        );
        
        final List<List<String>> dividendTableData = 
            WebStrings.getTableContents(dividendTableText);
                
        return handleDividendData(symbolIndex, dividendTableData);        
    }
    
    private static List<Dividend> handleDividendData(
        final int symbolIndex,
        final List<List<String>> dividendTableData
    ) throws ParseException {
        if (
            dividendTableData == null
        ) {
            throw new ParseException("Null table: " + symbolIndex, 0);
        }
        
        final int exDivIndex = 
            dividendTableData.get(0).indexOf("Ex-Dividend Date");
        final int thousIndex = dividendTableData.get(0).indexOf("Amount");
        
        List<Dividend> result = new ArrayList<Dividend>();
        for (
            int dividendIndex = 1; 
            dividendIndex < dividendTableData.size(); 
            dividendIndex++
        ) {
            final List<String> c = dividendTableData.get(dividendIndex);
            try {
                result.add(
                    new Dividend(
                        StockSymbolWiki.getDjiaSymbols().get(symbolIndex),
                        DividendUtil.getThousandths(c.get(thousIndex)), 
                        DividendUtil.getDividendDate(c.get(exDivIndex))
                    )
                );
            } catch (InstantiationException e) {
                Logger.logMessage(
                    "failed to get dividend: " + c.get(dividendIndex)
                );
            } catch (Exception e) {
                Logger.logMessage(
                    "failed to get a number: " 
                    + c.get(dividendIndex) + " " + e.getMessage()
                );
            }
        }
        
        return result;
    }
    
    private static String getDateAsYYMMDD() {
        final DateFormat dateFormat = new SimpleDateFormat("yyMMdd");
        return dateFormat.format(new Date()); 
    }
}
