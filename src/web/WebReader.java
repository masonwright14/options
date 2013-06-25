package web;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public abstract class WebReader {
    
    public static String getText(final String address) {
        URL url;
        URLConnection yc;
        BufferedReader br = null;
        String line;

        try {
            url = new URL(address);
            
            System.setProperty("http.agent", "");

            yc = url.openConnection();
            yc.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36");
            System.out.println(yc.getRequestProperties());
            br = new BufferedReader(new InputStreamReader(yc.getInputStream()));

            StringBuilder builder = new StringBuilder();
            while ((line = br.readLine()) != null) {
                builder.append(line).append('\n');
            }
            return builder.toString();
        } catch (MalformedURLException mue) {
             mue.printStackTrace();
        } catch (IOException ioe) {
             ioe.printStackTrace();
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException ioe) {
                ioe.printStackTrace();
            }
        }
        
        return null;
    }
}
