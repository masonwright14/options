package launcher;

public abstract class Launcher {

    public static void main(final String[] args) {
        StockPageVisitor.visitAllToPrint();
    }
}
