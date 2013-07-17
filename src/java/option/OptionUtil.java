package option;

public abstract class OptionUtil {
    
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
}
