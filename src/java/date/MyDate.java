package date;

import java.util.Calendar;
import java.util.GregorianCalendar;


public final class MyDate implements Comparable<MyDate> {

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
    
    public String getCSVString() {
        StringBuilder builder = new StringBuilder();
        builder.append(String.format("%02d", day))
            .append(String.format("%02d", month.getIndexOneBased()))
            .append(String.format("%02d", year));
        return builder.toString();
    }
    
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("MyDate [month=");
        builder.append(month);
        builder.append(", day=");
        builder.append(day);
        builder.append(", year=20");
        builder.append(String.format("%02d", year));
        builder.append("]");
        return builder.toString();
    }
    
    public int daysFromThisToThat(final MyDate that) {
        final int yearOffset = 2000;
        Calendar calendarThis = 
            new GregorianCalendar(
                this.year + yearOffset, 
                this.month.getIndexOneBased(), 
                this.day
            );
        Calendar calendarThat = 
            new GregorianCalendar(
                that.year + yearOffset, 
                that.month.getIndexOneBased(), 
                that.day
            );
        final long thisTime = calendarThis.getTimeInMillis();
        final long thatTime = calendarThat.getTimeInMillis();
        final long differenceInMillis = thatTime - thisTime;
        final int millis = 1000;
        final int secondsPerHour = 3600;
        final int hoursPerDay = 24;
        return Math.round(
            differenceInMillis / (millis * secondsPerHour * hoursPerDay)
        );
    }

    @Override
    public int compareTo(final MyDate that) {
        if (this == that) {
            return 0;
        }
        
        if (this.year < that.year) {
            return -1;
        }
        if (this.year > that.year) {
            return 1;
        }
        if (this.month.getIndexOneBased() < that.month.getIndexOneBased()) {
            return -1;
        }
        if (this.month.getIndexOneBased() > that.month.getIndexOneBased()) {
            return 1;
        }
        if (this.day < that.day) {
            return -1;
        }
        if (this.day > that.day) {
            return 1;
        }
        
        return 0;
    }
}
