package date;

public enum Month {
    JAN(1), FEB(2), MAR(3), APR(4), MAY(5), JUN(6), 
        JUL(7), AUG(8), SEP(9), OCT(10), NOV(11), DEC(12);
    
    private final int indexOneBased;
    
    private Month(final int aIndex) {
        this.indexOneBased = aIndex;
    }
    
    public static Month getByIndexOneBased(final int index) {
        for (Month month: Month.values()) {
            if (month.indexOneBased == index) {
                return month;
            }
        }
        
        return null;
    }
    
    public int getIndexOneBased() {
        return this.indexOneBased;
    }
}
