package test_case;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.util.List;
import java.util.concurrent.TimeUnit;

public class TestServiceConsign {
    private WebDriver driver;
    private String baseUrl;

    public static void login(WebDriver driver,String username,String password){
        driver.findElement(By.id("login_email")).clear();
        driver.findElement(By.id("login_email")).sendKeys(username);
        driver.findElement(By.id("login_password")).clear();
        driver.findElement(By.id("login_password")).sendKeys(password);
        driver.findElement(By.id("login_button")).click();
    }

    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "/Users/hechuan/Downloads/chromedriver");
        driver = new ChromeDriver();
        baseUrl = "http://localhost:80/";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    public void login()throws Exception{
        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(1000);

        //get login status
        String statusLogin = driver.findElement(By.id("login_result_msg")).getText();
        if("".equals(statusLogin))
            System.out.println("Failed to Login! Status is Null!");
        else if(statusLogin.startsWith("Success"))
            System.out.println("Success to Login! Status:"+statusLogin);
        else
            System.out.println("Failed to Login! Status:"+statusLogin);

        Assert.assertEquals(statusLogin.startsWith("Success"),true);
        driver.findElement(By.id("microservice_page")).click();
    }

    @Test (dependsOnMethods = {"login"})
    public void testViewMyOrders() throws Exception {

        driver.findElement(By.id("flow_three_page")).click();
        Thread.sleep(1000);
        driver.findElement(By.id("refresh_my_order_list_button_three")).click();
        Thread.sleep(1000);

        List<WebElement> orders = driver.findElements(By.id("my_orders_result_three"));
        if (null == orders || orders.isEmpty()) {
            System.out.println("Failed! There is no order data!");
            Assert.assertEquals(true, null == orders || orders.isEmpty());
        } else {
            System.out.println("Succeed!");
            Assert.assertEquals(true, orders.size() > 0);
        }
    }

    @Test (dependsOnMethods = {"testViewMyOrders"})
    public void testConsign() throws Exception {
        // consign the first order
        driver.findElement(By.xpath("//*[@id='collapse0']/div/form/div[13]/div/button")).click();
        Alert alert = driver.switchTo().alert();
        Thread.sleep(1000);
        alert.sendKeys("chuan"); // input consignee
        alert.accept();
        alert.sendKeys("123456789"); // input phone
        alert.accept();
        alert.sendKeys("10"); // input the weight of consign things
        alert.accept();
        Thread.sleep(1000);
        String status = alert.getText();
        alert.accept();
        boolean flag = status.startsWith("You have consigned successfully");

        if (flag) {
            System.out.println(status); // Consign Succeed
            Assert.assertEquals(true, flag);
        } else {
            System.out.println(status); // Consign Failed
            Assert.assertEquals(false, flag);
        }
    }

    @Test(dependsOnMethods = {"testConsign"})
    public void testViewConsigns() throws Exception {

        driver.findElement(By.id("refresh_my_consign_list_button3")).click();
        Thread.sleep(1000);

        List<WebElement> orders = driver.findElements(By.id("my_consigns_result3"));
        if (null == orders || orders.isEmpty()) {
            System.out.println("Failed! There is no consign data!");
            Assert.assertEquals(true, null == orders || orders.isEmpty());
        } else {
            System.out.println("Succeed!");
            Assert.assertEquals(true, orders.size() > 0);
        }
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
