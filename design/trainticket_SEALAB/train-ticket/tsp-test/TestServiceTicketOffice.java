package test_case;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.util.List;
import java.util.concurrent.TimeUnit;

public class TestServiceTicketOffice {

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
    public void testQueryTicketOffice() {

        driver.get(baseUrl + "/");
        //*[@id="office_province"]
        WebElement province = driver.findElement(By.xpath("//div/select[@id='office_province']"));
        Select selectProvince = new Select(province);
        selectProvince.selectByValue("1"); // the first data.

        WebElement city = driver.findElement(By.xpath("//div/select[@id='office_city']"));
        Select selectCity = new Select(city);
        selectCity.selectByValue("1"); // the first data.

        WebElement region = driver.findElement(By.xpath("//div/select[@id='office_region']"));
        Select selectRegion = new Select(region);
        selectRegion.selectByValue("1"); // the first data.

        driver.findElement(By.id("query_office_button")).click();
        List<WebElement> rows = driver.findElements(By.xpath("//table[@id='office_list_table']/tbody/tr"));

        if (null != rows && !rows.isEmpty()) {
            System.out.println("Get ticket office list successfully!");
            Assert.assertEquals(true, (rows.size() > 0));
        }
        else {
            System.out.println("ERROR! There is no ticket office data!");
            Assert.assertEquals(true, (rows == null || rows.isEmpty()));
        }
    }

    @Test
    public void testQueryTicketOfficeWithoutProvince() {

        driver.get(baseUrl + "/");

        WebElement province = driver.findElement(By.xpath("//div/select[@id='office_province']"));
        Select selectProvince = new Select(province);
        selectProvince.selectByValue("0"); // the first data.

        driver.findElement(By.id("query_office_button")).click();
        Alert alert = driver.switchTo().alert();
        String alertMessage = alert.getText();
        boolean flag = alertMessage.startsWith("Please select the province");

        if (flag) {
            System.out.println("Please select the province!");
            Assert.assertEquals(true, flag);
        }
        else {
            Assert.assertEquals(false, flag);
        }
    }

    @Test
    public void testQueryTicketOfficeWithoutCity() {

        driver.get(baseUrl + "/");
        //*[@id="office_province"]
        WebElement province = driver.findElement(By.xpath("//div/select[@id='office_province']"));
        Select selectProvince = new Select(province);
        selectProvince.selectByValue("1"); // the first data.

        WebElement city = driver.findElement(By.xpath("//div/select[@id='office_city']"));
        Select selectCity = new Select(city);
        selectCity.selectByValue("0"); // the first data.

        driver.findElement(By.id("query_office_button")).click();
        Alert alert = driver.switchTo().alert();
        String alertMessage = alert.getText();
        boolean flag = alertMessage.startsWith("Please select the province, city");

        if (flag) {
            System.out.println("Please select the province, city!");
            Assert.assertEquals(true, flag);
        }
        else {
            Assert.assertEquals(false, flag);
        }
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
