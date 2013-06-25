package selenium;


import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public abstract class SeleniumWebReader {

    public static String getText(final String address) {
        final WebDriver driver = new FirefoxDriver();
        driver.get(address);        
        
        final String result = driver.getPageSource();
        driver.quit();
        return result;
    }

}
