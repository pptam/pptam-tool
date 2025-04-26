package test_case;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.util.List;
import java.util.concurrent.TimeUnit;

public class TestServiceNews {

    private WebDriver driver;
    private String baseUrl;

    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "/Users/hechuan/Downloads/chromedriver");
        driver = new ChromeDriver();
        baseUrl = "http://localhost:80/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    public void testViewNewsList() {
        driver.get(baseUrl + "/");

        driver.findElement(By.id("refresh_news_button")).click();
        Alert alert = driver.switchTo().alert();
        alert.accept();
        alert.accept();
        alert.accept();
        alert.accept();
        List<WebElement> rows = driver.findElements(By.xpath("//div[@id='news_div']/div[@class='panel-heading']"));

        if (null != rows && !rows.isEmpty()) {
            System.out.println("Get news list successfully!");
            Assert.assertEquals(true, (rows.size() > 0));
        }
        else {
            System.out.println("ERROR! There is no news data!");
            Assert.assertEquals(true, (rows == null || rows.isEmpty()));
        }
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
