package web;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public abstract class WebReader {
    
    public static String getText(final String address) {
        BufferedReader reader = null;
        
        try {
            final URL url = new URL(address);
            
            System.setProperty("http.agent", "");

            final URLConnection connection = url.openConnection();
            connection.setRequestProperty(
                "User-Agent", "Mozilla/5.0 " 
                + "(Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 " 
                + "(KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    		);
            reader = new BufferedReader(
                new InputStreamReader(connection.getInputStream())
            );

            final StringBuilder builder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                builder.append(line).append('\n');
            }
            
            return builder.toString();
        } catch (MalformedURLException mue) {
             mue.printStackTrace();
        } catch (IOException ioe) {
             ioe.printStackTrace();
        } finally {
            try {
                if (reader != null) {
                    reader.close();
                }
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }
        
        return null;
    }
}
