package selenium;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;

public abstract class SeleniumTestDrive {

    public static void main(final String[] args) {
        secondExample();
    }
    
    @SuppressWarnings("unused")
    private static void firstExample() {
        // Create a new instance of the html unit driver
        // Notice that the remainder of the code relies on the interface, 
        // not the implementation.
        WebDriver driver = new HtmlUnitDriver();

        // And now use this to visit Google
        driver.get("http://www.google.com");

        // Find the text input element by its name
        WebElement element = driver.findElement(By.name("q"));

        // Enter something to search for
        element.sendKeys("Cheese!");

        // Now submit the form. WebDriver will 
        // find the form for us from the element
        element.submit();

        // Check the title of the page
        System.out.println("Page title is: " + driver.getTitle());
    }
    
    private static void secondExample() {
        // The Firefox driver supports javascript 
        WebDriver driver = new FirefoxDriver();
        
        // Go to the Google Suggest home page
        driver.get("http://www.google.com/webhp?complete=1&hl=en");
        
        // Enter the query string "Cheese"
        WebElement query = driver.findElement(By.name("q"));
        query.sendKeys("Cheese");

        // Sleep until the div we want is visible or 5 seconds is over
        final int sleepMillis = 5000;
        long end = System.currentTimeMillis() + sleepMillis;
        while (System.currentTimeMillis() < end) {
            WebElement resultsDiv = driver.findElement(By.className("gssb_e"));

            // If results have been returned, the results 
            // are displayed in a drop down.
            if (resultsDiv.isDisplayed()) {
              break;
            }
        }

        // And now list the suggestions
        List<WebElement> allSuggestions = 
            driver.findElements(By.xpath("//td[@class='gssb_a gbqfsf']"));
        
        for (WebElement suggestion : allSuggestions) {
            System.out.println(suggestion.getText());
        }
    }
}
