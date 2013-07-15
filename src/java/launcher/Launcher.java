package launcher;

import java.awt.Toolkit;

public abstract class Launcher {

    public static void main(final String[] args) {
        StockPageVisitor.visitAllToPrint();
        Toolkit.getDefaultToolkit().beep();
    }
}
