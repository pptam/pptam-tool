package example;

import java.io.File;
import java.net.URL;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxBinary;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.remote.CommandExecutor;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.safari.SafariDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.WebDriverWait;

public class sample0  {
    public static void main(String[] args) {
    	
    	System.setProperty("webdriver.chrome.driver", "/Users/admin/work/workspace_spring/testing/selenium/selenium_webdriver/drivers/chromedriver");
		WebDriver driver = new ChromeDriver();
		
		driver.get("http://localhost:16006/hello6?cal=-1");
		driver.get("http://localhost:16006/hello6?cal=-10");
		driver.get("http://localhost:16006/hello6?cal=-200");
		driver.get("http://localhost:16006/hello6?cal=0.1");
		driver.get("http://localhost:16006/hello6?cal=0.5");
		driver.get("http://localhost:16006/hello6?cal=1");
		driver.get("http://localhost:16006/hello6?cal=2");
		driver.get("http://localhost:16006/hello6?cal=3");
		driver.get("http://localhost:16006/hello6?cal=4");
		driver.get("http://localhost:16006/hello6?cal=5");
		driver.get("http://localhost:16006/hello6?cal=6");
		driver.get("http://localhost:16006/hello6?cal=7");
		driver.get("http://localhost:16006/hello6?cal=8");
		driver.get("http://localhost:16006/hello6?cal=9");
		driver.get("http://localhost:16006/hello6?cal=9.9");
		driver.get("http://localhost:16006/hello6?cal=10");
		driver.get("http://localhost:16006/hello6?cal=25");
		driver.get("http://localhost:16006/hello6?cal=30");
		driver.get("http://localhost:16006/hello6?cal=50");
		driver.get("http://localhost:16006/hello6?cal=60");
		driver.get("http://localhost:16006/hello6?cal=80");
		driver.get("http://localhost:16006/hello6?cal=81");
		driver.get("http://localhost:16006/hello6?cal=90");
		driver.get("http://localhost:16006/hello6?cal=91");
		driver.get("http://localhost:16006/hello6?cal=95");
		driver.get("http://localhost:16006/hello6?cal=96");
		driver.get("http://localhost:16006/hello6?cal=97");
		driver.get("http://localhost:16006/hello6?cal=98");
		driver.get("http://localhost:16006/hello6?cal=100");
		driver.get("http://localhost:16006/hello6?cal=150");
		driver.get("http://localhost:16006/hello6?cal=120");
		driver.get("http://localhost:16006/hello6?cal=1000");
		
		
		driver.get("http://localhost:16005/hello5?cal=-10");
		driver.get("http://localhost:16005/hello5?cal=0.1");
		driver.get("http://localhost:16005/hello5?cal=10");
		driver.get("http://localhost:16005/hello5?cal=90");
		driver.get("http://localhost:16005/hello5?cal=96");
		driver.get("http://localhost:16005/hello5?cal=120");
		
		
		driver.get("http://localhost:16004/hello4?cal=-10");
		driver.get("http://localhost:16004/hello4?cal=0.1");
		driver.get("http://localhost:16004/hello4?cal=10");
		driver.get("http://localhost:16004/hello4?cal=90");
		driver.get("http://localhost:16004/hello4?cal=96");
		driver.get("http://localhost:16004/hello4?cal=120");
		
		
		driver.get("http://localhost:16003/hello3?cal=-10");
		driver.get("http://localhost:16003/hello3?cal=0.1");
		driver.get("http://localhost:16003/hello3?cal=10");
		driver.get("http://localhost:16003/hello3?cal=90");
		driver.get("http://localhost:16003/hello3?cal=96");
		driver.get("http://localhost:16003/hello3?cal=120");
		
		
		driver.get("http://localhost:16002/hello2?cal=-10");
		driver.get("http://localhost:16002/hello2?cal=0.1");
		driver.get("http://localhost:16002/hello2?cal=10");
		driver.get("http://localhost:16002/hello2?cal=90");
		driver.get("http://localhost:16002/hello2?cal=96");
		driver.get("http://localhost:16002/hello2?cal=120");
		
		
		driver.get("http://localhost:16001/hello1?cal=-10");
		driver.get("http://localhost:16001/hello1?cal=0.1");
		driver.get("http://localhost:16001/hello1?cal=10");
		driver.get("http://localhost:16001/hello1?cal=90");
		driver.get("http://localhost:16001/hello1?cal=96");
		driver.get("http://localhost:16001/hello1?cal=120");
		
		
		driver.get("http://localhost:16000/greeting?cal=-10");
		driver.get("http://localhost:16000/greeting?cal=0.1");
		driver.get("http://localhost:16000/greeting?cal=10");
		driver.get("http://localhost:16000/greeting?cal=90");
		driver.get("http://localhost:16000/greeting?cal=96");
		driver.get("http://localhost:16000/greeting?cal=120");
		
		
        driver.quit();
    }
}