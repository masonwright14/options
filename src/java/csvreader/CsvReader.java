package csvreader;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import date.Month;
import date.MyDate;


public abstract class CsvReader {

    public static List<String> getHeader(final String fileName) {
        return Arrays.asList(getFirstLine(fileName).split(","));
    }
    
    public static List<List<String>> getRowsAfterHeader(
        final List<String> fileNames
    ) {
        List<List<String>> result = new ArrayList<List<String>>();
        
        for (String fileName: fileNames) {
            result.addAll(getRowsAfterHeader(fileName));
        }
        
        return result;
    }
    
    public static MyDate getMyDate(final String fileName) {
        String dateString = getDateString(fileName);
        
        int monthIndex = Integer.parseInt(dateString.substring(2, 4));
        Month month = Month.getByIndexOneBased(monthIndex);

        int year = Integer.parseInt(dateString.substring(0, 2));
        int day = Integer.parseInt(dateString.substring(4, 6));
        
        try {
            return new MyDate(month, day, year);
        } catch (InstantiationException e) {
            e.printStackTrace();
            return null;
        } 
    }
    
    private static String getDateString(final String fileName) {
        final int optionsLength = 7;
        final int dateLength = 6;
        return fileName.substring(optionsLength, optionsLength + dateLength);
    }
    
    public static List<List<String>> getRowsAfterHeader(final String fileName) {
        final List<String> lines = getLines(fileName);
        lines.remove(0);
        
        final List<List<String>> result = new ArrayList<List<String>>();
        for (String line: lines) {
            result.add(Arrays.asList(line.split(",")));
        }
        
        return result;
    }
    
    public static List<String> getLines(final String fileName) {
        final File file = new File(fileName);
        
        List<String> result = new ArrayList<String>();
        
        try {
            BufferedReader input =  new BufferedReader(new FileReader(file));
          
            try {
                String line = null;
                /*
                 * readLine is a bit quirky :
                 * it returns the content of a line MINUS the newline.
                 * it returns null only for the END of the stream.
                 * it returns an empty String if two newlines appear in a row.
                 */
                while ((line = input.readLine()) != null) {
                    result.add(line);
                }
            } finally {
                input.close();
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        
        return result;
    }
    
    public static String getContents(final String fileName) {
        final File file = new File(fileName);
        
        StringBuilder contents = new StringBuilder();
        
        try {
            BufferedReader input =  new BufferedReader(new FileReader(file));
          
            try {
                String line = null;
                /*
                 * readLine is a bit quirky :
                 * it returns the content of a line MINUS the newline.
                 * it returns null only for the END of the stream.
                 * it returns an empty String if two newlines appear in a row.
                 */
                while ((line = input.readLine()) != null) {
                    contents.append(line);
                    contents.append(System.getProperty("line.separator"));
                }
            } finally {
                input.close();
            }
        } catch (IOException ex) {
            ex.printStackTrace();
            return null;
        }
        
        return contents.toString();
    }
    
    private static String getFirstLine(final String fileName) {
        final File file = new File(fileName);
                
        try {
            BufferedReader input =  new BufferedReader(new FileReader(file));
          
            try {
                String line = null;
                /*
                 * readLine is a bit quirky :
                 * it returns the content of a line MINUS the newline.
                 * it returns null only for the END of the stream.
                 * it returns an empty String if two newlines appear in a row.
                 */
                if ((line = input.readLine()) != null) {
                    return line;
                }
            } finally {
                input.close();
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        
        return null;
    }
}
