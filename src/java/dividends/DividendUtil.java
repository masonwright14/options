package dividends;

import date.Month;
import date.MyDate;

public abstract class DividendUtil {

    public static int getThousandths(final String amount) {
        final int minLength = 5;
        if (amount == null || amount.length() < minLength) {
            throw new IllegalArgumentException();
        }
        if (amount.charAt(0) != '$') {
            throw new IllegalArgumentException();
        }
        
        String newAmount = amount.replaceAll("\\$|\\,", "");
        final int dollars = 
            Integer.parseInt(newAmount.substring(0, newAmount.indexOf('.')));
        String fractionString = newAmount.substring(newAmount.indexOf('.') + 1);
        final int maxFractionDigits = 3;
        final int minFractionDigits = 2;
        if (fractionString.length() > maxFractionDigits) {
            fractionString = fractionString.substring(0, maxFractionDigits);
        } else if (fractionString.length() == minFractionDigits) {
            // pad with a zero to get thousandths
            fractionString += "0";
        }
        final int fractionPart = Integer.parseInt(fractionString);
        
        final int thousand = 1000;
        return fractionPart + dollars * thousand;
    }
    
    // mM/dD/YYYY
    public static MyDate getDividendDate(final String aDate) 
        throws InstantiationException {
        final int minLength = 8;
        if (aDate == null || aDate.length() < minLength) {
            throw new IllegalArgumentException();
        }
        
        int afterMonth = aDate.indexOf("/");
        int afterDay = aDate.indexOf("/", afterMonth + 1);
        if (afterDay < 0) {
            throw new IllegalArgumentException();
        }
        
        int monthNumber = Integer.parseInt(aDate.substring(0, afterMonth));
        Month month = Month.getByIndexOneBased(monthNumber);
        int day = Integer.parseInt(aDate.substring(afterMonth + 1, afterDay));
        final int yearOffset = 2000;
        int year = Integer.parseInt(aDate.substring(afterDay + 1)) - yearOffset;
        return new MyDate(month, day, year);
    }
    
    public static void main(final String[] args) {
        System.out.println(getThousandths("$0.55"));
        System.out.println(getThousandths("$0.1452"));
        System.out.println(getThousandths("$1.50"));
        try {
            System.out.println(getDividendDate("5/9/2013"));
            System.out.println(getDividendDate("12/10/2012"));
            System.out.println(getDividendDate("5/9/2013").getCSVString());
            System.out.println(getDividendDate("12/10/2012").getCSVString());
        } catch (InstantiationException e) {
            e.printStackTrace();
        }
    }
}
