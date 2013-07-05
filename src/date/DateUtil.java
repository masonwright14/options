package date;

import java.util.regex.Matcher;
import java.util.regex.Pattern;


public abstract class DateUtil {
    
    private static final String JAN_STR = "Jan";
    private static final String FEB_STR = "Feb";
    private static final String MAR_STR = "Mar";
    private static final String APR_STR = "Apr";
    private static final String MAY_STR = "May";
    private static final String JUN_STR = "Jun";
    private static final String JUL_STR = "Jul";
    private static final String AUG_STR = "Aug";
    private static final String SEP_STR = "Sep";
    private static final String OCT_STR = "Oct";
    private static final String NOV_STR = "Nov";
    private static final String DEC_STR = "Dec";
    
    private static final String NOT_APPLICABLE = "N/A";
    
    public static final int NOT_APPLICABLE_INT = -5;
    
    public static final int UNRECORDED_INT = -4;
    
    public static int getNumber(final String number) 
        throws Exception {
        if (number == null) {
            throw new IllegalArgumentException();
        }
        
        if (number.equals(NOT_APPLICABLE)) {
            return NOT_APPLICABLE_INT;
        }
        
        try {
            int result = Integer.parseInt(number.replaceAll(",", ""));
            return result;
        } catch (NumberFormatException e) {
            throw new Exception(number);
        }
    }
    
    public static int getPriceInThousandths(final String number) 
        throws Exception {
        if (number == null) {
            throw new IllegalArgumentException();
        }
        final boolean couldBePrice = 
            number.matches("\\d{1,6}\\.\\d{2,3}");
        if (!couldBePrice) {
            if (number.equals(NOT_APPLICABLE)) {
                return NOT_APPLICABLE_INT;
            }
            
            throw new Exception(number);
        }
        
        final int decimalIndex = number.indexOf('.');
        final String integerPart = number.substring(0, decimalIndex);
        final String fractionPart = number.substring(decimalIndex + 1);
        final int integer = Integer.parseInt(integerPart);
        final int fraction = Integer.parseInt(fractionPart);
        final int thousand = 1000;
        final int ten = 10;
        final int three = 3;
        
        if (fractionPart.length() == 2) {
            return integer * thousand + fraction * ten;
        } else if (fractionPart.length() == three) {
            return integer * thousand + fraction;
        } 
        
        throw new Exception(number);
    }
    
    public static boolean isDateString(final String target) {
        if (target == null) {
            return false;
        }
        
        final int digitLength = 6;
        if (target.length() != digitLength) {
            return false;
        }
        
        Pattern datePattern = Pattern.compile("\\d\\d\\d\\d\\d\\d");
        Matcher matcher = datePattern.matcher(target);
        if (!matcher.find()) {
            return false;
        }
        
        return true;
    }
    
    public static Month getMonthFromMonthYear(final String date) 
        throws Exception {
        if (date == null) {
            throw new IllegalArgumentException();
        }
        
        int i = 0;
        for (; i < date.length(); i++) {
            if (Character.isLetter(date.charAt(i))) {
                break;
            }
        }
        
        final int monthLength = 3;
        if (i == date.length() || i + monthLength > date.length()) {
            throw new Exception(date);
        }
        
        String monthName = date.substring(i, i + monthLength);
        return getMonth(monthName);
    }
    
    public static int getYearFromMonthYear(final String date) 
        throws Exception {
        if (date == null) {
            throw new IllegalArgumentException();
        }
        
        int i = 0;
        for (; i < date.length(); i++) {
            if (Character.isLetter(date.charAt(i))) {
                break;
            }
        }
        
        final int monthLength = 3;
        if (i == date.length() || i + monthLength > date.length()) {
            throw new Exception(date);
        }
        
        int j = i + monthLength;
        for (; j < date.length(); j++) {
            if (Character.isDigit(date.charAt(j))) {
                break;
            }
        }
        
        final int yearLength = 4;
        if (j == date.length() || j + yearLength > date.length()) {
            throw new Exception(date);
        }
        String yearName = date.substring(j, j + yearLength);

        try {
            int result = Integer.parseInt(yearName);
            return result;
        } catch (NumberFormatException e) {
            throw new Exception(yearName);
        }
    }

    public static Month getMonth(final String monthName) 
        throws Exception {
        if (monthName == null) {
            throw new IllegalArgumentException();
        }
        if (monthName.equalsIgnoreCase(JAN_STR)) {
            return Month.JAN;
        }
        if (monthName.equalsIgnoreCase(FEB_STR)) {
            return Month.FEB;
        }
        if (monthName.equalsIgnoreCase(MAR_STR)) {
            return Month.MAR;
        }
        if (monthName.equalsIgnoreCase(APR_STR)) {
            return Month.APR;
        }
        if (monthName.equalsIgnoreCase(MAY_STR)) {
            return Month.MAY;
        }
        if (monthName.equalsIgnoreCase(JUN_STR)) {
            return Month.JUN;
        }
        if (monthName.equalsIgnoreCase(JUL_STR)) {
            return Month.JUL;
        }
        if (monthName.equalsIgnoreCase(AUG_STR)) {
            return Month.AUG;
        }
        if (monthName.equalsIgnoreCase(SEP_STR)) {
            return Month.SEP;
        }
        if (monthName.equalsIgnoreCase(OCT_STR)) {
            return Month.OCT;
        }
        if (monthName.equalsIgnoreCase(NOV_STR)) {
            return Month.NOV;
        }
        if (monthName.equalsIgnoreCase(DEC_STR)) {
            return Month.DEC;
        }
        
        throw new Exception(monthName);
    }
}
