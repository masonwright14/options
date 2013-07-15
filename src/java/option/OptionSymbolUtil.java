package option;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import date.DateUtil;
import date.MyDate;

public abstract class OptionSymbolUtil {
    
    public static boolean isMiniOptionSymbol(final String target) {
        if (target == null) {
            return false;
        }

        boolean couldBeMiniOptionSymbol = 
            target.matches("[A-Z]{1,6}\\d{7}[P|C]\\d{8}");
        if (!couldBeMiniOptionSymbol) {
            return false;
        }
        
        return true;
    }

    public static boolean isOptionSymbol(final String target) {
        if (target == null) {
            return false;
        }

        boolean couldBeOptionSymbol = 
            target.matches("[A-Z]{1,6}\\d{6}[P|C]\\d{8}");
        if (!couldBeOptionSymbol) {
            return false;
        }
        
        return true;
    }
    
    public static int getYear(final String optionSymbol) {
        return getYearFromDate(getDateString(optionSymbol));
    }
    
    public static int getMonth(final String optionSymbol) {
        return getMonthFromDate(getDateString(optionSymbol));
    }
    
    public static int getDay(final String optionSymbol) {
        return getDayFromDate(getDateString(optionSymbol));
    }
    
    public static String getStockSymbol(final String optionSymbol) {
        if (optionSymbol == null || !isOptionSymbol(optionSymbol)) {
            throw new IllegalArgumentException();
        }
        
        int firstDigitIndex = 0;
        while (!Character.isDigit(optionSymbol.charAt(firstDigitIndex))) {
            firstDigitIndex++;
        }
        
        return optionSymbol.substring(0, firstDigitIndex);
    }
    
    public static boolean isCall(final String optionSymbol) {
        if (optionSymbol == null || !isOptionSymbol(optionSymbol)) {
            throw new IllegalArgumentException();
        }
        
        int firstDigitIndex = 0;
        while (!Character.isDigit(optionSymbol.charAt(firstDigitIndex))) {
            firstDigitIndex++;
        }
        
        int indicatorIndex = optionSymbol.indexOf('C', firstDigitIndex);
        return (indicatorIndex > 0);
    }
    
    public static long getStrikePriceInThousandths(final String optionSymbol) {
        if (optionSymbol == null || !isOptionSymbol(optionSymbol)) {
            throw new IllegalArgumentException();
        }
        
        int i = optionSymbol.length() - 1;
        while (!Character.isLetter(optionSymbol.charAt(i))) {
            i--;
        }
        
        long result = Long.parseLong(optionSymbol.substring(i + 1));
        return result;
    }
    
    private static String getDateString(final String optionSymbol) {
        if (optionSymbol == null) {
            throw new IllegalArgumentException();
        }
        
        Pattern datePattern = Pattern.compile("\\d\\d\\d\\d\\d\\d");
        Matcher matcher = datePattern.matcher(optionSymbol);
        if (matcher.find()) {
            int dateIndex = matcher.start();
            final int dateLength = 6;
            return optionSymbol.substring(dateIndex, dateIndex + dateLength);
        }
        
        throw new IllegalArgumentException();
    }
    
    private static int getYearFromDate(final String dateString) {
        if (!DateUtil.isDateString(dateString)) {
            throw new IllegalArgumentException();
        }
        
        int result = Integer.parseInt(dateString.substring(0, 2));
        if (result < MyDate.MIN_YEAR || result > MyDate.MAX_YEAR) {
            throw new IllegalArgumentException();
        }
        return result;
    }
    
    private static int getMonthFromDate(final String dateString) {
        if (!DateUtil.isDateString(dateString)) {
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
    
    private static int getDayFromDate(final String dateString) {
        if (!DateUtil.isDateString(dateString)) {
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
}
