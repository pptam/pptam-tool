package test_case;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class TestServiceRoute {
    private WebDriver driver;
    private String baseUrl;
    private List<WebElement> routeList;

    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "/Users/hechuan/Downloads/chromedriver");
        driver = new ChromeDriver();
        baseUrl = "http://localhost:80/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    public void testGetRouteList() throws Exception {

        driver.get(baseUrl + "/");
        driver.findElement(By.id("refresh_route_button")).click();
        Thread.sleep(1000);

        //gain my results
        routeList = driver.findElements(By.xpath("//div/table[@id='route_list_table']/tbody"));
        if (routeList.size() > 0) {
            System.out.printf("Success to show routes list，the list size is:%d%n", routeList.size());
        }
        else
            System.out.println("Failed to show routes list，the list size is 0 or No orders in this user!");
        Assert.assertEquals(routeList.size() > 0,true);
    }

    @Test (dependsOnMethods = {"testGetRouteList"})
    public void testUpdateRoute() throws Exception {

        WebElement routeDistance = driver.findElement(By.xpath("//div/table[@id='route_list_table']/tbody/tr[4]/td[6]/input"));
        routeDistance.clear();
        routeDistance.sendKeys("0,1400");
        driver.findElement(By.xpath("//div/table[@id='route_list_table']/tbody/tr[4]/td[7]/button")).click();

        Alert alert = driver.switchTo().alert();
        alert.accept();
        String status = alert.getText();

        if (status.startsWith("Success")) {
            System.out.println("Update the route succeed!");
        }
        else
            System.out.println("Update the route failed!");

        Assert.assertEquals(true, status.startsWith("Success"));
    }

    @Test
    public void testAddRoute() throws Exception {

        driver.get(baseUrl + "/");
        JavascriptExecutor js = (JavascriptExecutor) driver;

        js.executeScript("document.getElementById('route_start_id').value='hechuan@outlook.com'");
        js.executeScript("document.getElementById('route_terminal_id').value='hechuan@outlook.com'");
        js.executeScript("document.getElementById('route_pass_station_id').value='hechuan@outlook.com'");
        js.executeScript("document.getElementById('route_pass_distance_id').value='120'");

        driver.findElement(By.id("create_route_button")).click();
        Thread.sleep(1000);
        //get Notification status
        String statusSendEmail = driver.findElement(By.id("create_route_create_message")).getText();
        if("".equals(statusSendEmail))
            System.out.println("Failed to Add route! Add route status is NULL");
        else if(statusSendEmail.startsWith("Success"))
            System.out.println("Add route status:"+statusSendEmail);
        else
            System.out.println("Failed to Add route! Add route status："+statusSendEmail);
        Assert.assertEquals(statusSendEmail.startsWith("Success"),true);

    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}