package launcher;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public abstract class Logger {

    private static final String LOG_PREFIX = "log";
    
    private static final List<String> MESSAGES = new ArrayList<String>();
    
    public static void clearMessages() {
        MESSAGES.clear();
    }
    
    public static String getMessagesAsString() {
        if (MESSAGES.isEmpty()) {
            return null;
        }
        
        StringBuilder builder = new StringBuilder();
        for (String message: MESSAGES) {
            builder.append(message).append("\n\n");
        }
        
        return builder.toString();
    }
    
    public static void logMessage(final String text) {
        MESSAGES.add(text);
        Writer output = null;
        try {
            output = new BufferedWriter(
                new FileWriter(getLogFileAndCreateIfNeeded(), 
                true
            ));
            output.write(text + "\n\n");
            output.close();
        } catch (IOException e) {
            if (output != null) {
                try {
                    output.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }
            e.printStackTrace();

            return;
        }
    }
    
    private static File getLogFileAndCreateIfNeeded() {
        final String fileName = LOG_PREFIX + getDateAsYYMMDD() + ".txt";
        final File outputFile = new File(fileName);
        try {
            outputFile.createNewFile();
        } catch (final IOException e) {
            e.printStackTrace();
            return null;
        }
        
        return outputFile;
    }
    
    private static String getDateAsYYMMDD() {
        final DateFormat dateFormat = new SimpleDateFormat("yyMMdd");
        return dateFormat.format(new Date()); 
    }
}
