package test_case;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class TestServiceVoucher {

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
    public void testSetOrderUsed()throws Exception{

        WebElement elementRefreshOrdersBtn = driver.findElement(By.id("refresh_order_button"));

        // for order type check box
        WebElement elementOrderTypeGTCJ = driver.findElement(By.xpath("//*[@id='microservices']/div[14]/div[1]/h3/input[1]"));
        WebElement elementOrderTypePT = driver.findElement(By.xpath("//*[@id='microservices']/div[14]/div[1]/h3/input[2]"));
        elementOrderTypeGTCJ.click();
        elementOrderTypePT.click();
        if(elementOrderTypeGTCJ.isEnabled() || elementOrderTypePT.isEnabled()){
            elementRefreshOrdersBtn.click();
            System.out.println("Show Orders according database!");
        }
        else {
            elementRefreshOrdersBtn.click();
            Alert javascriptConfirm = driver.switchTo().alert();
            javascriptConfirm.accept();
            elementOrderTypeGTCJ.click();
            elementOrderTypePT.click();
            elementRefreshOrdersBtn.click();
        }


        //gain orders
        List<WebElement> ordersList = driver.findElements(By.xpath("//table[@id='all_order_table']/tbody/tr"));

        WebElement elementOrderStatus = ordersList.get(0).findElement(By.xpath("td[8]/select"));
        Select selSeat = new Select(elementOrderStatus);
        selSeat.selectByValue("6"); // set order to used
        ordersList.get(0).findElement(By.xpath("td[9]/button")).click();
        Thread.sleep(1000);
        System.out.println("Success change the first order to used!");

        Assert.assertEquals(ordersList.size() > 0,true);
    }

    @Test (dependsOnMethods = {"testSetOrderUsed"})
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
    public  void testVoucher() throws Exception {

        driver.findElement(By.xpath("//*[@id='collapse0']/div/form/div[14]/div/button")).click();
        Thread.sleep(1000);

        List<WebElement> voucherList = driver.findElements(By.xpath("//*[@id='voucher_info']/table"));

        if (null == voucherList || voucherList.isEmpty()) {
            System.out.println("Failed! There is no voucher data!");
            Assert.assertEquals(true, null == voucherList || voucherList.isEmpty());
        } else {
            System.out.println("Succeed!");
            Assert.assertEquals(true, voucherList.size() == 1);
        }
    }

    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
