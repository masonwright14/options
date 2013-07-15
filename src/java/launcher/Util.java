package launcher;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public abstract class Util {
    
    public static String getDateDDMMYY() {
        DateFormat df = new SimpleDateFormat("ddMMyy");
        return df.format(new Date()); 
    }

    public static void printToFile(final String text) {
        
        final String fileName = "output.txt";
        final File outputFile = new File(fileName);

        Writer output = null;
        try {
            output = new BufferedWriter(new FileWriter(outputFile));
            output.write(text);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
