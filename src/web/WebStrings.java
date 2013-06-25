package web;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public abstract class WebStrings {
    public static List<List<String>> getTableContents(final String source) {
        if (source == null) {
            throw new IllegalArgumentException();
        }
        
        int i = source.indexOf("<table");
        if (i < 0) {
            throw new IllegalStateException();
        }
        
        final int endTable = source.indexOf("</table>", i);
        if (endTable < 0) {
            throw new IllegalStateException();
        }
        
        List<List<String>> result = new ArrayList<List<String>>();
        
        i = source.indexOf("<tr", i);
        if (i < 0) {
            throw new IllegalStateException();
        }
        while (i < endTable && i > 0) {
            final int endRowLength = 5;
            final int endRow = source.indexOf("</tr>", i) + endRowLength;
            if (endRow < 0) {
                throw new IllegalStateException();
            }
            
            result.add(getTableRowContents(source.substring(i, endRow)));
            
            i = source.indexOf("<tr", endRow);
        }
        
        return result;
    }
    
    public static List<String> getTableRowContents(final String source) {
        if (source == null) {
            throw new IllegalArgumentException();
        }
                        
        int i = source.indexOf("<tr");
        if (i < 0) {
            throw new IllegalStateException();
        }
        
        final int endRow = source.indexOf("</tr>", i);
        if (endRow < 0) {
            throw new IllegalStateException();
        }
        
        List<String> result = new ArrayList<String>();

        while (i < endRow) {
            boolean isTd = true;
            int temp = source.indexOf("<td", i);
            if (temp < 0 || temp > endRow) {
                i = source.indexOf("<th", i);
                isTd = false;
                if (i < 0 || i > endRow) {
                    break;
                }
            } else {
                i = temp;
            }
            
            final int endTagLength = 5;
            int endItem;
            if (isTd) {
                if (
                    source.indexOf("</td>", i) < 0 
                    || source.indexOf("</td>", i) > endRow
                ) {
                    throw new IllegalStateException(source.substring(i));
                }
                endItem = source.indexOf("</td>", i) + endTagLength;
            } else {
                if (
                    source.indexOf("</th>", i) < 0 
                    || source.indexOf("</th>", i) > endRow
                ) {
                    throw new IllegalStateException(
                        source.substring(i, endTagLength)
                    );
                }
                endItem = source.indexOf("</th>", i) + endTagLength;
            }
            
            result.add(getNestedTagContents(source.substring(i, endItem)));
            i = endItem;
        }
        
        return result;
    }
    
    public static String getNestedTagContents(final String source) {
        if (source == null) {
            throw new IllegalArgumentException();
        }
        
        Pattern closeTag = Pattern.compile("</[a-z]+>");
        Matcher matcher = closeTag.matcher(source);
        if (!matcher.find()) {
            throw new IllegalArgumentException(source);
        }
        
        int endIndex = matcher.start();
        int i = endIndex - 1;
        while (source.charAt(i) != '>' && i > 0) {
            i--;
        }
        
        if (source.charAt(i) != '>') {
            throw new IllegalArgumentException();
        }
        
        return source.substring(i + 1, endIndex);
    }
    
    public static List<String> getTagContents(
        final String tag, 
        final String source
    ) {
        if (source == null) {
            throw new IllegalArgumentException();
        }
        
        List<String> result = new ArrayList<String>();
        
        int i = 0;
        while (i < source.length()) {
            int oldI = i;
            i = source.indexOf("<" + tag + " ", i);
            if (i < 0) {
                i = oldI;
                i = source.indexOf("<" + tag + ">", i);
            }
            if (i < 0) {
                break;
            }
            
            i = source.indexOf(">", i);
            if (i < 0) {
                throw new IllegalStateException();
            }
            
            int startIndex = i + 1;
            i = startIndex;
            i = source.indexOf("</" + tag + ">", i);
            if (i < 0) {
                throw new IllegalStateException();
            }
            result.add(source.substring(startIndex, i));
        }
        
        return result;
    }
    
    public static String getStringFrom(
        final String start, 
        final String source
    ) {
        if (source == null) {
            return null;
        }
        
        int index = source.indexOf(start);
        if (index < 0) {
            return null;
        }
        
        return source.substring(index);
    }

    public static String getStringAfter(
        final String start, 
        final String source
    ) {
        if (source == null) {
            return null;
        }
        
        int index = source.indexOf(start);
        if (index < 0) {
            return null;
        }
        
        return source.substring(index + start.length());
    }
    
    public static String getStringThrough(
        final String end, 
        final String source
    ) {
        if (source == null) {
            return null;
        }
        
        int index = source.indexOf(end);
        if (index < 0) {
            return source;
        }
                
        return source.substring(0, index + end.length());
    }
    
    public static String getStringBefore(
        final String end, 
        final String source
    ) {
        if (source == null) {
            return null;
        }
        
        int index = source.indexOf(end);
        if (index < 0) {
            return source;
        }
                
        return source.substring(0, index);
    }
    
    public static String getStringFromThrough(
        final String from,
        final String to,
        final String source
    ) {
        return getStringThrough(to, getStringFrom(from, source));
    }
    
    public static String getStringFromTo(
        final String from,
        final String to,
        final String source
    ) {
        return getStringBefore(to, getStringFrom(from, source));
    }
    
    public static String getStringBetween(
        final String start,
        final String end,
        final String source
    ) {
        return getStringBefore(end, getStringAfter(start, source));
    }
}
