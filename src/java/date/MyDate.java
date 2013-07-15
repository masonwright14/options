package date;

import java.util.Calendar;
import java.util.GregorianCalendar;


public final class MyDate {

    private final Month month;
    
    private int day;
    
    private final int year;
    
    public static final int MAX_YEAR = 20;
    public static final int MIN_YEAR = 00;
    public static final int MAX_DAY = 31;
    public static final int MAX_MONTH = 12;
    
    public MyDate(
        final Month aMonth,
        final int aDay,
        final int aYear
    ) throws InstantiationException {
        if (aMonth == null) {
            throw new InstantiationException();
        }
        if (aDay < 1 || aDay > MAX_DAY) {
            throw new InstantiationException();
        }

        if (aYear < MIN_YEAR || aYear > MAX_YEAR) {
            throw new InstantiationException();
        }
        
        this.month = aMonth;
        this.day = aDay;
        this.year = aYear;
    }
    
    public MyDate(
        final Month aMonth,
        final int aYear
    ) throws InstantiationException {
        if (aMonth == null) {
            throw new InstantiationException();
        }


        if (aYear < MIN_YEAR || aYear > MAX_YEAR) {
            final int twoThousand = 2000;
            final int aughtsYear = aYear - twoThousand;
            if (aughtsYear < MIN_YEAR || aughtsYear > MAX_YEAR) {
                throw new InstantiationException("" + aughtsYear);
            }
            
            this.year = aughtsYear;
        } else {
            this.year = aYear;
        }
        
        this.month = aMonth;
    }
    
    public static MyDate getCurrentDate() {
        Calendar calendar = new GregorianCalendar();
        Month month = 
            Month.getByIndexOneBased(calendar.get(Calendar.MONTH) + 1);
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        final int bias = 2000;
        int year = calendar.get(Calendar.YEAR) - bias;
        try {
            return new MyDate(month, day, year);
        } catch (InstantiationException e) {
            e.printStackTrace();
            return null;
        }
    }

    public Month getMonth() {
        return this.month;
    }

    public int getDay() {
        return this.day;
    }
    
    public void setDay(final int aDay) {
       this.day = aDay;
    }

    public int getYear() {
        return this.year;
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("MyDate [month=");
        builder.append(month);
        builder.append(", day=");
        builder.append(day);
        builder.append(", year=");
        builder.append(year);
        builder.append("]");
        return builder.toString();
    }
}